
import scipy.special
import scipy.integrate 
from scipy.integrate import quad
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import sys    
import os
import xlwt
import xlrd
import pandas as pd
from xlrd.sheet import ctype_text 
import pickle
import sklearn.linear_model
regr = sklearn.linear_model.LinearRegression()
from scipy.optimize import curve_fit, fsolve
import operator
import scipy.stats
#from scipy.stats import norm
from numpy import linspace
from pylab import plot,show,hist,figure,title
import matplotlib
import matplotlib.cm as cm
import math
from scipy.signal import argrelextrema, savgol_filter

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

#unzipping dictionary contents 
def unzip_dict(dictionary):
    keys = []
    values = []
    for k, v in dictionary[soil_type].items():
        keys.append(k)
        values.append(v)
    for var in zip(keys, values):
        exec( "%s=%s" % (var[0], var[1]))

#extract lines of a tex file as an array of numbers and strings
def extract_lines(tex_file_name):
    lines = [] #Declare an empty list named "lines"
    with open (tex_file_name, 'rt') as in_file: 
        for line in in_file: 
            try:
                el = float(line.strip())
            except ValueError:
                el = line.strip()
            lines.append(el)
    return lines

import sys    
import os
import xlwt
import xlrd
import pandas as pd

def xl_output(array_names, array_values, special='', overwrite=0, sheet_name='output_sheet'): #values will typically be arrays themselves
    #create the tex file and place it in a logical area relative to the main script:
    cwd = os.getcwd()
    file_n =  os.path.basename(sys.argv[0])
    if special == '':
        xl_file = cwd + '/xl/' + file_n[:-3] +'_output.xlsx'
    else:
        xl_file = cwd + '/xl/' + file_n[:-3] +'_output_' + special + '.xlsx'
    #doesn't create if file already exists 
    if os.path.isfile(xl_file):
        None
    else:
        os.mknod(xl_file) 
    #does file already have data?
    if overwrite == 0: #do NOT overwite 
        df = pd.read_excel(xl_file) # or
        if df.empty:
            #write data to file
            cols = len(array_names)
            book = xlwt.Workbook()
            #sh = book.add_sheet(sheet)
            sh = book.add_sheet(sheet_name)
            for i in range(0, cols):
                sh.write(0, i, array_names[i])
                data_col = array_values[i]
                for j in range(0, len(data_col)):
                    sh.write(j+1, i, data_col[j])
            book.save(xl_file)
        else:
            print('File nonempty. To write over the current file, specify overwrite=1 while calling the function.')
    else: #directly rewite, no checking to see if empty
        #write data to file
        cols = len(array_names)
        book = xlwt.Workbook()
        #sh = book.add_sheet(sheet)
        sh = book.add_sheet(sheet_name)
        for i in range(0, cols):
            sh.write(0, i, array_names[i])
            data_col = array_values[i]
            for j in range(0, len(data_col)):
                sh.write(j+1, i, data_col[j])
        book.save(xl_file)

from xlrd.sheet import ctype_text 
#extract excel information and convert to python object
#UNPACKING 
def extract_xl(special='', sheet_index=0, name_file='std (format: ~/xl/current_pyfile_name_output.xlsx)'):
    if name_file == 'std (format: ~/xl/current_pyfile_name_output.xlsx)':
        cwd = os.getcwd()
        file_n =  os.path.basename(sys.argv[0])
        if (special == '') or (special == None):
            xl_file = cwd + '/xl/' + file_n[:-3] +'_output.xlsx'
        else:
            xl_file = cwd + '/xl/' + file_n[:-3] +'_output_' + special + '.xlsx'
    else:
        xl_file = name_file
    if os.path.isfile(xl_file): #file exists so we can extract its contents 
        workbook1 = xlrd.open_workbook(xl_file)
        xl_sheet = workbook1.sheet_by_index(sheet_index)
        # Iterate through rows, and print out the column values
        row_vals = []
        for row_idx in range(0, xl_sheet.nrows):
            for col_idx in range(0, xl_sheet.ncols):
                cell_obj = xl_sheet.cell(row_idx, col_idx)
                cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
                print ('(row %s) %s (type:%s)' % (row_idx, cell_obj.value, cell_type_str))
                row_vals.append(cell_obj.value)
        # Retrieve non-empty rows
        nonempty_row_vals = [x for x in row_vals if x]    
        num_rows_missing_vals = xl_sheet.nrows - len(nonempty_row_vals)
        print ('Vals: %d; Rows Missing Vals: %d' % (len(nonempty_row_vals), num_rows_missing_vals))
    else:
        print('This file does not exist---no content to extract.')
        
##unzip dictionary contents template:

#specify_dic = ...
##----
#keys, values = [],[]
#for k, v in specify_dic.items():
    #keys.append(k)
    #values.append(v)
#for var in zip(keys, values):
    #exec( "%s=%s" % (var[0], var[1]))

