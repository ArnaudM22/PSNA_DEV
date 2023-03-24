# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:09:56 2022

@author: feimeng.wu
"""

from pathlib import Path
import openpyxl
import os
 
# get files
os.chdir(os.path.abspath(os.path.dirname(__file__)))
pdir = Path('C:/Users/arnaud.maupas/Downloads/Nouveau_rhesus/Nouveau_rhesus/Rhesus_2021')
filelist = [filename for filename in pdir.iterdir() if filename.suffix == '.xlsx']
 
for filename in filelist:
    print(filename.name)
 
for infile in filelist:
    workbook = openpyxl.load_workbook(infile)
    outfile = f"{infile.name.split('.')[0]}.xls"
    workbook.save(outfile)