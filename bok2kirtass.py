import csv
import subprocess
import tempfile

ENV = {'MDB_JET3_CHARSET':'cp1256'}

def convert_main_table_to_csv(fname):
    command = ['mdb-export', '-d"|*|"', "-Q", fname, 'Main']
    temp = tempfile.TemporaryFile("w+t")
    subprocess.Popen(command, stdout=temp, env=ENV).communicate()
    return temp

if __name__ == '__main__':
    csv_file = convert_main_table_to_csv("jami.bok")
    csv_file.seek(0)
    for x in csv_file:
        print(x.rstrip())
