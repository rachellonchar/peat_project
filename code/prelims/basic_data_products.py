import numpy as np
import matplotlib.pyplot as plt
import sys    
import os
import xlwt
import xlrd
import pandas as pd
from xlrd.sheet import ctype_text 
import pickle

from save_funcs import *
import sklearn.linear_model
regr = sklearn.linear_model.LinearRegression()
from scipy.optimize import curve_fit
import operator

Dv,Dn = {},{}
ay = []
for nn in range(9,19):
    ay.append(2000+nn)
    
    
def emp(param='',no_warn=1):
    if no_warn==0:
        print('warning: no data for parameter, '+param)
        print('check to make sure you made the call and/or years correct')
        print('check to make sure correct v,n dictionaries being called (defaults are empty)')

def stitcher(param='Prec',years=ay,v=Dv,n=Dn,ret='all'):
    hold,nosuch = [],[]
    for yr in years:
        try:
            hold = np.append(hold, v[yr][param])
        except:
            nosuch.append(yr) #years for which parameter data is unavailable 
    emp(param,len(hold))
    if type(n)==dict:
        unit, modf = n['units'][param],''
    else:
        unit, modf = n[0],n[1]
    if ret=='hold':
        return hold
    else:
        return nosuch, hold, modf, unit

#functions to define more as needed 
def accum(param='Prec',years=ay,v=Dv,n=Dn):
    dic, naming = v,n
    holdD,nosuch = {},[]
    ct = 0
    for year in years:
        try:
            rains,days = dic[year][param],dic[year]['DoY']
            cum_rain=0
            Rbar = np.mean(rains)
            A = np.zeros(len(days))
            for d in range(0,len(days)):
                rain,day = rains[d],days[d]
                cum_rain += rain
                A[d] = cum_rain - Rbar*day
            holdD.update({year:A})
            ct += 1
        except:
            nosuch.append(year)
    emp(param,ct)
    unit,modf = '','accumulation, normalized to annual total cumulation'
    return nosuch,holdD,modf,unit
    
def normalize_series(series):#,preserve_negativity=0,maxx=None, minn=None,
    mn,mx = min(series),max(series)
    overall_mx = max(abs(mx),abs(mn))
    def funorm(val): return val/overall_mx
    new = [funorm(s) for s in series]
    return new
def normalize_annual(param='Prec',years=ay,v=Dv,n=Dn):
    holdD,nosuch = {},[]
    ct = 0
    for year in years:
        try:
            series = v[year][param]
            holdD.update({year:normalize_series(series)})
            ct += 1
        except:
            nosuch.append(year)
    emp(param,ct)
    unit,modf = '','(normalized by annual max)'
    return nosuch,holdD,modf,unit

thres_run={}
def threshold_mask(threshold=0,param='WT',years=ay,v=Dv,n=Dn):
    holdD, nosuch = {},[]
    ct = 0
    not_winter=True
    pDa,pDi,tDa,tDi,ma,mi = {},{},{},{},{},{}
    for year in years:
        try:
            series = v[year][param]
            PoI,PoA = np.zeros_like(series),np.zeros_like(series)
            mask_above,mask_below = np.zeros_like(series),np.zeros_like(series)
            permA,permI = [],[]
            below, above = 0,0
            for idx in range(0, len(series)):
                pt = series[idx]
                #winter condition:
                if v[year]['Tsoil_10cm'][idx]<0:
                    #winter...ground too frozen - always mask this
                    below, above = 0,0
                    if not_winter:
                        not_winter=False
                else:
                    if v[year]['Tsoil_10cm'][idx-1]>1:
                        not_winter=True
                if pt>threshold: # inundated
                    if series[idx-1]<=threshold:
                        permI.append(above)
                        above = 0
                    mask_above[idx] = 1 # masks the inundated pt
                    above += 1
                    PoI[idx],PoA[idx] = above,0
                else: #aerated
                    if series[idx-1]>threshold:
                        permA.append(below)
                        below = 0
                    mask_below[idx] = 1 # masks the aerated pt
                    below += 1
                    PoI[idx],PoA[idx] = 0,below
                modfD = {'PoI':'period of inundation','PoA':'period of aeration',
                    'tA':'permanence time in aerated state',
                    'tI':'permanence time in inundated state',
                    'mA':'mask aerated states','mI':'mask inundated states'}
                pDa.update({year:PoA})
                pDi.update({year:PoI})
                tDa.update({year:permA})
                tDi.update({year:permI})
                ma.update({year:mask_below})
                mi.update({year:mask_above})
                ct+=1
        except:
            nosuch.append(year)
    holdD = {'PoI':pDi,'PoA':pDa,'tA':tDa,'tI':tDi,'mA':ma,'mI':mi}
    emp(param,ct)
    unit = 'days'
    thres_run0 = {}
    thres_run0.update({threshold:[nosuch,holdD,modfD,unit]})
    thres_run.update({param:thres_run0})
    return nosuch,holdD,modfD,unit

