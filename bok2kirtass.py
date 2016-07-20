import csv
import subprocess
from collections import namedtuple


ENV = {'MDB_JET3_CHARSET':'cp1256'}


def convert_main_table_to_csv(fname):
    command = ['mdb-export', '-d|', fname, 'Main']
    with open("main.csv", "w") as f:
        subprocess.Popen(command, stdout=f, env=ENV).communicate()
        return f

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
    with open("bookinfo.info", "w") as f:
        f.write(bookinfo)

if __name__ == '__main__':
    csv_file = convert_main_table_to_csv("jami.bok")
    csv_obj = read_csv("main.csv")
    make_bookinfo_xml(main_parser(csv_obj))
