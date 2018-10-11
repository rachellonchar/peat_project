
##regular code directory setup:
#import sys, os, os.path
#cwd = os.getcwd()
#sys.path.insert(0, cwd+'/prelims')
#from save_funcs import *
#import basic_fitting_funcs as btf


#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------
