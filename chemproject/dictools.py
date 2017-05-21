import nltk
from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup
from chemspipy import ChemSpider
cs = ChemSpider('0201ba66-585d-4135-9e6b-d28ba4724fcf')
from rdkit import Chem
from rdkit.Chem import Descriptors
from inspect import getmembers, isfunction

def link_to_soup(link):
    '''
    support function for dictionary_maker and search_and_filter.
    makes a beautiful soup object from link. Disguises itself
    as a browser so its not confused for a bot

    input:
    link: to use as the source for the Beautiful soup object

    returns:
    -Soup object if one can be made
    -None otherwise
    '''
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
    except:
        return None

    return soup

def search_and_filter(number,
                      search_prefix='http://www.femaflavor.org/search/apachesolr_search/',
                      substring='/flavor/library/'):
    '''
    support function for dictionary_maker
    searches the Fema website for the number given and
    returns a list of links that contain the substring.
    Returns None otherwise

    Inputs:
    -number: Fema number to search for
    -search_prefix: web address prefix to search in
    -substring: to filter results

    Returns:
    -page_headings
    -name
    -link

    or
    -None if none are found
    '''


    search_link = search_prefix + str(number)
    soup = link_to_soup(search_link)
    if soup:
        search_block = soup.find_all('dl', class_='search-results apachesolr_search-results')
    else:
        return None

    #See if there are any results and extract only the links to flavor compounds
    try:
        titles = search_block[0].find_all('dt', class_='title')
        #extract all search result links
        links = [title.find('a').get('href') for title in titles]
        #select only links with flavor compund substring
        links_checked = [link for link in links if substring in link]
    except:
        return None

    if len(links_checked) >= 1:
        for link in links_checked:
            soup = linkToSoup(link)
            if soup:
                page_title = soup.find('h2', class_='page_title')
                page_headings = soup.find_all('div', class_='field field-type-header')
                title = page_title.text.split('|')
                title = [word.strip() for word in title]
                name = title[0] #compound name
                title_num = title[-1] #compound number
                if title_num == str(number):
                    return page_headings, name, link
    else:
        return None

def same_chemical(results):
    '''
    returns an rdkit chemical object if a the chemicals in a chemspipy result list have:
    -the same molecular weight, and
    -the same smiles representation
    returns None otherwise
    '''
    if results.count == 0:
        return None

    smiles = []
    mws = []

    if results.count >= 1:
        for chemical in results:
            try:
                smiles_base = chemical.smiles
                chem_base = Chem.MolFromSmiles(smiles_base)

                smiles_temp = Chem.MolToSmiles(chem_base)
                smiles.append(smiles_temp)

                mw_temp = Chem.Descriptors.MolWt(chem_base)
                mws.append(mw_temp)
            except:
                continue

        if (len(set(smiles)) == 1 and
                len(set(mws)) == 1):
            return Chem.MolFromSmiles(Chem.MolToSmiles(chem_base))

    else:
        return None

def chem_search(dict_entry, priotity_list):
    '''
    returns a rdkit molecule after searching the chemspider database based on the items
    in the priority list.
    '''

    for tup in priotity_list:
        try:
            tup_string = dict_entry.get(tup[1])
        except AttributeError:
            continue

        if tup_string:
            search_string = tup[0] + tup_string
            #print('searching for: {}' .format(search_string))
            results = cs.search(search_string)
            #print('stopped searching')
            if same_chemical(results):
                #print(tup)
                return same_chemical(results)
            else:
                continue
    return None

def dictionary_maker(num_iterator):
    '''
    returns a dictionary of chemicals found in the femaflavor.org website with FEMA numbers in
    the given num_iterator

    inputs:
    -num_iterator: an iterable object with the fema numbers to be searched

    returns:
    dictionary with fema number as primary key and the following subkeys:
    'link','name', 'descriptors', 'CAS', 'JECFA', 'CFR'
    '''

    dictionary = {}
    count = 0
    priority_list = [('fema ', 'FEMA'), ('jecfa ', 'JECFA'), ('', 'CAS'), ('', 'name')]

    for number in num_iterator:
        #searchNameLink is (pageHeadings, name, link) if there is a FEMA website for number.
        # None otherwise
        page_name_link = search_and_filter(number)

        if page_name_link:
            #Add all information from FEMA webpage to dictionary[number][subentries]
            dictionary[number] = {}
            dictionary[number]['link'] = page_name_link[2]
            dictionary[number]['name'] = page_name_link[1]
            dictionary[number]['FEMA'] = str(number)
            for item in page_name_link[0]:
                try:
                    label = item.find('h3', class_='field-label').stripped_strings
                    label = list(label)[0]
                    content = item.find('div', class_='field-item').stripped_strings
                    content = list(content)[0]
                except:
                    continue

                if label == 'FLAVOR PROFILE':
                    dictionary[number]['descriptors'] = content
                    #lowercase, remove non-word characters (function1), and reduce words
                    # to their stem (function2)
                    content.lower()
                    pattern = re.compile('[\W_]+')
                    pattern.sub(' ', content)
                    stemmer = nltk.stem.SnowballStemmer('english')
                    stems = [stemmer.stem(word) for word in content.split(' ')]
                    stems = ' '.join(stems)
                    text = nltk.word_tokenize(stems)
                    tokens = nltk.pos_tag(text)
                    selected = [token[0] for token in tokens if token[1] in ['NN', 'JJ']]
                    dictionary[number]['tokens'] = selected
                elif label == 'CAS':
                    dictionary[number]['CAS'] = content
                elif label == 'JECFA NUMBER':
                    dictionary[number]['JECFA'] = content
                elif label == 'CFR':
                    dictionary[number]['CFR'] = content

            #Add rdkit molecule to dictionary[number]['rdkit Mol']
            test = chem_search(dictionary[number], priority_list)
            if test:
                dictionary[number]['rdkit Mol'] = test
            else:
                print(' {}nMol' .format(number), end='')

        else:
            print(' {}nLink' .format(number), end='')

        count += 1
        if count%10 == 0:
            print(' {:.2f}%' .format(count/len(num_iterator)*100), end='')
        else:
            print('.', end='')
    return dictionary
