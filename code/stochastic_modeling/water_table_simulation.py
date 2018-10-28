import numpy as np
import matplotlib.pyplot as plt
import xlrd
import scipy.special
import scipy.integrate 
from scipy.integrate import quad
import math
import random

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------

from water_table_functions import *
#from substrate_directory import *

#----------------------------------------------------------------------------------
#PARAMTER SELECTION:
soil_type = 'ex1_tamea'
#SIMULATION PARAMETERS
#user-defined paramters (independent of soil-type) 

np.random.seed(1)
beta_limit = 0.01
flux_limit = 40
N = 30000
dt = 0.1
y_initial = -10
sm_initial = .5 
readings = 50   # readings are for mct simulation runs

#some parameters that are not dependent on y can be defined beforehand:
sv = substrate_dict[soil_type]
psi_s,rd = sv['psi_s'],sv['rd']
sfc, B, nu_star, psi_fc, y_c = Y_ind(soil_type)#T_p, k_s, m, n, psi_s, rd) #@UndefinedVariable
very_deep = -5*rd + psi_fc - psi_s #@UndefinedVariable
ylim = lowerlim(-50, site_loc=soil_type)[0] #@UndefinedVariable
#print('ylim', ylim)
#print('y_c', y_c)
#print('very_deep', very_deep)

# # check functional depence of ET and f on y
# y_arr = np.linspace(0,ylim,300)
# fluxes_arr = np.zeros((2,len(y_arr)))
# for i,y in enumerate(y_arr):
#     _, ET, f1 = simulation_paramters(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, 'ylim info') #@UndefinedVariable 
#     fluxes_arr[0,i] = ET
#     fluxes_arr[1,i] = f1
# plt.plot(y_arr, fluxes_arr[0]); plt.plot(y_arr, fluxes_arr[1])
# plt.show()

#RAINFALL SIMULATION
#rain_series = Rain_events(site_loc=soil_type, N=N, dt=dt) #@UndefinedVariable
#Adding real rainfall data:
v,n = load_obj('parameters_09_18'),load_obj('parameter_index_09_18')
def stitcher(param='Prec',years=n['all years']):
    hold = []
    for yr in years:
        hold = np.append(hold, v[yr][param])
    return hold
rain_series_inches = stitcher()
rain_series = [rin*2.54 for rin in rain_series_inches]
N,dt = len(rain_series),1
#print('mean depth', np.mean(rain_series[rain_series>0]))

#WATER TABLE SIMULATION
water_table_series, h_y_series = np.zeros(N), np.zeros(N)
water_table_series[0] = y_initial 

#SIMULATION FOR WATER TABLE
for i in range(0, N-1):
    y = water_table_series[i]
    beta, ET_y, f1y, deficit = simulation_paramters(y, site_loc=soil_type)
    Xi_y_t = max(0, rain_series[i] - deficit)
    # limit fluctuations related to specific yield to those 
    beta = max(beta_limit, beta)
    fluxes = min(flux_limit, Xi_y_t/beta - dt*(ET_y - f1y)/beta)
    y_new =  fluxes + y  
    water_table_series[i+1] = y_new
#min_y, max_y = min(water_table_series), max(water_table_series)
#print('min and max depth for simulation (cm)')
#print(min_y, max_y)
#print('analytical lower limit (cm)')
#print(ylim)

plt.figure(); plt.plot(water_table_series,label='prediction')
actual_WT = stitcher('WT')
plt.plot([wt*100 for wt in actual_WT],label='observation')
plt.xlabel('time (days)')
plt.ylabel('water table (cm)')
plt.legend()
plt.show()
#plt.figure(); plt.hist(water_table_series, 50, histtype='bar', rwidth=0.5, normed=True)
##plt.show()

#plt.figure(); plt.hist(actual_WT, 50, histtype='bar', rwidth=0.5, normed=True)
#plt.show()
