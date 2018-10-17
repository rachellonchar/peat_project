
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
variables,naming = load_obj('new_parameters'),load_obj('new_naming')
all_years = naming['years']
from analysis_funcs_newdat import dict_call
def updater(*params,normalized_to_all_years='no',stats='no'):
    for param in params:
        dict_call(param,variables, naming,normalized_to_all_years,stats)
    return variables, naming
#-----------------------------------------------------------------------
#plt.plot([wt/100 for wt in variables['WT']])
#plt.show()

plt.plot(variables['WT'],'b')
plt.title('water table, BLF 2015-18 data')
plt.ylabel('water table (m)')
plt.show()
