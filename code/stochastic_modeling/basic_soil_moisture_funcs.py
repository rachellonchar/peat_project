#Rachel Lonchar
#Project 1: Stochastic simulations of the soil-plant atmosphere continuum (SPAC)

#Part 1: Stochastic rainfall-soil moisture simulations

#import numpy as np
#import matplotlib.pyplot as plt
from pickle_funcs import *
import math
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
#defining rain series function based on lamda alpha parameters
def rain_events(mean_frequency, mean_intensity, years, dt):
    N = math.ceil(years*365/dt)
    lam = mean_frequency #mean freq = 1/(mean period) e.g. 1/(mean wait time)
    alpha = mean_intensity
    depths = np.random.exponential(alpha, N)
    event_markers = np.random.random(N)
    rain_events_ = event_markers < (lam)*dt
    rain_series = np.zeros(N)
    rain_series[rain_events_] = depths[rain_events_]
    return rain_series

def s_star(s0,porosity,rain_depth,ETmax=1.5,dt=0.1,zr=50):
    return (rain_depth - (ETmax*s0*dt))/(porosity*zr) + s0

#make soil type dictionaries
soils = {}
names = ['porosity','saturated hydraulic conductivity (mm/day)','water retention parameter','soil water potential near saturation (MPa)']
soils.update({'calls':names})
def add_to_soils(soil_name,n,Ksat,b,psi_sat):
    loamy = {}
    loamy.update({'n':n}) #porosity
    loamy.update({'Ksat':Ksat}) #saturated hydraulic conductivity, mm/day
    loamy.update({'b':b}) #water retention parameter
    loamy.update({'psi_sat':psi_sat}) #soil water potential near saturation, MPa
    soils.update({soil_name:loamy})
add_to_soils('parameters',names[0],names[1],names[2],names[3])
add_to_soils('loamy sand soil',0.45,10,4.38,-0.17*10**(-3))
add_to_soils('sandy soil',0.35,20,4.05,-0.34*10**(-3))
save_obj(soils,'soil_parameters')

def soil_moisture_series(rain_series,soil_type,s0,ETmax,dt,zr):
    n = soils[soil_type]['n']
    sm_series,days_series = np.zeros_like(rain_series),np.zeros_like(rain_series)
    ET_series, L_series = np.zeros_like(rain_series),np.zeros_like(rain_series)
    s1,t_days = s0,0
    for idx in range(0,len(rain_series)):
        ET_series[idx] = ETmax*s1
        s_pre = s_star(s1,n,rain_series[idx],ETmax=ETmax,dt=dt,zr=zr)
        if (s_pre>=0 and s_pre<1):
            s2,Leak_term = s_pre,0
        elif s_pre>=1:
            Leak_term = (s_pre-1)*dt/(n*zr)
            s2 = 1#s_pre - Leak_term
        else:
            s2 = 0
            #print('error: cannot have negative soil moisture',s1,s_pre)
        L_series[idx] = Leak_term
        sm_series[idx] = s2
        s1 = s2
        t_days += dt
        days_series[idx] = t_days
    dicsm = {}
    dicsm.update({'soil moisture':sm_series})
    dicsm.update({'leakage':L_series})
    dicsm.update({'evapotranspiration':ET_series})
    dicsm.update({'time series':days_series})
    return dicsm
    
import scipy.special
def steady_state_pdf(s,soil_type,ETmax=1.5, zr=50,mean_frequency=0.1, mean_intensity=10):
    lam = mean_frequency #mean freq = 1/(mean period) e.g. 1/(mean wait time)
    alpha = mean_intensity
    n = soils[soil_type]['n']
    nu,gam = ETmax/(n*zr),(n*zr)/alpha
    a,x = lam/nu, gam
    d1 = scipy.special.gammainc(a,x)
    d2 = scipy.special.gamma(a)
    denom = d1*d2
    pbs = s**(a-1)*gam**a*np.exp(-gam*s)/denom
    return pbs

