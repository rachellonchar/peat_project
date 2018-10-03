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

##functions to define more as needed 
#def generic_accumulation(param,dictionary, original_names_dict):
    #dic, naming = dictionary,original_names_dict
    #years = naming['years']
    #for year in years:
        #rains,days = dic[year][param],dic[year]['DoY']
        #cum_rain=0
        #Rbar = np.mean(rains)
        #A = np.zeros(len(days))
        #for d in range(0,len(days)):
            #rain,day = rains[d],days[d]
            #cum_rain += rain
            #A[d] = cum_rain - Rbar*day
        #dic[year].update({param+'Accum':A})
    #fn = naming['full titles'][param]
    #dn = naming['description'][param]
    #un = naming['units'][param]
    #naming['full titles'].update({param+'Accum':fn+' accumulation index'})
    #naming['description'].update({param+'Accum':'Deviation from expected daily value in a given year for '+dn})
    #naming['units'].update({param+'Accum':un})
    #newc = np.append(naming['calls'],param+'Accum')
    #naming.update({'calls':newc})
    ##return dic, naming

def extras(param,dictionary, original_names_dict,add_to_dic='yes',
    specify_stats=None):
    dic, naming = dictionary,original_names_dict
    call = param
    years = naming['years']
    calls = naming['calls']
    #srt = []
    #for year in years:
        #s,f = dic['year marks'][year][0],dic['year marks'][year][1]
        #srt = np.append(srt,dic[year][call])
        #minn, maxx = min(srt),max(srt)
    srt=dic[call]
    minn, maxx = min(srt),max(srt)
    ref_meas = {}
    ref_meas.update({'Q1':np.percentile(srt,25)})
    ref_meas.update({'median':np.percentile(srt,50)})
    ref_meas.update({'Q2':np.percentile(srt,75)})
    ref_meas.update({'max':maxx})
    ref_meas.update({'min':minn})
    ref_meas.update({'mean':np.mean(srt)})
    ref_meas.update({'+1std':np.mean(srt)+np.std(srt)})
    ref_meas.update({'-1std':np.mean(srt)-np.std(srt)})
    als = ['Q1','median','Q2','max','min','mean','+1std','-1std']
    al = ['25th percentile','50th percentile','75th percentile','max of all years','min of all years',
        'mean', 'plus one standard deviation', 'minus one standard deviation']
    if param=='WT':
        ref_meas.update({'5cm':-5/100})
        ref_meas.update({'10cm':-10/100})
        ref_meas.update({'20cm':-20/100})
        ref_meas.update({'30cm':-30/100})
        ref_meas.update({'40cm':-40/100})
        ref_meas.update({'50cm':-50/100})
        ref_meas.update({'100cm':-100/100})
        ref_meas.update({'200cm':-200/100})
        ref_meas.update({'0cm':0})
        #wtal = ['10cm below the soil surface','50cm below the soil surface','100cm below the soil surface','soil surface']
        wtals = ['5cm','10cm','20cm','30cm','40cm','50cm','100cm','200cm','0cm']
        wtal = [ww+' below the soil surface' for ww in wtals]
        al = np.append(al, wtal)
        als = np.append(als, wtals)
    if specify_stats!=None:
        if type(specify_stats)!=list:
            specify_stats = [specify_stats]
        if type(specify_stats[0])!=list:
            specify_stats = [specify_stats]
        for ss in specify_stats:
            if ss[0]=='percentile' or ss[0]=='%':
                ref_meas.update({'P'+str(ss[1]):np.percentile(srt,ss[1])})
                al = np.append(al,str(ss[1])+'th percentile')
                als = np.append(als,'P'+str(ss[1]))
    tem = {}
    for ii in range(0,len(als)):
        tem.update({als[ii]:al[ii]})
    tem.update({'all':als})
    if add_to_dic=='for norm function usage':
        ref_meas.update({'ref measures':tem})
        #ref_meas.update({'all reference measures':als})
        return ref_meas
    else:
        try:
            dic['reference measures'].update({call:ref_meas})
        except KeyError:
            ref_ms_param = {}
            ref_ms_param.update({call:ref_meas})
            dic.update({'reference measures':ref_ms_param})
            naming.update({'reference measures':tem})
            #naming['reference measures'].update({a

