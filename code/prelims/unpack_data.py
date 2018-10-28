
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

def param_namer(strin):
    if strin[0:6]=='Tsoil_':
        name = 'soil temperature at ' + strin[6:] + ' below the surface'
    elif strin[0:2]=='Ta':
        name = 'air temperature'
    elif strin[0:3]=='NEE':
        name = 'net ecosystem exchange (CO2)'
    elif strin[0]=='W':
        name = 'water table'
    elif strin[0]=='P':
        name = 'precipitation'
    else:
        name = strin
    return name 


def unwrap1518():
    uncut, naming = {},{}
    tn,tu = {},{}
    arr, names, unis = extract_xl_BLF(all_cols=1)
    list_data_names = []
    for nam in names:
        out = param_namer(nam)
        list_data_names.append(out)
    new_abvs = []
    for i in range(0, len(names)):
        abvs = names[i]
        if abvs=='WT' or abvs=='Water_Table':            #WT values originally in cm (mislabeled...labeled accurately later on) 
            dat = [wt_crude-7.01 for wt_crude in arr[i]] #subtract 7.01 cm according to Julain + Tyler
        else:
            dat = arr[i]
        if abvs=='CH4_s1':
            abvs='CH4'
        uncut.update({abvs:dat[2:]})
        nam = list_data_names[i]
        uns = unis[i]
        tn.update({abvs:nam})
        tu.update({abvs:uns})
        new_abvs.append(abvs)
    naming.update({'full names':tn})
    naming.update({'units':tu})
    naming.update({'calls':new_abvs})
    return uncut, naming
uc,nam = unwrap1518()

#for older data:
def yr_unwrap(years):
    uncut, naming = {},{}
    tn,tu = {},{}
    new_abvs = []
    for yr in years:
        file_name = 'BLF_daily_' + str(yr)
        arr, names, unis = extract_xl_BLF('', 0, file_name=file_name)
        list_data_names = []
        uncut_1y = {}
        #print(names)
        for nam in names:
            out = param_namer(nam)
            list_data_names.append(out)
        for i in range(0, len(names)):
            abvs = names[i]
            if abvs=='WT' or abvs=='Water_Table':
                dat = [wt_crude for wt_crude in arr[i]]
                abvs='WT'
            else:
                dat = arr[i]
            uncut_1y.update({abvs:dat[2:]})
            if yr==years[0]:
                nam = list_data_names[i]
                uns = unis[i]
                tn.update({abvs:nam})
                tu.update({abvs:uns})
                new_abvs.append(abvs)
        uncut.update({yr:uncut_1y})
    naming.update({'full names':tn})
    naming.update({'units':tu})
    naming.update({'calls':new_abvs})
    naming.update({'years':years})
    #naming.update({'description':tn})
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
        Tair, Ts10 = uncut['Tair'], uncut['Tsoil_10cm']
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
#years_old = [2009,2010,2011,2012,2013,2014]
#yr_unwrap(years_old)

def days_in(dic,original_names_dict):
    years_old = [2009,2010,2011,2012,2013,2014]
    dOLD_,nOLD_ = yr_unwrap(years_old)
    dOLD, nOLD = all_data_cleanup(dOLD_,nOLD_)
    calls = original_names_dict['calls']
    
    naming = original_names_dict
    Tott = [i for i in range(1,len(dic['Date'])+1)]
    yr1 = [i for i in range(1,366)]
    yr_leap = [i for i in range(1,367)]
    yrs = np.append(yr1,yr_leap) #2016 was leap year
    for i in range(0,3):
        yrs = np.append(yrs,yr1)
    DoY = [yrs[i] for i in range(0,len(dic['Date']))]
    years = [2015,2016,2017,2018]
    yr_marks = {}
    s,f = 0,365
    for y in years:
        yr_marks.update({y:[s,f]})
        pls=366 if y==2016 else 365
        plf=366 if y==2015 else 365
        s+=pls
        f+=plf
    for yr in years:
        dOLD.update({yr:{}})
    cOLD = nOLD['calls']
    callsp = []
    for call in calls:
        dat = dic[call]
        for yr in years:
            st,fi = yr_marks[yr][0],yr_marks[yr][1]
            if call=='Date':
                call = 'DoY'
                dOLD[yr].update({call:DoY[st:fi]})
            elif call=='Water Table':
                call = 'WT'
                dOLD[yr].update({call:[wt*100-7.01 for wt in dat[st:fi]]}) #subtract 7.01 cm according to Julain + Tyler
            else:
                dOLD[yr].update({call:dat[st:fi]})
            callsp.append(call)
        #if call not in cOLD:
            #print(call)
    nOLD.update({'calls+':callsp})
    nOLD.update({'years+':years})
    nOLD.update({'all years':np.append(years_old,years)})
    nOLD.update({'units':original_names_dict['units']})
    nOLD['units'].update({'WT':'cm'}) #changing WT units to be in cm
    return dOLD,nOLD

v,n = days_in(uc,nam)
save_obj(v,'parameters_09_18')
save_obj(n,'parameter_index_09_18')
#yrs = n['all years']
#for yr in yrs:
    ##print(yr)
    #if yr in n['years']:
        #plt.plot(v[yr]['WT'],marker='.',label=str(yr))
    #else:
        #plt.plot(v[yr]['WT'],label=str(yr))
    
#plt.legend()
#plt.show()





#def rainfall_accumulation(dic, naming):
    #years = naming['years']
    #all_A = []
    #for year in years:
        #s,f = dic['year marks'][year][0],dic['year marks'][year][1]
        #rains,days = dic['Prec'][s:f],dic['DoY'][s:f]
        #cum_rain=0
        #Rbar = np.mean(rains)
        #A = np.zeros(len(days))
        #for d in range(0,len(days)):
            #rain,day = rains[d],days[d]
            #cum_rain += rain
            #A[d] = cum_rain - Rbar*day
        #all_A = np.append(all_A,A)
    #dic.update({'RainAccum':all_A})
    #naming['full names'].update({'RainAccum':'Rainfall accumulation index'})
    ##naming['description'].update({'RainAccum':'Deviation of precipitation from expected daily precipitation in a given year'})
    #naming['units'].update({'RainAccum':'inches/day'})
    #newc = np.append(naming['calls'],'RainAccum')
    #naming.update({'calls':newc})
    #return dic, naming
#rainfall_accumulation(uc,nam)

#def avg_CH(dic,naming):
    #s1, s2 = dic['CH4_S1'],dic['CH4_S2']
    #avg = [(s1[i]+s2[i])/2 for i in range(0, len(s1))]
    #dic.update({'CH4':avg})
    #naming['full names'].update({'CH4':'Average methane reading'})
    #naming['units'].update({'CH4':'g/(m2 day)'})
    #newc = np.append(naming['calls'],'CH4')
    #naming.update({'calls':newc})
    #return dic, naming
#avg_CH(uc,nam)


#save_obj(uc,'new_parameters')
#save_obj(nam,'new_naming')
