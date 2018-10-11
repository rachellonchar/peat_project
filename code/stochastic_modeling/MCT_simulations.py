import numpy as np
import matplotlib.pyplot as plt
import xlrd
import scipy.special
import scipy.integrate 
from scipy.integrate import quad
import math
import random
from RL_water_table_functions import Y_ind, Rain_events, \
    simulation_paramters, lowerlim
from RL_substrate_directory import substrate_dict

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

#unzipping dictionary contents 
keys = []
values = []
for k, v in substrate_dict[soil_type].items():
    keys.append(k)
    values.append(v)
for var in zip(keys, values):
    exec( "%s=%s" % (var[0], var[1]))
#some parameters that are not dependent on y can be defined beforehand:
sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd) #@UndefinedVariable
very_deep = -5*rd + psi_fc - psi_s #@UndefinedVariable
ylim = lowerlim(-50, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)[0] #@UndefinedVariable
print('ylim', ylim)
print('y_c', y_c)
print('very_deep', very_deep)

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
rain_series = Rain_events(lam, alpha, N, dt) #@UndefinedVariable
print('mean depth', np.mean(rain_series[rain_series>0]))

#WATER TABLE SIMULATION
water_table_series = np.zeros(N)
water_table_series[0] = y_initial 
h_y_series = np.zeros(N)

#SIMULATION FOR WATER TABLE
for i in range(0, N-1):
    y = np.copy(water_table_series[i])
    beta, ET_y, f1y, deficit = simulation_paramters(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam) #@UndefinedVariable
    Xi_y_t = max(0, rain_series[i] - deficit)
    # limit fluctuations related to specific yield to those 
    beta = max(beta_limit, beta)
    fluxes = min(flux_limit, Xi_y_t/beta - dt*(ET_y - f1y)/beta)
    y_new =  fluxes + y  
    water_table_series[i+1] = y_new
min_y, max_y = min(water_table_series), max(water_table_series)
print('min and max depth for simulation (cm)')
print(min_y, max_y)
print('analytical lower limit (cm)')
print(ylim)

plt.figure(); plt.plot(water_table_series)
plt.figure(); plt.hist(water_table_series, 50, histtype='bar', rwidth=0.5, normed=True)
plt.show()

#SIMULATION MCTs
#define threshold depth
thres_pts = readings
step = math.floor((max_y - min_y)/thres_pts)
thres = np.zeros(thres_pts)
MCT_thres_a, MCT_thres_b = np.zeros(thres_pts), np.zeros(thres_pts)
proportion_above, proportion_below = np.zeros(thres_pts), np.zeros(thres_pts)
#MCT_analytic = np.zeros(thres_pts)
#mct_for_y = np.zeros(thres_pts)
z = min_y
for p in range(0, thres_pts):
    above, below = [], []
    count_b, count_a, cb_tot, ca_tot = 0, 0, 0, 0
    for y in water_table_series: #N-1
        if y <= z:
            above.append(count_a)
            count_a = 0
            count_b += dt
            cb_tot += dt
        elif y > z: #above threshold
            below.append(count_b) #count total counts below and reset to zero
            count_b = 0
            count_a += dt
            ca_tot += dt
    MCT_above, MCT_below = np.mean(above[1:]), np.mean(below[1:])
    MCT_thres_a[p] = MCT_above
    MCT_thres_b[p] = MCT_below
    proportion_above[p] = ca_tot/len(water_table_series)
    proportion_below[p] = cb_tot/len(water_table_series)
    thres[p] = z
    z += step

print(' ')
print('above threshold: ', MCT_above, ' days')
print('below threshold: ', MCT_below, 'days')
