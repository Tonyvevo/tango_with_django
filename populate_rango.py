import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    # Lists of dictionaries containing pages to be
    # added to each category

    python_pages = [
        {"title":"Official Python Tutorial",
         "url":"http://docs.python.org/2/tutorial/",
         "views": 1024},
        {"title":"How to think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/",
         "views": 512},
        {"title":"Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/",
         "views": 64}
        ]

    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": 768},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/",
         "views": 256}
        ]

    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/",
         "views": 8},
        {"title":"Flask",
         "url":"http://flask.pocoo.org",
         "views": 32}
        ]

    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/",
         "views": 8},
        {"title":"Flask",
         "url":"http://flask.pocoo.org",
         "views": 32}
        ]

    pascal_pages = [
        {"title":"Pascal tutorial for beginners",
         "url":"http://www.pascal-programming.info/index.php",
         "views": 4},
        {"title":"Free Pascal",
         "url":"http://www.freepascal.org/advantage.var",
         "views": 6}
        ]

    prolog_pages = [
        {"title":"SWI-Prolog",
         "url":"http://www.swi-prolog.org/",
         "views": 16},
        {"title":"Visual Prolog",
         "url":"http://www.visual-prolog.com/default.htm",
         "views": 12}
        ]

    postscript_pages = [
        {"title":"Postscript Tutorial",
         "url":"http://paulbourke.net/dataformats/postscript/",
         "views": 78},
        {"title":"Adobe Postscript",
         "url":"http://www.adobe.com/products/postscript.html",
         "views": 32}
        ]

    php_pages = [
        {"title":"PHP",
         "url":"http://php.net/",
         "views": 291},
        {"title":"PHP Tutorial",
         "url":"http://www.w3schools.com/php/",
         "views": 60}
        ]

    programming_pages = [
        {"title":"Programming - Wikipedia",
         "url":"http://en.wikipedia.org/wiki/Programming/",
         "views": 512},
        ]

    perl_pages = [
        {"title":"The perl programming language",
         "url":"http://www.perl.org/",
         "views": 8},
        ]

    # Dictionary of dictionaries for our categories

    cats = {"Python": {"pages": python_pages,
                       "views": 128,
                       "likes": 64},
            "Django": {"pages": django_pages,
                       "views": 64,
                       "likes": 32},
            "Other Frameworks": {"pages": other_pages,
                                 "views": 32,
                                 "likes": 16},
            "Pascal": {"pages": pascal_pages,
                       "views": 8,
                       "likes": 4},
            "Prolog": {"pages": prolog_pages,
                       "views": 4,
                       "likes": 2},
            "Perl": {"pages": perl_pages,
                     "views": 48,
                     "likes": 5},
            "PHP": {"pages": php_pages,
                    "views": 256,
                    "likes": 128},
            "PostScript": {"pages": postscript_pages,
                           "views": 32,
                           "likes": 8},
            "Programming": {"pages": programming_pages,
                            "views": 2048,
                            "likes": 1024}
            }

    # Iterate through the cats dictionary adding each category,
    # and then add the pages associated to that category

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # Print out the categories we have added

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
    
