import csv
import subprocess

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


if __name__ == '__main__':
    csv_file = convert_main_table_to_csv("jami.bok")
    readed = read_csv("main.csv")
    for x in readed:
        print(x["Betaka"])
