#!/usr/bin/env python3

import pywikibot
import argparse
import threading

def get_en_cats(page):
    site_en = pywikibot.Site('en', 'wikipedia')
    item = None
    
    try:
        item = pywikibot.ItemPage.fromPage(page)
        item.get()
    except pywikibot.exceptions.NoPageError:
        print(f"Error: No page found for '{page.title()}' on enwiki")

    if item and 'enwiki' in item.sitelinks:
        en_title = item.sitelinks['enwiki'].title
        en_page = pywikibot.Page(site_en, en_title)
        return [cat for cat in en_page.categories() if not cat.isHiddenCategory()]

    return []
    
def get_bn_cats(en_cats):
    site_bn = pywikibot.Site('bn', 'wikipedia')
    bn_cats = []

    for en_cat in en_cats:
        try:
            item = en_cat.data_item()
            item.get()
            
            if 'bnwiki' in item.sitelinks:
                bn_title = item.sitelinks['bnwiki'].title
                bn_cat = pywikibot.Page(site_bn, bn_title)
                bn_cats.append(bn_cat)
        except pywikibot.exceptions.NoPageError:
            pass

    return bn_cats

def add_bn_cats(page, bn_cats):
    existing_cats = page.categories()
    existing_cat_titles = {cat.title(with_ns=False) for cat in existing_cats}
    cats_to_add = [cat.title() for cat in bn_cats if cat.title(with_ns=False) not in existing_cat_titles]

    if cats_to_add:
        numerals = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
        bengali_length = ''.join(numerals[digit] for digit in str(len(cats_to_add)))
        cats_text = "\n".join(f"[[বিষয়শ্রেণী:{cat}]]" for cat in cats_to_add)
        page.text += "\n" + cats_text
        page.save(f" {bengali_length}টি বিষয়শ্রেণী যুক্ত করা হয়েছে", minor=False)
        print(f"+ Added {len(cats_to_add)} categories to {page.title()}")

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-file", dest="file_path", nargs='?', const="data/advoocats.txt", help="Path to the file containing page titles")
parser.add_argument("-cat", dest="category", help="Category name")
parser.add_argument("-depth", dest="depth", type=int, default=1, help="Category depth")
parser.add_argument("-recent", dest="recent", type=int, default=0, help="Number of recent pages")
parser.add_argument("-page", dest="page_title", help="Page title")
parser.add_argument("-template", dest="template", help="Template name")
args = parser.parse_args()

site_bn = pywikibot.Site('bn', 'wikipedia')

# Process based on command-line arguments
def process_page(bn_page, bn_cats):
    print(f"Processing page: {bn_page.title()}")
    thread = threading.Thread(target=add_bn_cats, args=(bn_page, bn_cats))
    thread.start()
def process_category(category, depth):
    print(f"Processing category: {category.title()}")
    pages = category.articles(namespaces=0, content=True, recurse=depth)
    for page in pages:
        bn_cats = get_bn_cats(get_en_cats(page))
        process_page(page, bn_cats)

if args.file_path:
    if not args.file_path.strip():
        args.file_path = "data/advoocats.txt"
    print(f"Processing {len(page_titles)} pages from file: {args.file_path}")
    with open(args.file_path, 'r', encoding='utf-8') as file:
        page_titles = file.read().splitlines()
    for page_title in page_titles:
        bn_page = pywikibot.Page(site_bn, page_title)
        en_cats = get_en_cats(bn_page)
        bn_cats = get_bn_cats(en_cats)
        process_page(bn_page, bn_cats)

elif args.category:
    category = pywikibot.Category(site_bn, args.category)
    depth = args.depth if args.depth <= 5 else 5
    process_category(category, depth)

elif args.recent:
    recent_pages = site_bn.recentchanges(total=args.recent)
    for rc in recent_pages:
        bn_page = pywikibot.Page(site_bn, rc['title'])
        bn_cats = get_bn_cats(get_en_cats(bn_page))
        process_page(bn_page, bn_cats)

elif args.page_title:
    bn_page = pywikibot.Page(site_bn, args.page_title)
    bn_cats = get_bn_cats(get_en_cats(bn_page))
    process_page(bn_page, bn_cats)

elif args.template:
    template = pywikibot.Page(site_bn, args.template, ns=10)
    transclusions = template.getReferences(only_template_inclusion=True, namespaces=0, total=args.recent)

    for bn_page in transclusions:
        bn_cats = get_bn_cats(get_en_cats(bn_page))
        process_page(bn_page, bn_cats)
else:
    print("No valid command-line arguments provided. Please check the options.")
