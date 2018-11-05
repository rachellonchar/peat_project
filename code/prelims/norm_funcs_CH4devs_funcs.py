#import numpy as np
#import matplotlib.pyplot as plt
#import sys    
#import os
#import xlwt
#import xlrd
#import pandas as pd
#from xlrd.sheet import ctype_text 
#import pickle

#from save_funcs import *
#import sklearn.linear_model
#regr = sklearn.linear_model.LinearRegression()
#from scipy.optimize import curve_fit
#import operator
#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------
import basic_fit_funcs as btf

def normalize_series(series):#,preserve_negativity=0,maxx=None, minn=None,
    mn,mx = min(series),max(series)
    overall_mx = max(abs(mx),abs(mn))
    def funorm(val): return val/overall_mx
    new = [funorm(s) for s in series]
    return new
def normalize_annual(param,dic,naming):
    holdD,hold_all = {},[]
    for year in naming['years']:
        if year!='all':
            series = dic[param][year]
            nseries = normalize_series(series)
            holdD.update({year:nseries})
            hold_all = np.append(hold_all,nseries)
    holdD.update({'all':hold_all})
    dic.update({'N'+param:holdD})
    calls = naming['calls']
    calls = np.append(calls,'N'+param)
    naming.update({'calls':calls})
    naming['full calls'].update({'N'+param:naming['full calls'][param]+' (normalized)'})
    naming['units'].update({'N'+param:''})
    return dic,naming
    
def add_CH4_devs(dic,naming,param1='NTs10',param2='CH4_S1',fit_type=btf.func_exp):
#def normalize_annual(param,dic,naming):
    holdD1,hold_all1 = {},[]
    holdD2,hold_all2 = {},[]
    holdD3,hold_all3 = {},[]
    for year in naming['years']:
        series1,series2 = dic[param1][year],dic[param2][year]
        dev_dic = btf.deviations_from_fit(series1,series2,fit_type=fit_type,mask=None,
            clipped=0,clipped_devs=0)
            
        holdD1.update({year:dev_dic['Yexp']})
        holdD2.update({year:dev_dic['log Yexp']})
        holdD3.update({year:dev_dic['deviations']})
        #if year in [2009,2010,2011,2012,2013,2014,2015,20170]:
            #hold_all1 = np.append(hold_all1,dev_dic['Yexp'])
            #hold_all2 = np.append(hold_all2,dev_dic['log Yexp'])
            #hold_all3 = np.append(hold_all3,dev_dic['deviations'])
            
    #holdD1.update({'all':hold_all1})
    #holdD2.update({'all':hold_all2})
    #holdD3.update({'all':hold_all3})
    
    dic.update({'exp '+param2:{param1:holdD1}})
    dic.update({'exp log '+param2:{param1:holdD2}})
    dic.update({'dev '+param2:{param1:holdD3}})
    
    calls = naming['calls']
    calls = np.append(calls,['exp '+param2,'exp log '+param2,'dev '+param2])
    naming.update({'calls':calls})
    naming['full calls'].update({'exp '+param2:naming['full calls'][param2]+' (expected)'})
    naming['full calls'].update({'exp log '+param2:naming['full calls'][param2]+' (expected log transform)'})
    naming['full calls'].update({'dev '+param2:naming['full calls'][param2]+' (deviations from expected)'})
    naming['units'].update({'exp '+param2:naming['units'][param2]})
    naming['units'].update({'exp log '+param2:'[log '+naming['units'][param2][1:]})
    naming['units'].update({'dev '+param2:naming['units'][param2]})
    return dic,naming



    
    
    
    
    
    
    
    
    
    
    
    
