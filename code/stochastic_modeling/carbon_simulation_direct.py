import numpy as np
import matplotlib.pyplot as plt
import xlrd
import scipy.special
import scipy.integrate 
from scipy.integrate import quad
#from helpful_functions import unzip_dict, extract_lines, txt_out, xl_output, blockPrint, enablePrint
#blockPrint()
import math
import random
np.random.seed(1)
#from water_table_functions import Y_ind, Rain_events, \
    #simulation_paramters, lowerlim
#from substrate_directory import substrate_dict
#from substrate_directory import soil_type, beta_limit, flux_limit, \
    #N, dt, y_initial, sm_initial, readings
#enablePrint()

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------

from water_table_functions import *
from substrate_directory import *

#----------------------------------------------------------------------------------
print('Soil type selected from substrate directory: ')
print(soil_type)
print(' ')

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
time_days = np.zeros(N)

#SIMULATION FOR WATER TABLE
for tt in range(0, N-1):
    y = np.copy(water_table_series[tt])
    beta, ET_y, f1y, deficit = simulation_paramters(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam) #@UndefinedVariable
    Xi_y_t = max(0, rain_series[tt] - deficit)
    # limit fluctuations related to specific yield to those 
    beta = max(beta_limit, beta)
    fluxes = min(flux_limit, Xi_y_t/beta - dt*(ET_y - f1y)/beta)
    y_new =  fluxes + y  
    water_table_series[tt+1] = y_new
    time_days[tt] = tt*dt
min_y, max_y = min(water_table_series), max(water_table_series)
print('min and max depth for simulation (cm)')
print(min_y, max_y)
print('analytical lower limit (cm)')
print(ylim)

#CARBON PRODUCTION
#define threshold depths
thres_pts = readings
#step = math.floor((max_y - min_y)/thres_pts)
max_y = 0
step = (max_y - min_y)/thres_pts
thres = np.zeros(thres_pts)
#MCTs = np.zeros(thres_pts)
y_start = min_y
sample = math.ceil(y_start) #change to floor and adjust lower bound
carbon_series = np.zeros((thres_pts, N)) #for i=0,...,N carbon_series[i] will be a vector for different threshold values
emission_series = np.zeros_like(carbon_series)
DMC = np.zeros((thres_pts, N))
Ctot, emissions_total = np.zeros(N), np.zeros(N)
#carbon_series[0] = 0
rho_dry_peat = 0.4 #g/cm3
rho_wet_peat = 1.12 #g/cm3
rho = (0.4+1.12)/2
#organic carbon anywhere from 18-60% of peat
Cperc = .55
# in 1 cm2 surface area
C0_depth = Cperc*rho #g/cm
C0 = C0_depth*step #grams of carbon in one threshold slice
Ctot[0] = C0
for i in range(0, thres_pts):
    thres[i] = sample
    sample += step
    #set carbon production to C0 for first time step
    carbon_series[i, 0] = C0
    emission_series[i, 0] =0

beats = 0
for tt in range(0, N-1):
    for ii in range(0, thres_pts):
        sumC_tt_1 = carbon_series[ii,tt]
        sum_em = emission_series[ii, tt]
        if thres[ii] < water_table_series[tt]: #inundation
            tlag = 2 #days
            #DMC[ii, tt] = 1
            beats += 1
            time_inundated = beats*dt
            if time_inundated >= tlag:
                krate = -0.002 #*3600*24 #aeration carbon rate, 1/days
            else:
                krate = 0
        else: #aeration
            beats = 0
            krate = -0.008 #*3600*24
            tlag = 0
            #DMC[ii, tt] = 0
        Cnew = carbon_series[ii, tt]/(1-krate*dt)
        emission_series[ii, tt+1] = -Cnew*krate
        #print(Cnew)
        if Cnew != 'inf':
            if Cnew >= 0:
                carbon_series[ii, tt+1] = Cnew
            else:
                carbon_series[ii, tt+1] = 0
        else:
            carbon_series[ii, tt+1] = 1000
        sumC_tt_1 += carbon_series[ii, tt+1]
        sum_em += emission_series[ii, tt+1]
    Ctot[tt+1] = sumC_tt_1
    emissions_total[tt+1] = sum_em

#print(carbon_series[1,:])
#plt.figure(); plt.plot(Ctot)
#plt.figure(); plt.plot(carbon_series[3,:], 'r') #over time
#plt.figure()
#for j in np.arange(0,N,100):
    #plt.plot(carbon_series[:,j], 'r') #per threshold value
#plt.figure()
#for j in np.arange(0,N,100):
    #plt.plot(emission_series[:,j], 'r') #per threshold value
#plt.show()

#define integral of simulation pdf (histogram)
def hist_cdf(x, wt_series):
    n_, bins_, patch = plt.hist(wt_series, 50, histtype='bar', rwidth=0.5, normed=True, cumulative=True)
    np_, binsp_, patch = plt.hist(wt_series, 50, histtype='bar', rwidth=0.5, normed=True)
    cdf_x = 0 
    pdf_x = 0 
    for i in range(0, len(bins_)):
        if x >= bins_[i]:
            cdf_x = n_[i-1]
            pdf_x = np_[i-1]
        else:
            None
    if x>= binsp_[-1]:
        pdf_x = 0
    else:
        None
    return pdf_x, cdf_x

