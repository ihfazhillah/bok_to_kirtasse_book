import csv
import subprocess
from collections import namedtuple
import os


ENV = {'MDB_JET3_CHARSET':'cp1256'}
MAIN = "Main"
TITLE = "t{bkid}"
BOOK = "b{bkid}"
BOOKDIR = "bk{bkid}"

def convert_table_to_csv(fname, table_name, target_path='main.csv'):
    command = ['mdb-export', '-d|', fname, table_name]
    with open(target_path, "w") as f:
        subprocess.Popen(command, stdout=f, env=ENV).communicate()

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

if __name__ == '__main__':
    csv_file = convert_table_to_csv("jami.bok", MAIN)
    csv_obj = read_csv("main.csv")
    make_bookinfo_xml(main_parser(csv_obj))