def specify(threshold=0,param='WT',metric='PoA',v=Dv,n=Dn,years=ay,ret='all'):
    try:
         ag = thres_run[param][threshold]
         nosuch,holdD,modfD,unit = ag[0],ag[1],ag[2],ag[3]
    except:
        nosuch,holdD,modfD,unit = threshold_mask(threshold,param,years=ay,v=v,n=n)
    if ret=='hold':
        holder=[]
        for year in years:
            holder = np.append(holder,holdD[metric][year])
        return holder
    else:
        return nosuch, holdD[metric],modfD[metric],unit

            

def products(v=Dv,n=Dn,ay=ay):
    def N(p): return normalize_annual(p,ay,v,n)
    def A(p): return accum(p,ay,v,n)
    def st(p): return stitcher(p,ay,v,n)
    def sth(p): return stitcher(p,ay,v,n,'hold')
    def sp(t,p,m): return specify(t,p,m,v,n,years=ay,ret='hold')
    return N,A,st,sth,sp

#def type_op(string,v=Dv,n=Dn):
    
    #N,A,st,sth,sp = products(v,n)
    ##def sv(
    ##def iD(p): return [], v, ''
    #if string=='norm':
        #return N
    #elif string=='accum':
        #return A
    #elif string=='none':
        #return 
        
#def deviations(X,Y,fit_type=btf.func_linear,mask=None):
    #fit_dic, new_mask,outs_removed = general_fit_pre(X=X,Y=Y,fit_type=fit_type,mask=None)
    #fun = fit_dic['function']
    #exp = [fun(notation_fix(X)[ii]) for ii in range(0,len(v[X]))]
    #if fit_type!=btf.func_exp:
        #dev = [v[Y][ii]-exp[ii] for ii in range(0,len(v[X]))]
    #else:
        #dev = [np.exp(np.log(notation_fix(Y)[ii])-exp[ii]) for ii in range(0,len(v[X]))]
        ##dev = [np.exp(np.log(v[Y][ii])-exp[ii]) for ii in range(0,len(v[X]))]
    #return dev


    
#def thres_products(v=Dv,n=Dn):
    
    
        
##uc,nam = load_obj('new_parameters'), load_obj('new_naming')  
##smart_norms('NEE',uc,nam)
##plt.plot(uc['DoY'],uc['NEE'])
##plt.show()  

#def dict_call(param,dictionary, original_names_dict,normalized_to_all_years='no',
    #extra_params='no',specify_stats=None):
    #always_in = original_names_dict['calls']
    #if param not in always_in:
        ##print(param[-10:])
        #if param[0]=='N' and param[-10:]!='deviations':
            ##if param[-5:]=='Accum' and param!='NRainAccum':
                ###find accumulation index first and then normalize
                ##generic_accumulation(param[1:-5],dictionary, original_names_dict)
            #smart_norms(param[1:],dictionary, original_names_dict,normalized_to_all_years,
                #extra_params,specify_stats=specify_stats)
        ##elif param[-5:]=='Accum':
            ##generic_accumulation(param[:-5],dictionary, original_names_dict)
    #if extra_params=='yes':
        #try:
            #dictionary['reference measures'][param]
        #except KeyError:
            #extras(param,dictionary, original_names_dict)
    #return dictionary,original_names_dict

