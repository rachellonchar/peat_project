
#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
from save_funcs import *
#-------------------------------------------

#open BLF flux data folder:
xl_dirc = main_dirc + 'data_files/' + 'Marcell_xl_data/' + 'BLF_flux_data/'

def extract_xl_BLF(special='', sheet_index=0, file_name='BLF_daily_2015-2018',all_cols=2):
    titles = []
    xl_file = xl_dirc + file_name + '.xlsx'
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
    #cwd = os.getcwd()
    #xl_file = cwd + '/xl/BLF_flux_data/BLF_daily_2015-2018' +'.xlsx'
    #arr, names, unis = extract_xl_BLF('', 0, xl_file,all_cols=1)
    arr, names, unis = extract_xl_BLF(all_cols=1)
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
    naming.update({'years':'2015-2018'})
    return uncut, naming
uc,nam = unwrap1518()

def days_in1518(dic,original_names_dict):
    naming = original_names_dict
    Tott = [i+2190 for i in range(1,len(dic['ID'])+1)] #total days SINCE DAY ONE OF 2009
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
days_in1518(uc,nam)

def rainfall_accumulation1518(dic, naming):
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
rainfall_accumulation1518(uc,nam)

def avg_CH1518(dic,naming):
    s1, s2 = dic['CH4_S1'],dic['CH4_S2']
    avg = [(s1[i]+s2[i])/2 for i in range(0, len(s1))]
    dic.update({'CH4':avg})
    naming['full names'].update({'CH4':'Average methane reading'})
    naming['units'].update({'CH4':'g/(m2 day)'})
    newc = np.append(naming['calls'],'CH4')
    naming.update({'calls':newc})
    return dic, naming
avg_CH1518(uc,nam)
#print(uc)

def adj_wt1518(dic,naming):
    wto = dic['WT']
    avg = [wto[i]-7.01 for i in range(0, len(wto))]
    dic.update({'WTa':avg})
    naming['full names'].update({'WTa':'Adjusted water table'})
    naming['units'].update({'WTa':'cm'})
    newc = np.append(naming['calls'],'WTa')
    naming.update({'calls':newc})
    return dic, naming
adj_wt1518(uc,nam)
#print(uc)

def bulky_1518(dic, naming):
    calls = naming['calls']
    years = naming['years']
    dic_y1518 = {}
    for call in calls:
        nf={}
        for year in years:
            sf = dic['year marks'][year]
            s,f = sf[0],sf[1]
            #print(year,s,f)
            yr_dat = dic[call][s:f]
            nf.update({year:yr_dat})
        dic_y1518.update({call:nf})
    return dic_y1518,naming
v18,n18 = bulky_1518(uc,nam)
#print(v18)

def yr_unwrap(years):
    list_data_names = ['Day of the year', 
        'Net ecosystem exchange', 'Methane', 'senH', 'LE', 'Air temperature', 'Soil temperature 10cm below the surface', 
        'Soil temperature 100cm below the surface', 'Water table depth', 'Relative heat', 'Precipitation']
    list_data_units = ['days','g/(m2 day)', 'g/(m2 day)', 'Wm2','Wm2','C','C','C','m','%', 'inches/day']
    list_abrevs = ['DoY', 'NEE', 'CH4', 'senH', 'LE', 'Tair', 'Ts10', 'Ts100', 'WT', 'RH', 'Prec']
    uncut, naming = {},{}
    tn,tu = {},{}
    for yr in years:
        file_name = 'BLF_daily_' + str(yr)
        arr, names, unis = extract_xl_BLF('', 0, file_name=file_name)
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
        if yr==2017:
            uncut.update({20170:uncut_1y})
        elif yr==2015:
            uncut.update({20150:uncut_1y})
        else:
            uncut.update({yr:uncut_1y})
    naming.update({'full titles':tn})
    naming.update({'units':tu})
    naming.update({'calls':list_abrevs})
    def fx(yr):
        ret = 20170 if yr==2017 else yr
        ret2 = 20150 if ret==2015 else ret
        return ret2
    yearN = {}
    for year in years:
        yearN.update({fx(year):fx(year)})
    naming.update({'year names':yearN})
    naming.update({'years':[fx(year) for year in years]})
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
        y_call = years[yy]
        y_act = int(str(years[yy])[:4])
        DTy = [dd+(y_act-2009)*365 for dd in cut_dic[y_call]['DoY']]
        DT = np.append(DT, DTy)
        cut_dic[y_call].update({'TotDays':DTy})
    naming['full titles'].update({'TotDays':'Total days into entire period'})
    #naming['description'].update({'TotDays':'Total days into entire period (starting from year '+str(min(years))+')'})
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

