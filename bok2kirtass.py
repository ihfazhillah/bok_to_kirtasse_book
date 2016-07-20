import csv
import subprocess
from collections import namedtuple
import os
from jinja2 import Template


ENV = {'MDB_JET3_CHARSET':'cp1256'}
MAIN = "Main"
TITLE = "t{bkid}"
BOOK = "b{bkid}"
BOOKDIR = "bk{bkid}"
# shorts
std_shorts={
    u'A': u'صلى الله عليه وسلم',
    u'B': u'رضي الله عن',
    u'C': u'رحمه الله',
    u'D': u'عز وجل',
    u'E': u'عليه الصلاة و السلام',
}

title_template = Template(
"""
<?xml version="1.0" encoding="UTF-8"?>
<dataroot>
    {% for title in titles %}
    <title>
        <tit>{{title.tit}}</tit>
        <lvl>{{title.lvl}}</lvl>
        <id>{{title.id}}</id>
    </title>
    {% endfor %}
</dataroot>
""".strip()
)

book_template = Template("""
<?xml version="1.0" encoding="UTF-8"?>
<dataroot>
    {% for book in books %}
    <book>
        <nass>{{book.nass}}</nass>
        <part>{{book.part}}</part>
        <seal>{{book.seal}}</seal>
        <id>{{book.id}}</id>
        <page>{{book.page}}</page>
    </book>
    {% endfor %}
</dataroot>
""".strip())


def convert_table_to_csv(fname, table_name, target_path):
    command = ['mdb-export', '-d|', fname, table_name]
    with open(target_path, "w") as f:
        subprocess.Popen(command, stdout=f, env=ENV).communicate()


def main2csv(fname):
    convert_table_to_csv(fname, MAIN, "main.csv")

def title2csv(fname, main_object):
    bkid = main_object.bkid
    folder = BOOKDIR.format(bkid=bkid)
    convert_table_to_csv(fname, TITLE.format(bkid=bkid), folder+"/title.csv")


def book2csv(fname, main_object):
    bkid = main_object.bkid
    folder = BOOKDIR.format(bkid=bkid)
    convert_table_to_csv(fname, BOOK.format(bkid=bkid), folder+"/book.csv")


def read_csv(fileobj):
    f = open(fileobj, "r")
    csv.register_dialect("kirtass", delimiter="|")
    reader = csv.DictReader(f, dialect='kirtass')
    return reader

def main_parser(csv_obj):
    for row in csv_obj:
        bk_id = row.get('BkId')
        title = row.get('Bk')
        betaka = row.get('Betaka')
        author = row.get('Auth')
        category = row.get('cat')
    bookinfo = namedtuple("BookInfo", ["bkid", "title",
                        "betaka", "author", "cat"])
    try:
        os.mkdir(BOOKDIR.format(bkid=bk_id))
    except:
        pass

    return bookinfo(bk_id, title, betaka, author, category)

def make_bookinfo_xml(main_object):
    template = """
<?xml version='1.0' encoding='UTF-8'?>
<dataroot>
<groupe title="{title}" betaka="{betaka}" author="{author}"/>
</dataroot>""".strip()
    bookinfo = template.format(title=main_object.title,
                           betaka=main_object.betaka.replace("\n", "&#xa;"),
                           author=main_object.author)
    with open(BOOKDIR.format(bkid=main_object.bkid)+"/bookinfo.info", "w") as f:
        f.write(bookinfo)

def titles_parser(main_object, title_object):
    titles = []
    title = namedtuple('title', ['tit', 'lvl', 'id'])
    for x in title_object:
        tit = x['tit']
        lvl = x['lvl']
        id_ = x['id']
        titles.append(title(tit, lvl, id_))
    return titles


def book_parser(book_object):
    books = []
    book = namedtuple("book", ["nass", "part", "seal", "id", "page"])
    for x in book_object:
        nass = x['nass']
        part = x['part']
        seal = x['seal']
        id_ = x['id']
        page = x['page']

        import re
        nass = re.sub("\n", "\n\n", nass)
        nass = re.sub("\n\nA", "\n\nالجواب", nass)
        for key in std_shorts:
            nass = nass.replace(key, std_shorts[key])

        # print(help(nass))

        books.append(book(nass, part, seal, id_, page))

    return books

def make_title_xml(main_object, title_object):
    title_string = title_template.render(titles=title_object)
    with open(BOOKDIR.format(bkid=main_object.bkid)+"/title.xml", "w") as f:
        f.write(title_string)

def make_book_xml(main_object, book_object):
    title_string = book_template.render(books=book_object)
    with open(BOOKDIR.format(bkid=main_object.bkid)+"/book.xml", "w") as f:
        f.write(title_string)

if __name__ == '__main__':
    main2csv("jami.bok")
    main = main_parser(read_csv("main.csv"))
    book2csv("jami.bok", main)
    book = read_csv(BOOKDIR.format(bkid=main.bkid)+"/book.csv")
    book_ = book_parser(book)
    make_book_xml(main, book_)
    #make_bookinfo_xml(main_parser(csv_obj))
    # titles = titles_parser(main, csv_obj)
    # for x in titles:
    #     print(x)
    # make_title_xml(main, titles)
