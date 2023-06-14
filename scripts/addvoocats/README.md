# addvoocats.py Documentation


Purpose:
---------
The addvoocats.py script is a utility tool designed to automate the process of adding Bengali Wikipedia (bn.wikipedia.org) categories to pages based on their corresponding English Wikipedia (en.wikipedia.org) categories. It aims to make it easier to synchronize category information between the English and Bengali versions of Wikipedia.

Features:
---------
1. File-based Mode: The script can read a list of page titles from a file and process each page individually.

2. Category-based Mode: The script can work on all pages within a specific category. It supports customization of the category depth, allowing the inclusion of subcategories as well.

3. Recent Pages Mode: The script can process a specified number of recently created or modified pages.

4. Single Page Mode: The script can operate on a single page.

5. Template Mode: The script can work on all pages where a specific template is used.

6. Multithreading: The script utilizes threading to process multiple pages concurrently, improving efficiency.

Customization:
---------------
The addvoocats.py script provides several options for customization:

1. File Path: The default file path for page titles is set to "data/addvoocats.txt". You can customize the file path by providing the `-file` argument followed by the desired file path.

2. Category Depth: By default, the category depth is set to 1, meaning only the immediate categories of a given category are considered. You can customize the category depth by providing the `-depth` argument followed by the desired depth value (limited to a maximum depth of 5).

3. Recent Pages: By default, the script does not process any recent pages. You can customize the number of recent pages to be processed by providing the `-recent` argument followed by the desired number.

4. Single Page: By default, the script does not process any specific page. You can customize the page by providing the `-page` argument followed by the desired page title.

5. Template: By default, the script does not process any specific template. You can customize the template by providing the `-template` argument followed by the desired template name.

Usage:
------
The addvoocats.py script is executed from the command line and accepts various options as arguments. Here are some example usages:

1. Process pages from a file:
   $ python addvoocats.py -file test.txt

2. Process all pages within a category:
   $ python addvoocats.py -cat Category_Name

3. Process all pages within a category and its subcategories (up to a depth of 3):
   $ python addvoocats.py -cat Category_Name -depth 3

4. Process the 50 most recent pages:
   $ python addvoocats.py -recent 50

5. Process a specific page:
   $ python addvoocats.py -page Page_Title

6. Process pages where a specific template is used:
   $ python addvoocats.py -template Template_Name

Note: You can include multiple options together to perform customized operations.

Dependencies:
--------------
The addvoocats.py script requires the following dependencies to be installed:

- Pywikibot: The script uses the Pywikibot framework to interact with the Wikipedia API. You can install Pywikibot by following the installation instructions provided at https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation.

- Python 3: The script is compatible with Python 3.x versions.

Contributing:
--------------
If you wish to contribute to the addvoocats.py script, you can fork the repository on GitHub 







# Future Feature
* -file:"name"
* -page:"name" -wth | -lop
* -template:"name"
* -cat:"name" -cats -depth:"0" -start:"xx" -end:"zz"
* -recent:int -cats