#dict_call('NCH4_S1',uc,nam)

#def merge_years(param,years,dictionary, original_names_dict,normalized_to_all_years='no',
    #extra_params='no',specify_stats=None):
    #dic, naming = dict_call(param,dictionary, original_names_dict,
        #normalized_to_all_years,extra_params,specify_stats=specify_stats)
    #if type(years)!=list:
        #ys = [years]
    #else:
        #ys = years
    #new = []
    #for y in ys:
        #new = np.append(new,dic[y][param])
    #return new


#def extras(param,dictionary, original_names_dict,add_to_dic='yes',
    #specify_stats=None):
    #dic, naming = dictionary,original_names_dict
    #call = param
    #years = naming['years']
    #calls = naming['calls']
    ##srt = []
    ##for year in years:
        ##s,f = dic['year marks'][year][0],dic['year marks'][year][1]
        ##srt = np.append(srt,dic[year][call])
        ##minn, maxx = min(srt),max(srt)
    #srt=dic[call]
    #minn, maxx = min(srt),max(srt)
    #ref_meas = {}
    #ref_meas.update({'Q1':np.percentile(srt,25)})
    #ref_meas.update({'median':np.percentile(srt,50)})
    #ref_meas.update({'Q2':np.percentile(srt,75)})
    #ref_meas.update({'max':maxx})
    #ref_meas.update({'min':minn})
    #ref_meas.update({'mean':np.mean(srt)})
    #ref_meas.update({'+1std':np.mean(srt)+np.std(srt)})
    #ref_meas.update({'-1std':np.mean(srt)-np.std(srt)})
    #als = ['Q1','median','Q2','max','min','mean','+1std','-1std']
    #al = ['25th percentile','50th percentile','75th percentile','max of all years','min of all years',
        #'mean', 'plus one standard deviation', 'minus one standard deviation']
    #if param=='WT':
        #ref_meas.update({'5cm':-5/100})
        #ref_meas.update({'10cm':-10/100})
        #ref_meas.update({'20cm':-20/100})
        #ref_meas.update({'30cm':-30/100})
        #ref_meas.update({'40cm':-40/100})
        #ref_meas.update({'50cm':-50/100})
        #ref_meas.update({'100cm':-100/100})
        #ref_meas.update({'200cm':-200/100})
        #ref_meas.update({'0cm':0})
        ##wtal = ['10cm below the soil surface','50cm below the soil surface','100cm below the soil surface','soil surface']
        #wtals = ['5cm','10cm','20cm','30cm','40cm','50cm','100cm','200cm','0cm']
        #wtal = [ww+' below the soil surface' for ww in wtals]
        #al = np.append(al, wtal)
        #als = np.append(als, wtals)
    #if specify_stats!=None:
        #if type(specify_stats)!=list:
            #specify_stats = [specify_stats]
        #if type(specify_stats[0])!=list:
            #specify_stats = [specify_stats]
        #for ss in specify_stats:
            #if ss[0]=='percentile' or ss[0]=='%':
                #ref_meas.update({'P'+str(ss[1]):np.percentile(srt,ss[1])})
                #al = np.append(al,str(ss[1])+'th percentile')
                #als = np.append(als,'P'+str(ss[1]))
    #tem = {}
    #for ii in range(0,len(als)):
        #tem.update({als[ii]:al[ii]})
    #tem.update({'all':als})
    #if add_to_dic=='for norm function usage':
        #ref_meas.update({'ref measures':tem})
        ##ref_meas.update({'all reference measures':als})
        #return ref_meas
    #else:
        #try:
            #dic['reference measures'].update({call:ref_meas})
        #except KeyError:
            #ref_ms_param = {}
            #ref_ms_param.update({call:ref_meas})
            #dic.update({'reference measures':ref_ms_param})
            #naming.update({'reference measures':tem})
            ##naming['reference measures'].update({a
