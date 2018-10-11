
# script to specify soil/substrate parameters 
# based on code/prelims/substrate_directory

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------
from substrate_directory import substrate_dict
#------------------------------------------------------------------------

#PARAMTER SELECTION:
soil_type = 'ex1_tamea'

#unzipping dictionary contents 
specify_dic = substrate_dict[soil_type]
#----
keys, values = [],[]
for k, v in specify_dic.items():
    keys.append(k)
    values.append(v)
for var in zip(keys, values):
    exec( "%s=%s" % (var[0], var[1]))


#SIMULATION PARAMETERS
#user-defined paramters (independent of soil-type) 
#np.random.seed(1)
beta_limit = 0.01
flux_limit = 40
N = 30000
dt = 0.1
y_initial = -10
sm_initial = .5 
# readings are for mct simulation runs
readings = 100  

#ANALYTICAL DISCRETIZATION
fineness = 50 #readings to take for pdf and cdf 