def adj_wt09(dic,naming):
    wto = dic['WT']
    wta = {}
    years = naming['years']
    for year in years:
        adj = [wto[year][i]*100-7.01 for i in range(0, len(wto[year]))]
        wta.update({year:adj})
    dic.update({'WTa':wta})
    naming['full titles'].update({'WTa':'Adjusted water table'})
    naming['units'].update({'WTa':'cm'})
    newc = np.append(naming['calls'],'WTa')
    naming.update({'calls':newc})
    return dic, naming

#all years we have data for:
years09 = [2009]
for i in range(0, 6):
    new = years09[i]+1
    years09.append(new)
years09.append(2017)
#unwrap
uncut_data, toss = yr_unwrap(years09)
#remove aoutliers and nan values
data_dict, original_naming = all_data_cleanup(uncut_data, toss)
#add days in, rainfall accumulation, and normalized variables
v09_1,n09_1 = rainfall_accumulation(data_dict, original_naming)

def swap_yp(dic,naming):#,years):
    ds={}
    years = naming['years']
    yr0 = years[0]
    for call in naming['calls']:
        dat = dic[yr0][call]
        ds.update({call:{yr0:dat}})
    for yr in years[1:]:
        for call in naming['calls']:
            dat = dic[yr][call]
            ds[call].update({yr:dat})
    CH4d = ds['CH4']
    ds.update({'CH4_S1':CH4d})
    ds.update({'CH4_S2':CH4d})
    naming.update({'years':years})
    
    return ds,naming
v099,n099 = swap_yp(v09_1,n09_1)#,years09)
v09,n09 = adj_wt09(v099,n099)
#print(v09['WT'][2009])

def add_all(dic,naming,disclude_years=[2011,2013,20170],namer=1113,full_namer='demo'):
    
    #print(namer)
    #print(full_namer)
    yr_hold = []
    for call in naming['calls']:
        holder2 = []
        for year in naming['years']:
            if year not in disclude_years:
                holder2 = np.append(holder2,dic[call][year])
                if call=='DoY':
                    yr_hold.append(year)
                    #print(year)
        dic[call].update({namer:holder2})
    new_y = np.append(naming['years'],[namer])
    naming.update({'years':new_y})
    naming['years included'].update({namer:yr_hold})
    naming['year names'].update({namer:full_namer})
    #print(' ')
    return dic,naming

import find_algorithm as algorth
def weed_and_merge(*args,dic=v18,dic2=v09,naming_PREF=n18,naming2=n09,
    years2=[2009,2010,2011,2012,2013,2014,20150,20170],
    years1=[2015,2016,2017,2018]):
        
    naming=naming_PREF #e.g. includes more parameter info
    rel = [a for a in args]
    rel_data, rel_names = {},{}
    #years = naming['years']
    years = years1
    for r in rel:
        rel_data.update({r:dic[r]})
    rel_names.update({'calls':rel})
    ff,dd,uu = {},{},{}
    for r in rel:
        ff.update({r:naming['full names'][r]})
        uu.update({r:'['+naming['units'][r]+']'})
    rel_names.update({'full calls':ff})
    rel_names.update({'units':uu})
    
    #years2 = naming2['years']
    for r in rel:
        for y in years2:
            dat = dic2[r][y]#swap y and r
            rel_data[r].update({y:dat})
    yearsB_ = [2009,2010,2011,2012,2013,2014,20150,2015,2016,20170,2017,2018]
    yr_names,yr_incs = {},{}
    def fx(yr):
        yb = int(str(yr)[:4])
        if yb==2015 or yb==2017:
            nam = str(yb)+' (old data)' if len(str(yr))==5 else str(yb)+' (new data)'
        else:
            nam = str(yr)
        return nam
    for yy in yearsB_:
        yr_names.update({yy:fx(yy)})
        yr_incs.update({yy:[yy]})
    rel_names.update({'years included':yr_incs})
    rel_names.update({'years':yearsB_})
    rel_names.update({'year names':yr_names})
    
    #ADJUST OLD DATA BASED ON 2015 AND 2017:
    dats,nams = algorth.adj_old(rel_data,rel_names)
    return dats,nams
    #return rel_data,rel_names