scenerio_dic = {}
def define_scenerios(scenerio_name,mean_frequency=0.1, mean_intensity=10,years=1000, dt=0.1,
    s0=0.3, ETmax=1.5, zr=50):
    hold = {}
    hold.update({'lam':mean_frequency})
    hold.update({'alph':mean_intensity})
    hold.update({'years':years})
    hold.update({'dt':dt})
    hold.update({'s0':s0})
    hold.update({'ETmax':ETmax})
    hold.update({'zr':zr})
    scenerio_dic.update({scenerio_name:hold})
define_scenerios('baseline')

def plotting(*scenerios, soil_type,name_fig,sub_titles,plt_type):
    
    cols,rows = 1,1#len(scenerios)
    colors = ['yellow','blue']
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(9,9))
    plotn = 1
    times,sms,maxers = [],[],[]
    ymaxs=[]
    for sc in scenerios:
        v = scenerio_dic[sc]
        scenerio = rain_events(mean_frequency=v['lam'],mean_intensity=v['alph'], years=v['years'], dt=v['dt'])
        sim_dic = soil_moisture_series(scenerio,soil_type,dt=v['dt'],s0=v['s0'],ETmax=v['ETmax'],zr=v['zr'])
        time = sim_dic['time series']
        sm = sim_dic[plt_type]
        times.append(time)
        sms.append(sm)
        plt.subplot(cols,rows,1)
        #int(4000/v['zr'])
        plt.hist(sm, 20, color=colors[plotn-1],alpha=0.6,histtype='bar',  normed=True,
            label='normalized histogram, '+str(v['years'])+' yrs with time-step='+str(v['dt'])+' days')
        save_obj(sm,plt_type+'_ts_'+sc)

        maxer = 1 if plt_type=='soil moisture' else v['ETmax']
        maxers.append(maxer)
        sm_range = np.linspace(0,maxer,50) 
        if plt_type=='soil moisture':
            def pdf_fun(s): return steady_state_pdf(s,soil_type,ETmax=v['ETmax'],zr=v['zr'],mean_frequency=v['lam'],mean_intensity=v['alph'])
            sm_pdf = [pdf_fun(s) for s in sm_range]
            plt.plot(sm_range,sm_pdf,colors[plotn-1],alpha=1,label='steady state pdf')
        plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':10})
        ymaxs.append(1.1*max(sm))
        plt.title(sub_titles[plotn-1])
        plotn += 1
    fig.text(0.5, 0.04,plt_type, ha='center',fontdict=font)
    fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical',fontdict=font)
    plt.suptitle(plt_type +' for '+soil_type,fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    plt.savefig('g/'+name_fig)

#1.
define_scenerios('1',mean_frequency=0.2)
subt=['frequency=0.1/day','frequency=0.2/day']
plotting('baseline','1',soil_type='loamy sand soil',name_fig='1_loam',sub_titles=subt,plt_type='soil moisture')
plotting('baseline','1',soil_type='loamy sand soil',name_fig='1_loamE',sub_titles=subt,plt_type='evapotranspiration')

#2.
define_scenerios('2',zr=10)
subt=['rooting depth=50mm','rooting depth=10mm']
plotting('baseline','2',soil_type='loamy sand soil',name_fig='2_loam',sub_titles=subt,plt_type='soil moisture')
plotting('baseline','2',soil_type='loamy sand soil',name_fig='2_loamE',sub_titles=subt,plt_type='evapotranspiration')

#3.
define_scenerios('3',ETmax=2)
subt=['potential ET=1.5mm','potential ET=2mm']
plotting('baseline','3',soil_type='loamy sand soil',name_fig='3_loam',sub_titles=subt,plt_type='soil moisture')
plotting('baseline','3',soil_type='loamy sand soil',name_fig='3_loamE',sub_titles=subt,plt_type='evapotranspiration')

save_obj(scenerio_dic,'scenerios_from_pt_1')
def analytic_pdf(soil_type,scenerio='baseline'):
    v = scenerio_dic[scenerio]
    def pdf_fun(s): return steady_state_pdf(s,soil_type,ETmax=v['ETmax'],zr=v['zr'],mean_frequency=v['lam'],mean_intensity=v['alph'])
    return pdf_fun
    


