
#Rachel Lonchar
#Project 1: Stochastic simulations of the soil-plant atmosphere continuum (SPAC)

#Part 2: Stochastic rainfall-soil moisture simulations with more precise ET

from pickle_funcs import *
import math

#import parameter data:
soils = load_obj('soil_parameters')
scenerio_dic = load_obj('scenerios_from_pt_1')
plant_species = load_obj('plant_species')

#define ET functions:
from scipy.optimize import fsolve
def g_s(psi,species):
    dic = plant_species[species]
    gmax,beta = dic['gmax'],dic['beta'] #gmax --> m/day
    gs = gmax*1/(np.exp((-psi/beta)**beta)) #psi --> MPa
    return gs
def phi(psi,species):
    dic = plant_species[species]
    kmax,a,psi50 = dic['kmax'],dic['a'],dic['psi50'] #kmax --> m/(day MPa)
    phi_ = kmax*(psi + 1/a*np.log(np.exp(-a*psi) + np.exp(-a*psi50)) )
    return phi_
    
#transpiration rates, in m/day:
def T1(psi_p,VPD,species):             #input VPD in kPa
    return g_s(psi_p,species=species)*VPD/101.325  #make D unitless by dividing VPD by atmospheric pressure
def T2(psi_p,psi_s,species):
    phi1 = phi(psi_s,species=species)
    phi2 = phi(psi_p,species=species)
    return phi1 - phi2
#convert soil moisture to soil water potential:
def psi_s_sm(sm, soil_type):
    b,psi_sat = soils[soil_type]['b'], soils[soil_type]['psi_sat']
    return psi_sat*sm**(-b) #MPa
    
def T_dif(s0,VPD,species,soil_type):
    psi_s0 = psi_s_sm(s0,soil_type=soil_type)
    def newT(psi): return T1(psi,VPD,species=species) - T2(psi,psi_s=psi_s0,species=species) #psi in MPa
    return newT 
def ET_better(s0,soil_type,species,VPD):
    psi_s0 = psi_s_sm(s0,soil_type=soil_type)
    psi_px = fsolve(T_dif(s0,VPD=VPD,species=species,soil_type=soil_type),0.01)[0]
    transpiration = T2(psi_px,psi_s=psi_s0,species=species)
    return transpiration, psi_px

#defining rain series function based on lamda alpha parameters
def rain_events(mean_frequency, mean_intensity, years, dt):
    N = math.ceil(years*365/dt)
    lam = mean_frequency #mean freq = 1/(mean period) e.g. 1/(mean wait time)
    alpha = mean_intensity/1000 #convert intensity to meters
    depths = np.random.exponential(alpha, N)
    event_markers = np.random.random(N)
    rain_events_ = event_markers < (lam)*dt
    rain_series = np.zeros(N)
    rain_series[rain_events_] = depths[rain_events_] 
    return rain_series

def s_star(s0,rain_depth,soil_type,species,VPD,dt):#,zr=50):#ETmax=1.5,dt=0.1,zr=50):
    Zr = plant_species[species]['Zr'] #m
    porosity = soils[soil_type]['n']
    ET_star_,psi_px = ET_better(s0,soil_type=soil_type,species=species,VPD=VPD) #m/day
    ET_star = ET_star_*dt/(porosity*Zr) #[m/day][days/m] --> unitless
    s_bulk = (rain_depth)/(porosity*Zr) - ET_star + s0
    return s_bulk, ET_star_*dt*1000, psi_px
#print(s_star(0.3,0))

def soil_moisture_series(rain_series,soil_type,s0,species,VPD,dt,yrs):
    n = soils[soil_type]['n']
    Zr = plant_species[species]['Zr'] #m
    
    sm_series,days_series = np.zeros_like(rain_series),np.zeros_like(rain_series)
    ET_series, L_series, ps_series = np.zeros_like(rain_series),np.zeros_like(rain_series),np.zeros_like(rain_series)
    s1,t_days = s0,0
    for idx in range(0,len(rain_series)):
        s_pre,ET_series[idx],ps_series[idx] = s_star(s1,rain_series[idx],soil_type=soil_type,species=species,VPD=VPD,dt=dt)#,zr=zr)
        if (s_pre>=0 and s_pre<1):
            s2,Leak_term = s_pre,0
        elif s_pre>=1:
            Leak_term = (s_pre-1)*dt/(n*Zr)
            s2 = 1
        else:
            s2 = 0
        L_series[idx] = Leak_term
        sm_series[idx] = s2
        s1 = s2
        t_days += dt
        days_series[idx] = t_days
    dicsm = {}
    dicsm.update({'soil moisture':sm_series})
    #dicsm.update({'leakage':L_series})
    dicsm.update({'transpiration':ET_series})
    dicsm.update({'time series':days_series})
    dicsm.update({'plant water potential':ps_series})
    return dicsm


