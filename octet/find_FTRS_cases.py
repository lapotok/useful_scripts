import os
import re
import datetime
import xlsxwriter
from bs4 import BeautifulSoup as bs 

wb = xlsxwriter.Workbook('experiment_list_auto.xlsx')
ws = wb.add_worksheet()

bold = wb.add_format({'bold': True})
red = wb.add_format({'font_color': 'red'})

ws.write(0, 0, 'Date', bold)
ws.set_column(0, 0, 15)

ws.write(0, 1, 'Folder', bold)
ws.set_column(1, 1, 70)

ws.write(0, 2, 'SensorCols', bold)
ws.set_column(2, 2, 25)

ws.write(0, 3, 'SampleCols', bold)
ws.set_column(3, 3, 20)

ws.write(0, 4, 'Error', bold)
ws.set_column(4, 4, 50)

row_ix = 1
for root, dirs, files in os.walk("."):
    for i in range(len(files)):
        if re.search("OctetExperiment\.log$", files[i]):
            logfilename = f'{root}/{files[i]}'
            dirname = os.path.dirname(logfilename)
            print(dirname)
            fmf_filename = list(filter(lambda x: re.search("\.fmf$", x), os.listdir(dirname)))[0]
            cdatetime = datetime.datetime.fromtimestamp(os.stat(logfilename).st_mtime).strftime("%Y-%m-%d %H:%M")
            ws.write(row_ix, 0, cdatetime)
            ws.write(row_ix, 1, dirname)
            fmf = bs(open(f'{dirname}/{fmf_filename}', "r").read(), "lxml")
            ws.write(row_ix, 2, ",".join(sorted(set([el.find("sensorloc").text[1:] for el in fmf.find_all("sensordata") if el.find("sensortype").text != "" and el.find("sensorloc").text[1:]]), key=lambda x: int(x))))
            ws.write(row_ix, 3, ",".join(sorted(set([el.text[1:] for el in fmf.find_all("sampleloc") if len(el.text)>1]), key=lambda x: int(x))))

            m = re.search("[^\n]*failed to read spectra[^\n]*", open(logfilename, "r").read() , re.MULTILINE|re.IGNORECASE)
            if m:
                ws.write(row_ix, 4, m.group().replace("\t", "  "), red)
            row_ix += 1

wb.close()

