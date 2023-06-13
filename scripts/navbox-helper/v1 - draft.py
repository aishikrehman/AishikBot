# import pywikibot

# # Set up the Wikipedia sites
# site_en = pywikibot.Site("en", "wikipedia")
# site_bn = pywikibot.Site("bn", "wikipedia")
# repo = site_en.data_repository()

# # Define the path to the text file containing the article titles
# filename = "data/articles.txt"

# # Read the article titles from the text file into a list
# with open(filename, "r", encoding="utf-8") as f:
#     article_titles = f.read().splitlines()

# # Create a dictionary to store Bengali Wikipedia page titles for each article
# article_pages = {}

# # Iterate over the article titles and get their corresponding Bengali Wikipedia pages through Wikidata
# for title in article_titles:
#     try:
#         page_en = pywikibot.Page(site_en, title)
#         item = pywikibot.ItemPage.fromPage(page_en)
#         item.get()
#         qid = item.id
#         page_bn = None
        
#         # Check if the item has a Bengali Wikipedia page connected through Wikidata
#         if "bnwiki" in item.sitelinks:
#             page_bn = pywikibot.Page(site_bn, item.sitelinks["bnwiki"].title)
            
#         article_pages[title] = page_bn.title() if page_bn else "No Bengali Wikipedia page found"
        
#     except pywikibot.exceptions.NoPageError:
#         article_pages[title] = "No Wikidata item found"

# # Write the output to a text file
# with open("data/ebn.txt", "w", encoding="utf-8") as f:
#     for title, page in article_pages.items():
#         line = f"{title} - {page}\n"
#         f.write(line)

import pywikibot
from tqdm import tqdm

# Set up the Wikipedia sites
site_en = pywikibot.Site("en", "wikipedia")
site_bn = pywikibot.Site("bn", "wikipedia")
repo = site_en.data_repository()

# Define the path to the text file containing the article titles
filename = "data/articles.txt"

# Read the article titles from the text file into a list
with open(filename, "r", encoding="utf-8") as f:
    article_titles = f.read().splitlines()

# Create a dictionary to store Bengali Wikipedia page titles for each article
article_pages = {}

# Iterate over the article titles and get their corresponding Bengali Wikipedia pages through Wikidata
for title in tqdm(article_titles, desc="Getting Bengali Wikipedia pages", unit="page"):
    try:
        page_en = pywikibot.Page(site_en, title)
        item = pywikibot.ItemPage.fromPage(page_en)
        item.get()
        qid = item.id
        page_bn = None
        
        # Check if the item has a Bengali Wikipedia page connected through Wikidata
        if "bnwiki" in item.sitelinks:
            page_bn = pywikibot.Page(site_bn, item.sitelinks["bnwiki"].title)
            
        article_pages[title] = page_bn.title() if page_bn else "No_BN"
        
    except pywikibot.exceptions.NoPageError:
        article_pages[title] = "No_WD"

# Write the output to a text file
with open("data/ebn.txt", "w", encoding="utf-8") as f:
    for title, page in tqdm(article_pages.items(), desc="Writing output to file", unit="page"):
        line = f"{title} - {page}\n"
        f.write(line)
