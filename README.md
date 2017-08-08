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

By this point I have __2170 chemicals__ that can be used to train a machine learning classifier. 

## Unsupervised clustering based on flavor descriptors

__[5_descriptor_clustering](5_descriptor_clustering.ipynb)__

In this notebook I use use K-Means clustering the group the flavor chemicals based on their flavor and aroma descriptors.

I found two minimal groups: 

- One very large __fruity, floral__ group with 1880 chemicals
- A smaller __savory, roast__ group with 290 chemicals

They can be visualized with word clouds of all the descriptors in each group:

![](Images/1_wordcloud.png')

I can now use these labels to train a supervised machine learning classifier.

## Calculating chemical properties to use as machine learning features

__[6_property_calculations](6_property_calculations.ipynb)__

In this notebook I use the RDKit to calculate several quantitative chemical properties. I also generated three different "chemical fingerprints" based on either chemical fragments or topology for each molecule. In all, for each chemical __4422 features__ were generated.

## Training and testing a classifier to identify chemical class

__[7_algorithm_comparison](7_algorithm_comparison.ipynb)__

In this notebook ...

__[8_parameter_optimization](8_parameter_optimization.ipynb)__

In this notebook ...

__[9_estimator_analysis](9_estimator_analysis.ipynb)__

In this notebook ...
