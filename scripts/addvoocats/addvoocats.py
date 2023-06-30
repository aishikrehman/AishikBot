import pywikibot
from pywikibot import pagegenerators
from pywikibot.bot import suggest_help
from pywikibot import i18n

def main(*args: str) -> None:
    local_args = pywikibot.handle_args(args)
    onwiki = pywikibot.Site()
    fromwiki_family = onwiki.family.name
    fromwiki_lang = 'en'
    gen_args = []

    for arg in local_args:
        if arg.startswith('-fromlang'):
            fromwiki_lang = arg[len('-fromlang:'):]
        else:
            gen_args.append(arg)
    
    fromwiki = pywikibot.Site(fromwiki_lang, fromwiki_family)
    same_host_error = 'Source wiki not different from OnWiki!' if fromwiki == onwiki else ''

    gen_factory = pagegenerators.GeneratorFactory(site=onwiki)
    unknown_args = [arg for arg in gen_args if not gen_factory.handle_arg(arg)]
    gen = gen_factory.getCombinedGenerator(preload=True)

    if suggest_help(missing_generator=not gen, additional_text=same_host_error, unknown_parameters=unknown_args):
        return
    
    pywikibot.output("""
    ADDVOOCATS.PY configuration
    ---------------------------
    Source: {fromwiki}
    Working on: {onwiki}

    Generator of pages to voocate: {gen_args}
    """.format(fromwiki=fromwiki, onwiki=onwiki, gen_args=gen_args))

    for page in gen:
        pywikibot.output(f"=> Processing page: {page.title()}")
        try:
            item = pywikibot.ItemPage.fromPage(page)
            item.get()
        except pywikibot.exceptions.NoPageError:
            pywikibot.output(f"Page skipped: No item found for page {page.title()}")
            continue

        fromwiki_sitelink = item.sitelinks.get(fromwiki.dbName())
        fromwiki_page_title = fromwiki_sitelink.title if hasattr(fromwiki_sitelink, 'title') else None
        if not fromwiki_page_title:
            pywikibot.output(f"Page skipped: No title found for sitelink {fromwiki_sitelink}")
            continue
        pywikibot.output(f"Source wiki page: {fromwiki_page_title}")

        fromwiki_page = pywikibot.Page(fromwiki, fromwiki_page_title)
        fromwiki_categories = [cat for cat in fromwiki_page.categories() if not cat.isHiddenCategory()]
        # pywikibot.output(f"Categories found on Source Wiki: {fromwiki_categories}")

        onwiki_categories = []
        for fromwiki_cat in fromwiki_categories:
            try:
                onwiki_dbname = onwiki.dbName()
                item = fromwiki_cat.data_item()
                item.get()
                if onwiki_dbname in item.sitelinks:
                    onwiki_cats_title = item.sitelinks[onwiki_dbname].title
                    onwiki_category = pywikibot.Page(onwiki, onwiki_cats_title)
                    onwiki_categories.append(onwiki_category)
            except pywikibot.exceptions.NoPageError:
                pass
        # pywikibot.output(f"Corresponding categories found on OnWiki: {onwiki_categories}")

        onwiki_existing_categories = page.categories()
        onwiki_existing_category_titles = {cat.title(with_ns=False) for cat in onwiki_existing_categories}
        onwiki_categories_to_add = [cat.title() for cat in onwiki_categories if cat.title(with_ns=False) not in onwiki_existing_category_titles]
        
        if onwiki_categories_to_add:
            pywikibot.output("Adding categories.....")
            categories_text = "\n".join(f"[[{onwiki.namespace(14)}:{cat}]]" for cat in onwiki_categories_to_add)
            page.text += "\n" + categories_text
            bengali_numerals = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
            bengali_length = ''.join(bengali_numerals[digit] for digit in str(len(onwiki_categories_to_add)))
            summary = i18n.twtranslate(onwiki, 'addvoocats-summary').format(num=bengali_length if onwiki.lang == 'bn' else len(onwiki_categories_to_add))
            page.save(summary=summary)
            pywikibot.output(f"Added {len(onwiki_categories_to_add)} categories to {page.title()}")
        else:
            pywikibot.output("Page Skipped: No categories to add (!)")

if __name__ == '__main__':
    main()
