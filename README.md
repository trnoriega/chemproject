# Flavor chemical database and classifier

In this project I created (1) a database of flavor chemicals and their flavor descriptors, (2) Found the underlying flavor profiles in the database to create labels for a machine learning classifier, and (3) calculated chemical properties that could be used as features in a machine learning classifier, (4) trained a classifier to identify chemical class.  

## Making the flavor chemical database 

__[1_fema_extraction](1_fema_extraction.ipynb):__

In this notebook I extract information from the The Flavor and Extract Manufacturers Association (FEMA) website.

Each chemical has its own page (for example, [acetic acid](https://www.femaflavor.org/acetic-acid-2)) from which I extracted:
- Flavor descriptors
- FEMA and Chemical Abstracts Service (CAS) registry numbers

__[2_jecfa_extraction](2_jecfa_extraction.ipynb)__

In this notebook I extract information from the the Joint FAO/WHO Expert Committee on Food Additives  (JECFA) website.

Each chemical has its own page (for example, [acetic acid](http://www.fao.org/food/food-safety-quality/scientific-advice/jecfa/jecfa-flav/details/en/c/3/)) from which I extracted:
- Odor/flavor
- Synonyms
- Molecular weight
- JECFA and FEMA numbers

__[3_fema_jecfa_merge](3_fema_jecfa_merge.ipynb)__

In this notebook I merge the information extracted from the FEMA and JECFA websites. I make sure that each entry is for the same chemical and that all chemicals included have usable flavor/aroma descriptors.

__[4_rdkit_chemical_matching](4_rdkit_chemical_matching.ipynb)__

In this notebook I pair the chemicals found above with their RDkit representations. 

The [RDkit](http://www.rdkit.org/docs/Overview.html) is a chemical informatics toolkit. It allows for the calculation of chemical descriptors which can then be used as features for machine learning tasks. 

By this point I have 2170 chemicals that can be used to train a machine learning classifier. 

## Finding labels for machine learning classification

## Calculating chemical properties to use as machine learning features