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

#def save_only_needed(*args):
    ##sorting for relevent, possibly meaningful data
    #v_,n_ = weed_and_merge(*args)#,dic=v09,naming=n09)
    #v,n = add_all(v_,n_)
    
    ##saving as the object 
    #save_obj(v,'hold_parameters')
    #save_obj(n,'hold_naming')
    
    
#save_only_needed('DoY', 'NEE', 'CH4', 'Tair' ,'Ts10' ,'Ts100' ,'WTa', 'Prec',
    #'TotDays','RainAccum')

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


#def add_CH4_devs(param1,param2,dic,naming):
    
    
    
    
    
    
    
    
    
    
    
    
