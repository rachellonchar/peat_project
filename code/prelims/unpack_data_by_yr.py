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

def extract_xl_BLF(special='', sheet_index=0, name_file='std (format: ~/xl/current_pyfile_name_output.xlsx)'):
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
        for col_idx in range(0, xl_sheet.ncols-2):
            ti = xl_sheet.cell(0, col_idx)
            titles.append(urlify(ti.value.strip(), '_'))
            uni = xl_sheet.cell(1, col_idx)
            units.append(urlify(uni.value.strip(), ' '))
        for col_idx in range(0, xl_sheet.ncols-2):
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

def yr_unwrap(years):
    list_data_names = ['Day of the year', 
        'Carbon dioxide', 'Methane', 'senH', 'LE', 'Air temperature', 'Soil temperature 10cm below the surface', 
        'Soil temperature 100cm below the surface', 'Water table depth', 'Relative heat', 'Precipitation']
    list_data_units = ['days','g/(m2 day)', 'g/(m2 day)', 'Wm2','Wm2','C','C','C','m','%', 'inches/day']
    list_abrevs = ['DoY', 'CO2', 'CH4', 'senH', 'LE', 'Tair', 'Ts10', 'Ts100', 'WT', 'RH', 'Prec']
    uncut, naming = {},{}
    tn,tu = {},{}
    for yr in years:
        cwd = os.getcwd()
        xl_file = cwd + '/xl/BLF_flux_data/BLF_daily_' + str(yr) +'.xlsx'
        #print(xl_file)
        arr, names, unis = extract_xl_BLF('', 0, xl_file)
        uncut_1y = {}
        for i in range(0, len(list_abrevs)):
            abvs = list_abrevs[i]
            dat = arr[i]
            uncut_1y.update({abvs:dat})
            if yr==years[0]:
                nam = list_data_names[i]
                uns = list_data_units[i]
                tn.update({abvs:nam})
                tu.update({abvs:uns})
        uncut.update({yr:uncut_1y})
    naming.update({'full titles':tn})
    naming.update({'units':tu})
    naming.update({'calls':list_abrevs})
    naming.update({'years':years})
    naming.update({'description':tn})
    return uncut, naming


def all_data_cleanup(uncut_dict,original_names_dict):
    uncut0 = uncut_dict
    naming = original_names_dict
    calls = naming['calls']
    years = naming['years']
    no_outliers, no_nan = {},{}
    for year in years:
        mark_for_removal = []
        uncut = uncut0[year]
        no_nan_yr = {}
        for call in calls:
            #eliminate nan values  -------------------------------------
            marked_indices = [idx for idx in range(0, len(uncut[call])) if (np.logical_not(np.isnan(uncut[call][idx]))==False)]#.all()]
            mark_for_removal = np.append(mark_for_removal,marked_indices)
            #-----------------------------------------------------------
        for call in calls:
            nonan = [uncut[call][idx] for idx in range(0, len(uncut[call])) if idx not in mark_for_removal]
            no_nan_yr.update({call:nonan})
        no_nan.update({year:no_nan_yr})
    for year in years:
        uncut = no_nan[year]
        Tair, Ts10 = uncut['Tair'], uncut['Ts10']
        no_outliers_yr = {}
        for call in calls:
            #outlier conditions ----------------------------------------
            cleann = uncut[call]
            cleann = [cleann[idx] for idx in range(0, len(cleann)) if Tair[idx]<21 or Tair[idx]>-21]
            cleann = [cleann[idx] for idx in range(0, len(cleann)) if Ts10[idx]>-0.1]
            #-----------------------------------------------------------
            no_outliers_yr.update({call:cleann[2:]})
        no_outliers.update({year:no_outliers_yr})
    return no_outliers, original_names_dict

def days_in(cut_dic,original_names_dict):
    naming = original_names_dict
    years = naming['years']
    DT = []
    for yy in range(0, len(years)):
        y_do = {}
        y = years[yy]
        DTy = [dd*(1+yy) for dd in cut_dic[y]['DoY']]
        DT = np.append(DT, DTy)
        cut_dic[y].update({'TotDays':DTy})
    naming['full titles'].update({'TotDays':'Total days into entire period'})
    naming['description'].update({'TotDays':'Total days into entire period (starting from year '+str(min(years))+')'})
    naming['units'].update({'TotDays':'days'})
    newc = np.append(naming['calls'],'TotDays')
    naming.update({'calls':newc})
    return cut_dic, naming

def rainfall_accumulation(cut_dic, original_names_dict):
    dic, naming = days_in(cut_dic,original_names_dict)
    years = naming['years']
    for year in years:
        rains,days = dic[year]['Prec'],dic[year]['DoY']
        cum_rain=0
        Rbar = np.mean(rains)
        A = np.zeros(len(days))
        for d in range(0,len(days)):
            rain,day = rains[d],days[d]
            cum_rain += rain
            A[d] = cum_rain - Rbar*day
        dic[year].update({'RainAccum':A})
    naming['full titles'].update({'RainAccum':'Rainfall accumulation index'})
    naming['description'].update({'RainAccum':'Deviation of precipitation from expected daily precipitation in a given year'})
    naming['units'].update({'RainAccum':'inches/day'})
    newc = np.append(naming['calls'],'RainAccum')
    naming.update({'calls':newc})
    return dic, naming

#all years we have data for:
years = [2010]
for i in range(0, 5):
    new = years[i]+1
    years.append(new)
years.append(2017)

#unwrap
uncut_data, toss = yr_unwrap(years)

#remove aoutliers and nan values
data_dict, original_naming = all_data_cleanup(uncut_data, toss)

#add days in, rainfall accumulation, and normalized variables
full_data, naming = rainfall_accumulation(data_dict, original_naming)

def save_only_needed(*args):
    #load data dictionaries:
    #sorting for relevent, possibly meaningful data
    rel = [a for a in args]
    rel_data, rel_names = {},{}
    years = naming['years']
    for y in years:
        rel_y={}
        for r in rel:
            dat = full_data[y][r]
            rel_y.update({r:dat})
        rel_data.update({y:rel_y})
    rel_names.update({'calls':rel})
    rel_names.update({'years':years})
    ff,dd,uu = {},{},{}
    for r in rel:
        ff.update({r:naming['full titles']})
        dd.update({r:naming['description']})
        uu.update({r:naming['units']})
    rel_names.update({'description':dd})
    rel_names.update({'full titles':ff})
    rel_names.update({'units':uu})
    #saving as the object 
    save_obj(full_data,'basic_parameters')
    save_obj(naming,'basic_naming')

save_only_needed('DoY', 'CO2', 'CH4', 'Tair' ,'Ts10' ,'Ts100' ,'WT', 'Prec',
    'TotDays','RainAccum')


