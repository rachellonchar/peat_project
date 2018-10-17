
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
variables0,naming0 = load_obj('basic_parameters'),load_obj('basic_naming')
all_years = naming0['years']
from analysis_funcs_newdat import dict_call
#def updater(*params,normalized_to_all_years='no',stats='no'):
    #for param in params:
        #dict_call(param,variables, naming,normalized_to_all_years,stats)
    #return variables, naming
#-----------------------------------------------------------------------

#fix dictionaries to match that of new data objs:
yrs = load_obj('years')
naming = {}
for key, value in naming0.items():
    if key in ['units','calls','years']:
        naming.update({key:naming0[key]})
    elif key=='full titles':
        naming.update({'full names':naming0[key]})

variables = {}
for call in naming['calls']:
    hold = []
    for yr in yrs:
        hold = np.append(hold,variables0[yr][call])
    variables.update({call:hold})

#-----------------------------------------------------------------------
def updater(*params,normalized_to_all_years='no',stats='no'):
    for param in params:
        dict_call(param,variables, naming,normalized_to_all_years,stats)
    return variables, naming

#updater('NTs10')
#variables['NTs10']

plt.plot(variables['WT'],'r')
plt.title('water table, BLF 2009-15,2017 data')
plt.ylabel('water table (m)')
plt.show()