from inun_aer_funcs import *
from norm_funcs_CH4devs_funcs import *
def save_only_needed(*args,inundation_thresholds=[0],inundation_parameter='WTa',
    temp_thresholds=[5,6,7,8,9,10],temp_parameter='Ts10'):
    #sorting for relevent, possibly meaningful data
    accum = []
    v_,n_ = weed_and_merge(*args)#,dic=v09,naming=n09)
    v,n = add_all(v_,n_,disclude_years=[2011,2013,2015,2017],namer=11130,
        full_namer='disclude 2011,2013 \n(2015,2017 from old data)')
    accum = np.append(accum,11130)
    v,n = add_all(v_,n_,disclude_years=[2011,2013,20150,20170,11130],namer=1113,
        full_namer='disclude 2011,2013 \n(2015,2017 from new data)')
    accum = np.append(accum,1113)
    v,n = add_all(v,n,disclude_years=[1113,11130,20150,20170],namer=1517,
        full_namer='all years \n(2015,2017 from new data)')
    accum = np.append(accum,1517)
    v,n = add_all(v,n,disclude_years=[11130,1113,2015,2017,1517],namer=15170,
        full_namer='all years \n(2015,2017 from old data)')
    accum = np.append(accum,15170)
    v,n = add_all(v,n,disclude_years=[1113,11130,1517,15170,2015,2016,2017,2018],namer=4409170,
        full_namer='2009-2017, excluding 2016 \n(old data)')
    accum = np.append(accum,4409170)
    v,n = add_all(v,n,disclude_years=[1113,11130,1517,15170,4409170,20150,20170,2009,2010,2011,2012,2013,2014],namer=441518,
        full_namer='2015-2018 \n(new data)')
    accum = np.append(accum,441518)
    v,n = add_all(v,n,
        disclude_years=[1113,11130,1517,15170,4409170,441518,20150,20170,2009,2010,2011,2012,2013,2014,2016,2018],namer=441517,
        full_namer='2015,2017 \n(new data)')
    accum = np.append(accum,441517)
    v,n = add_all(v,n,
        disclude_years=[1113,11130,1517,15170,4409170,441518,441517,2015,2017,2009,2010,2011,2012,2013,2014,2016,2018],namer=4415170,
        full_namer='2015,2017 \n(old data)')
    accum = np.append(accum,4415170)
    v,n = add_all(v,n,
        disclude_years=[1113,11130,1517,15170,4409170,441518,441517,4415170],namer=0,
        full_namer='all data \n(2015,2017 respeated)')
    accum = np.append(accum,0)
    v,n = add_all(v,n,
        disclude_years=[1113,11130,1517,15170,4409170,441518,441517,4415170,0,2011,2013,2015,2016,2017,2018],namer=44091701113,
        full_namer='2009-2017, excluding 2011,2013,2016 \n(old data)')
    accum = np.append(accum,44091701113)
    v,n = add_all(v,n,
        disclude_years=np.append([2009,2010,2012,2014,2015,20150,2016,2017,20170,2018],accum),namer=441113,
        full_namer='outlier years \n(2011,2013)')
    for thres in inundation_thresholds:
        v,n = threshold_mask(v,n,threshold=thres,param=inundation_parameter)
    for thres in temp_thresholds:
        v,n = threshold_mask(v,n,threshold=thres,param=temp_parameter)

    for arg in args:
        if arg!='DoY' and arg!='TotDays':
            v,n = normalize_annual(arg,v,n)
    v,n = add_CH4_devs(v,n) #adding fixed deviations
    v,n = add_CH4_devs(v,n,param2='CH4_S2') #adding fixed deviations
    #v,n = normalize_annual('exp CH4_S1',v,n)
    #saving as the object 
    save_obj(v,'params_4states')
    save_obj(n,'names_4states')
    return v,n
    
    
save_only_needed('DoY', 'NEE', 'CH4', 'Tair' ,'Ts10' ,'Ts100' ,'WTa', 'Prec',
    'CH4_S1','CH4_S2',
    'TotDays','RainAccum',inundation_thresholds=[-0.5,0,0.5,1,1.5,1.6,1.7,1.8,1.9,2])
    
    
#v,n = save_only_needed('DoY', 'NEE', 'CH4', 'Tair' ,'Ts10' ,'Ts100' ,'WTa', 'Prec',
    #'CH4_S1','CH4_S2',
    #'TotDays','RainAccum',inundation_thresholds=[0])

#print(vv['WTa'])
#print(v['threshold='][0]

#vnew,nnew = threshold_mask(vv,nn)

