import numpy as np
import matplotlib.pyplot as plt
import sys    
import os
import xlwt
import xlrd
import pandas as pd
from xlrd.sheet import ctype_text 
import pickle
from helpful_functions import extract_xl, urlify, save_obj, load_obj
import sklearn.linear_model
regr = sklearn.linear_model.LinearRegression()
from scipy.optimize import curve_fit
import operator

def extract_xl_BLF(special='', sheet_index=0, name_file='std (format: ~/xl/current_pyfile_name_output.xlsx)',all_cols=2):
    titles = []
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
        array = []
        titles = []
        units = []
        for col_idx in range(0, xl_sheet.ncols-all_cols):
            ti = xl_sheet.cell(0, col_idx)
            titles.append(urlify(ti.value.strip(), '_'))
            uni = xl_sheet.cell(1, col_idx)
            units.append(urlify(uni.value.strip(), ' '))
        for col_idx in range(0, xl_sheet.ncols-all_cols):
            vector_vals = np.zeros(xl_sheet.nrows)
            for row_idx in range(2, xl_sheet.nrows):
                cel = xl_sheet.cell(row_idx, col_idx)
                try:
                    vector_vals[row_idx] = cel.value
                except ValueError:
                    vector_vals[row_idx] = cel
            array.append(vector_vals)
        return array, titles, units
    else:
        print('This file does not exist---no content to extract.')

def unwrap1518():
    list_data_names = ['ID Date', 
        'Carbon dioxide', 'Methane S1','Methane', 'senH', 'LE', 'Air temperature', 'Soil temperature 5cm below the surface', 
        'Soil temperature 10cm below the surface', 'Soil temperature 20cm below the surface', 
        'Soil temperature 30cm below the surface', 'Soil temperature 40cm below the surface', 
        'Soil temperature 50cm below the surface', 'Soil temperature 100cm below the surface', 
        'Soil temperature 200cm below the surface', 'Water table depth', 'Relative heat', 'Precipitation']
    list_data_units = ['days','g/(m2 day)','g/(m2 day)', 'g/(m2 day)', 'Wm2','Wm2','C','C','C',
        'C','C','C','C','C','C','m','%', 'inches/day']
    list_abrevs = ['ID', 'NEE','CH4_S1', 'CH4_S2', 'senH', 'LE', 'Tair', 'Ts5','Ts10',
        'Ts20','Ts30','Ts40','Ts50','Ts100', 'Ts200', 'WT', 'RH', 'Prec']
    uncut, naming = {},{}
    tn,tu = {},{}
    cwd = os.getcwd()
    xl_file = cwd + '/xl/BLF_flux_data/BLF_daily_2015-2018' +'.xlsx'
    arr, names, unis = extract_xl_BLF('', 0, xl_file,all_cols=1)
    for i in range(0, len(list_abrevs)):
        abvs = list_abrevs[i]
        dat = arr[i]
        uncut.update({abvs:dat[2:]})
        nam = list_data_names[i]
        uns = list_data_units[i]
        tn.update({abvs:nam})
        tu.update({abvs:uns})
    naming.update({'full names':tn})
    naming.update({'units':tu})
    naming.update({'calls':list_abrevs})
    #naming.update({'years':'2015-2018'})
    return uncut, naming
uc,nam = unwrap1518()

def days_in(dic,original_names_dict):
    naming = original_names_dict
    Tott = [i for i in range(1,len(dic['ID'])+1)]
    yr1 = [i for i in range(1,366)]
    yr_leap = [i for i in range(1,367)]
    yrs = np.append(yr1,yr_leap) #2016 was leap year
    for i in range(0,3):
        yrs = np.append(yrs,yr1)
    DoY = [yrs[i] for i in range(0,len(dic['ID']))]
    years = [2015,2016,2017,2018]
    yr_marks = {}
    s,f = 0,365
    for y in years:
        yr_marks.update({y:[s,f]})
        pls=366 if y==2016 else 365
        plf=366 if y==2015 else 365
        s+=pls
        f+=plf
    #markers = [0,365,365+366]
    dic.update({'year marks':yr_marks})
    naming.update({'years':years})
    dic.update({'TotDays':Tott})
    naming['full names'].update({'TotDays':'Total days in'})
    naming['units'].update({'TotDays':'days'})
    newc = np.append(naming['calls'],'TotDays')
    naming.update({'calls':newc})
    dic.update({'DoY':DoY})
    naming['full names'].update({'DoY':'Day of the year'})
    naming['units'].update({'DoY':'days'})
    newc = np.append(naming['calls'],'DoY')
    naming.update({'calls':newc})
    return dic, naming
days_in(uc,nam)

def rainfall_accumulation(dic, naming):
    years = naming['years']
    all_A = []
    for year in years:
        s,f = dic['year marks'][year][0],dic['year marks'][year][1]
        rains,days = dic['Prec'][s:f],dic['DoY'][s:f]
        cum_rain=0
        Rbar = np.mean(rains)
        A = np.zeros(len(days))
        for d in range(0,len(days)):
            rain,day = rains[d],days[d]
            cum_rain += rain
            A[d] = cum_rain - Rbar*day
        all_A = np.append(all_A,A)
    dic.update({'RainAccum':all_A})
    naming['full names'].update({'RainAccum':'Rainfall accumulation index'})
    #naming['description'].update({'RainAccum':'Deviation of precipitation from expected daily precipitation in a given year'})
    naming['units'].update({'RainAccum':'inches/day'})
    newc = np.append(naming['calls'],'RainAccum')
    naming.update({'calls':newc})
    return dic, naming
rainfall_accumulation(uc,nam)

def avg_CH(dic,naming):
    s1, s2 = dic['CH4_S1'],dic['CH4_S2']
    avg = [(s1[i]+s2[i])/2 for i in range(0, len(s1))]
    dic.update({'CH4':avg})
    naming['full names'].update({'CH4':'Average methane reading'})
    naming['units'].update({'CH4':'g/(m2 day)'})
    newc = np.append(naming['calls'],'CH4')
    naming.update({'calls':newc})
    return dic, naming
avg_CH(uc,nam)


save_obj(uc,'new_parameters')
save_obj(nam,'new_naming')
