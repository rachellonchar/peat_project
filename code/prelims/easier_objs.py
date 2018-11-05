
#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------
import basic_fitting_funcs as btf
sys.path.insert(0, cwd_code+'/stochastic_modeling')


##-----------------------------------------------------------------------
variables,naming = load_obj('parameters_09_18'),load_obj('parameter_index_09_18')
ay = []
for nn in range(9,19):
    ay.append(2000+nn)


years=[a for a in ay if a!=2013]
years=[2015,2016,2017,2018]
ay=years

#def stitcher(param='Prec',years=n['all years']):
    #hold = []
    #for yr in years:
        #hold = np.append(hold, v[yr][param])
    #return hold
    
    
##variables,naming = load_obj('new_parameters'),load_obj('new_naming')
#all_years = naming['years']


from basic_data_products import *
N,Ac,Mg,MgA,AI = products(variables,naming)
def permA(thres): return AI(thres,'WT','tA')
def permI(thres): return AI(thres,'WT','tI')

def maskA(thres): return AI(thres,'WT','mA')
def maskI(thres): return AI(thres,'WT','mI')


coas = ['WT','Prec','CH4','CH4_s2','Tsoil_10cm','DoY','Tair','NEE']
dicy,dica = {},{}
calls=[]
for parm in coas:
    hold,holdD = [],{}
    for year in years:
        try:
            hold=np.append(hold,variables[year][parm])
            holdD.update({year:variables[year][parm]})
            #print('none')
        except:
            hold=np.append(hold,variables[year]['CH4']) #reitated CH4 values for both s1 and s2
            holdD.update({year:variables[year]['CH4']})
            #print('enters')
    if parm=='Tsoil_10cm':
        parm='Ts10'
    calls.append(parm)
    dica.update({parm:hold})
    dicy.update({parm:holdD})

nosuch,holdD,modf,unit = accum('Prec',years=ay,v=variables,n=naming)
dicy.update({'RainAccum':holdD})
parm='RainAccum'
hold=[]
for year in years:
    hold=np.append(hold,holdD[year])
calls.append(parm)
dica.update({parm:hold})

for pp in calls:
    hold,holdD = [],{}
    for year in years:
        hold=np.append(hold,normalize_series(dicy[pp][year]))
        holdD.update({year:normalize_series(dicy[pp][year])})
    dica.update({'N'+pp:hold})
    dicy.update({'N'+pp:holdD})
save_obj(dica,'easier_params')
save_obj(dicy,'easier_params_yr')
#save_
#print(dica['Ts10'])
        
#print(naming['calls+'])
#v,n=variables,naming
##def f_products(fun,v=Dv,n=Dn):
    ##N,A,st,sp = products(v=v,n=n)

##def updater(*params,normalized_to_all_years='no',stats='no'):
    ##for param in params:
        ##dict_call(param,variables, naming,normalized_to_all_years,stats)
    ##return variables, naming
##-----------------------------------------------------------------------
##plt.plot([wt/100 for wt in variables['WT']])
##plt.show()
#fig, ax = plt.subplots(ncols=1,nrows=4,  sharex=True, sharey=True, figsize=(15,9))
#Nn=1
#for yr in [2015,2016,2017,2018]:
    #plt.subplot(1,4,Nn)
    #plt.plot(variables[yr]['WT'],'r')
    #Nn+=1
#plt.title('water table, BLF 2015-18 data')
#plt.ylabel('water table (m)')
#plt.show()