def normalize_series(series,preserve_negativity=0,maxx=None, minn=None,
    ref_measures=None):
    #d = series
    if maxx==None:
        mx=max(series)
    else:
        mx=maxx
    if minn==None:
        mn=min(series)
    else:
        mn=minn
    overall_mx = max(abs(mx),abs(mn))
    #if preserve_negativity==1:
        #def funorm(val): return (2*(val-mn)/(mx-mn) - 1)
    #else:
    def funorm(val): return val/overall_mx
    new = [funorm(s) for s in series]
    if type(ref_measures)==dict:
        retdic = {}
        callm = ref_measures['ref measures']['all']
        for call in callm:
            retdic.update({call:funorm(ref_measures[call])})
        return new, retdic,funorm
    else:
        return new, 0
def smart_norms(param,dictionary, original_names_dict,normalized_to_all_years='no',
    extra_params='no',specify_stats=None):
    dic, naming = dictionary,original_names_dict
    call = param
    years = naming['years']
    calls = naming['calls']
    keep_pos,caln = {},{}
    if extra_params=='yes':
        ref_meas = extras(param,dictionary, original_names_dict,
            add_to_dic='for norm function usage',specify_stats=specify_stats)
    else:
        ref_meas=None
    if normalized_to_all_years=='no':
        mnn, mxx = None, None
    else:
        if extra_params=='yes':
            minn,maxx = ref_meas['min'],ref_meas['max']
        else:
            #srt = []
            #for year in years:
                #srt = np.append(srt,dic[year][call])
            srt = dic[call]
            minn, maxx = min(srt),max(srt)
        mnn, mxx = minn, maxx
    #determine which norm to use or whether to normalize at all
    #if extra_params_only!='yes':
    name_norm = 'N'+call
    caln.update({call:name_norm})
    if call=='DoY' or call=='TotDays':#days don't get normalized
        keep_pos.update({call:'not normed'})
    else:
        keep_pos.update({call:'yes'})
        #for year in years:
            #series = dic[year][call]
        series=dic[call]
        if min(series)<-0.0001:
            keep_pos.update({call:'no'})
    #normalizing 
    #for year in years:
        #normal_dic_yr = {}
        ##for call in calls:
        #series = dic[year][call]
    series = dic[call]
    if extra_params=='yes':
        if keep_pos[call]=='not normed':
            new_s = series
        elif keep_pos[call]=='no':
            new_s, ref_ms,funcN = normalize_series(series,1,mxx,mnn,ref_meas)
            dic.update({caln[call]+' func':funcN})
        elif keep_pos[call]=='yes':
            new_s, ref_ms,funcN = normalize_series(series,0,mxx,mnn,ref_meas)
            dic.update({caln[call]+' func':funcN})
    else:
        if keep_pos[call]=='not normed':
            new_s = series
        elif keep_pos[call]=='no':
            new_s, ref_ms = normalize_series(series,1,mxx,mnn,ref_meas)
            #dic.update({caln[call]+' func':funcN})
        elif keep_pos[call]=='yes':
            new_s, ref_ms = normalize_series(series,0,mxx,mnn,ref_meas)
            #dic.update({caln[call]+' func':funcN})
    dic.update({caln[call]:new_s})
    #dic[year].update({caln[call]:new_s})
    if extra_params=='yes':
        try:
            dic['reference measures'].update({caln[call]:ref_ms})
        except KeyError:
            ref_ms_param = {}
            ref_ms_param.update({caln[call]:ref_ms})
            dic.update({'reference measures':ref_ms_param})
            naming.update({'reference measures':ref_meas['ref measures']})
    #naming
    calls_to_add = []
    #for call in calls:
    ca = caln[call]
    calls_to_add.append(ca)
    #print(naming['full titles'])
    fn = naming['full names'][call]
    #dn = naming['description'][call]
    if keep_pos[call]=='not normed':
        un = naming['units'][call]
        naming['full names'].update({ca:fn})
        naming['units'].update({ca:un})
        #naming['description'].update({ca:dn})
    elif keep_pos[call]=='no':
        naming['full names'].update({ca:fn})#+' (normalized)'})
        naming['units'].update({ca:'unitless, restricted to [-1,1]'})
        #naming['description'].update({ca:dn})#+' (normalized)'})
    elif keep_pos[call]=='yes':
        naming['full names'].update({ca:fn})#+' (normalized)'})
        naming['units'].update({ca:'unitless, restricted to [0,1]'})
        #naming['description'].update({ca:dn})#+' (normalized)'})
    naming.update({'calls':np.append(calls,ca)})
    #----------
    #if type(ref_ms)==dict:
        