##SIMULATION MCTs
##define threshold depth
#thres_pts = readings
##step = math.floor((max_y - min_y)/thres_pts)
#step = (max_y - min_y)/thres_pts
#thres = np.zeros(thres_pts)
#MCTs = np.zeros(thres_pts)
#y_start = min_y
#sample = math.ceil(y_start) #change to floor and adjust lower bound
#from itertools import groupby
#from operator import itemgetter
#print(groupby([1,2,3], [3,2,4]))
#for i in range(0, thres_pts):
    ##pdf, cdf = hist_cdf(sample, water_table_series)
    ##beta, ET, f1, det = simulation_paramters(sample, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    ###the loss for the additive noise process x:
    ##loss = (ET - f1)/beta
    ##MCTs[i] = cdf/(pdf*loss)
    ##thres[i] = sample
    ##sample += step
    #durations = []
    #below_times = np.where(water_table_series<sample)[0]
    #for k, g in groupby(enumerate(below_times), lambda ix: ix[0]-ix[1] ):
        ## find consecutive groups of numbers, take the length of groups to represent duration under threshold
        #durations.append( len(list(map(itemgetter(1), g))) )
    #MCTs[i] = np.mean(np.array(durations)*dt)
    #thres[i] = sample
    #sample += step

##hist makes no sense like this
##need a different hist for each threshold depth
#plt.hist(MCTs, 50, histtype='bar', rwidth=0.5, normed=True)
#plt.show()
sub_dir = 'g/carbon_flux/'
name0 = 'g/direct_C/sim_mcts_' + soil_type + '.png'
name1 = 'g/direct_C/sim_wt_' + soil_type + '.png'
name2 = 'g/direct_C/sim_hist_' + soil_type + '.png'
#name3 = 'g/sim_mcts_analytic_form_' + soil_type + '.png'
name4 = 'g/direct_C/sim_hist_mcts_' + soil_type + '.png'
name5 = 'g/direct_C/sim_histcdf_' + soil_type + '.png'

name1c = sub_dir + 'timeseries_' + soil_type + '.png'
name2c = sub_dir + 'emissions_vs_depth_' + soil_type + '.png'
name3c = sub_dir + 'production_vs_depth_' + soil_type + '.png'

#for j in np.arange(0,N,100):
    #plt.plot(carbon_series[:,j], 'r') #per threshold value
#plt.figure()
#for j in np.arange(0,N,100):
    #plt.plot(emission_series[:,j], 'r') #per threshold value
#plt.show()

fig1 = plt.figure()
plt.figure(1)
plt.plot(time_days, Ctot, 'b', label='peatland carbon production')
plt.plot(time_days, emissions_total, 'r', label='peatland carbon emissions')
plt.xlabel('time (days)')
plt.ylabel('net carhbon over all layers (g)')
plt.title('Peatland carbon time series')
#plt.savefig(name1c)
#plt.close(fig1)

fig2 = plt.figure()
plt.figure(2)
for j in np.arange(0,N,100):
    plt.plot(thres, emission_series[:,j], 'r') #per threshold value
#plt.show()
plt.xlabel('threshold depth (cm)')
plt.ylabel('carbon emissions (g)')
plt.title('Peatland carbon emissions')
#plt.savefig(name2c)
#plt.close(fig2)

fig3 = plt.figure()
plt.figure(3)
for j in np.arange(0,N,100):
    plt.plot(thres, carbon_series[:,j], 'r') #per threshold value
#plt.show()
plt.xlabel('threshold depth (cm)')
plt.ylabel('carbon production (g)')
plt.title('Peatland carbon production')
plt.show()
#plt.savefig(name3c)
#plt.close(fig3)

##fig0 = plt.figure()
##plt.figure(0)
##plt.plot(thres, MCTs)
##plt.title("Mean Crossing Times vs Threshold Depth")
##plt.xlim(min_y, 0)
##plt.ylim(0,50)
##plt.xlabel('Soil depth (cm)')
##plt.ylabel('Mean times of aeration (days)')
###plt.ylabel("Mean crossing time (days) ")
###plt.xlabel("Depth, z (cm)")
##plt.show()
##plt.savefig(name0)
##plt.close(fig0)

#fig1 = plt.figure()
#plt.figure(1)
#plt.plot(water_table_series)
#plt.xlabel('time (days)')
#plt.ylabel('depth of water table (cm)')
#plt.title('Water table time series')
#plt.savefig(name1)
#plt.close(fig1)

#fig2 = plt.figure()
#plt.figure(2)
#plt.hist(water_table_series, 50, histtype='bar', rwidth=0.5, normed=True)
#plt.xlabel('water table depth (cm)')
#plt.ylabel('frequency (normalized)')
#plt.title('Water table simulation histogram')
#plt.savefig(name2)
#plt.close(fig2)

#fig5 = plt.figure()
#plt.figure(5)
#plt.hist(water_table_series, 50, histtype='bar', rwidth=0.5, normed=True, cumulative=True)
#plt.xlabel('water table depth (cm)')
#plt.ylabel('cumulative frequency (normalized)')
#plt.title('Water table simulation cumulative histogram')
#plt.savefig(name5)
#plt.close(fig5)

##fig3 = plt.figure()
##plt.figure(3)
##plt.plot(thres, MCTs)
##plt.title("Mean Crossing Times vs Threshold Depth")
##plt.ylabel("Mean crossing time (days) ")
##plt.xlabel("Depth, z (cm)")
##plt.savefig(name3)
##plt.close(fig3)

##fig4 = plt.figure()
##plt.figure(4)
##plt.hist(MCT_thres_a, 50, histtype='bar', normed=True)
##plt.xlabel('mean crossing time (days)')
##plt.ylabel('frequency (normalized)')
##plt.title('MCTs histogram')
##plt.savefig(name4)
##plt.close(fig4)

###quick latex output for graphs
##names = [name1, name2, name3, name4]
##for i in range(0, len(names)):
    ##print('\\begin{figure}[!htb]')
    ##print('\\centering')
    ##print('\\includegraphics[width=.85\\textwidth]{' + names[i] + '}')
    ##print('\\end{figure}')
