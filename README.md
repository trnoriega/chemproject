# Flavor chemical database and classifier

In this project I created a database of flavor chemicals and their flavor descriptors based on information found in two sources:

1) The Flavor and Extract Manufacturers Association (FEMA) website

2) The Joint FAO/WHO Expert Committee on Food Additives  (JECFA) website


### The FEMA website

The FEMA website contains a series of [library pages](https://www.femaflavor.org/flavor/library?page=) that list all of the FEMA chemicals.


Each chemical then has its own page (for example, [acetic acid](https://www.femaflavor.org/acetic-acid-2)) from which I will extract:
- Flavor descriptors
- Chemical Abstracts Service (CAS) registry number
- JECFA number

The scripts used to extract the information from the FEMA website can be found in the [fema_extraction](fema_extraction.ipynb) notebook


### The JECFA website

The JECFA website contains an [index](http://www.fao.org/food/food-safety-quality/scientific-advice/jecfa/jecfa-flav/browse-alphabetically/en/) with all of the chemicals for which it has information.

Each chemical then has its own page (for example, [acetic acid]http://www.fao.org/food/food-safety-quality/scientific-advice/jecfa/jecfa-flav/details/en/c/3/) from which I will extract:
- Odor
- Physical form
- Synonyms
- JECFA, CAS, FEMA numbers