#uc,nam = load_obj('new_parameters'), load_obj('new_naming')  
#smart_norms('NEE',uc,nam)
#plt.plot(uc['DoY'],uc['NEE'])
#plt.show()  

def dict_call(param,dictionary, original_names_dict,normalized_to_all_years='no',
    extra_params='no',specify_stats=None):
    always_in = original_names_dict['calls']
    if param not in always_in:
        #print(param[-10:])
        if param[0]=='N' and param[-10:]!='deviations':
            #if param[-5:]=='Accum' and param!='NRainAccum':
                ##find accumulation index first and then normalize
                #generic_accumulation(param[1:-5],dictionary, original_names_dict)
            smart_norms(param[1:],dictionary, original_names_dict,normalized_to_all_years,
                extra_params,specify_stats=specify_stats)
        #elif param[-5:]=='Accum':
            #generic_accumulation(param[:-5],dictionary, original_names_dict)
    if extra_params=='yes':
        try:
            dictionary['reference measures'][param]
        except KeyError:
            extras(param,dictionary, original_names_dict)
    return dictionary,original_names_dict

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

#print('PrecAccum'[-5:])
    
    

    #print(tn,tu)
    #hold = [[] for i in range(0, len(list_abrevs))]
    #allyrs = {}
    #for i in range(0, len(list_abrevs)):
        #abvs = list_abrevs[i]
        #for yr in years:
            #hold[i] = np.append(hold[i],uncut[yr][abvs])
        #allyrs.update({abvs:hold[i]})
    #uncut.update({'all years':allyrs})
    #print(naming)

##--------------------------------------------------------------------------
##load data dictionaries:
#years = load_obj('years')
#calls = load_obj('calls')
#calls_by_year = load_obj('calls_by_year')
#full_calls = load_obj('full_calls')
#units = load_obj('units')
###--------------------------------------------------------------------------

##{'Tair': 'Air temperature', 
##'TotDays': 'Total days in', 
##'Prec': 'Precipitation', 
##'Ts10': 'Soil temperature 10cm below the surface', 
##'CO2': 'Carbon dioxide flux', 
##'CH4': 'Methane flux', 
##'DoY': 'Day of the year', 
##'RainAccum': 'Rainfall accumulation index', 
##'WT': 'Water table depth'}


##defining alternate measures ----------------------------------------------
##
##-----------------------------------------------------
##rewrites pickle file if rerun 
##-----------------------------------------------------
#from probability_funcs_all import averaged, gen_normed, ratio, partial_corr, sep_pos_neg, is_normal

#picks = ['CO2', 'CH4', 'Ts10', 'WT', 'Prec']

#other_measures = {}
#full_names = ['Averaging over some interval of days---values normalized within [-1,1]',
    #'Ratio of (normalized) carbon dioxide to methane ','Normalized within [-1,1]','partial linear correlation',
    #'Net carbon flux normalized','pass or not passes the Shapiro-Wilk test for a normal distribution']
#meas = ['averaged','ratios','normalized','correlation','net flux','SW_test']
#other_measures_titles = {}
#for i in range(0, len(meas)):
    #other_measures_titles.update({meas[i]:full_names[i]})
    
#c = [calls_by_year[pick] for pick in picks]
#c1 = [calls[pick] for pick in picks]
##-----------------------------------------------------
##averaged, correlations, normalized
#avgdays = [0,1,3,7,10,14,30,40,60,80,100,121,182]
#dd, ddcor, swsd = {}, {}, {}
#for av in avgdays:
    #if av==0:
        #avg_xd = gen_normed(c1[0],c1[1],c1[2],c1[3],c1[4])
    #else:
        #avg_xd = averaged(c[0],c[1],c[2],c[3],c[4], splits='none',avg_over=av)
    #temp = {}
    #itemp = {}
    #sws = {}
    #for i in range(0,len(picks)):
        #jtemp = {}
        #for j in range(0,len(picks)):
            #pc_ = partial_corr(np.array([avg_xd[i],avg_xd[j]]).T)
            #pc = pc_[0][1]
            #jtemp.update({picks[j]:pc})
        #itemp.update({picks[i]:jtemp})
    #for ii in range(0,5):
        #temp.update({picks[ii]:avg_xd[ii]})
        #try:
            #pas,words = is_normal(avg_xd[ii])
        #except:
            #pas,words = 2,'inconclusive---too few data points'
        #sws.update({picks[ii]:[pas,words]})
    #ddcor.update({str(av)+' day(s)':itemp})
    #dd.update({str(av)+' day(s)':temp})
    #swsd.update({str(av)+' day(s)':sws})
#other_measures.update({'averaged':dd})
#other_measures.update({'cor':ddcor})
#day1 = other_measures['averaged']['1 day(s)']
#other_measures.update({'normalized':day1})
#other_measures.update({'SW_test':swsd})


##-----------------------------------------------------
##seperating positive and negative flux
#sepp = sep_pos_neg(c1[0],c1[1])
#sepC, sepH, sC = {}, {}, {}
#sepC.update({'release':sepp[0][0]})
#sepC.update({'absorb':sepp[0][1]})
#sepH.update({'release':sepp[1][0]})
#sepH.update({'absorb':sepp[1][1]})
#sC.update({'CO2':sepC})
#sC.update({'CH4':sepH})
#other_measures.update({'net flux':sC})
##-----------------------------------------------------
##ratios
#CC = gen_normed(c1[0],c1[1])
#co2, ch4 = CC[0], CC[1]
#ratio_C = ratio(co2,ch4)
#other_measures.update({'ratios':ratio_C})
#CO2_out = other_measures['net flux']['CO2']['release']
#ratio_Cout = ratio(CO2_out, ch4)
#other_measures.update({'ratios of emissions':ratio_Cout})

##--------------------------------------------------------------------------

#save_obj(other_measures,'other_measures')
#save_obj(other_measures_titles,'other_measures_titles')



#name_norm = 'N'+call
    #caln.update({call:name_norm})
    #if call=='DoY' or call=='TotDays':#days don't get normalized
        #keep_pos.update({call:'not normed'})
    #else:
        #keep_pos.update({call:'yes'})
        #for year in years:
            #series = dic[year][call]
            #if min(series)<-0.0001:
                #keep_pos.update({call:'no'})
    ##normalizing 
    #for year in years:
        #normal_dic_yr = {}
        ##for call in calls:
        #series = dic[year][call]
        #if keep_pos[call]=='not normed':
            #new_s = series
        #elif keep_pos[call]=='no':
            #new_s, ref_ms = normalize_series(series,1,mxx,mnn,ref_meas)
        #elif keep_pos[call]=='yes':
            #new_s, ref_ms = normalize_series(series,0,mxx,mnn,ref_meas)
        #dic[year].update({caln[call]:new_s})
        ##dic[year].update({caln[call]:new_s})
    ##naming
    #calls_to_add = []
    ##for call in calls:
    #ca = caln[call]
    #calls_to_add.append(ca)
    ##print(naming['full titles'])
    #fn = naming['full titles'][call]
    #dn = naming['description'][call]
    #if keep_pos[call]=='not normed':
        #un = naming['units'][call]
        #naming['full titles'].update({ca:fn})
        #naming['units'].update({ca:un})
        #naming['description'].update({ca:dn})
    #elif keep_pos[call]=='no':
        #naming['full titles'].update({ca:fn+' (normalized)'})
        #naming['units'].update({ca:'unitless, restricted to [-1,1]'})
        #naming['description'].update({ca:dn+'\n(normalized to preserve negativity)'})
    #elif keep_pos[call]=='yes':
        #naming['full titles'].update({ca:fn+' (normalized)'})
        #naming['units'].update({ca:'unitless, restricted to [0,1]'})
        #naming['description'].update({ca:dn+'\n(normalized using maximum value)'})
    #naming.update({'calls':np.append(calls,ca)})
