
#Rachel Lonchar
#Project 1: Stochastic simulations of the soil-plant atmosphere continuum (SPAC)

#Parameter dictionaries:

from pickle_funcs import *

sims = 1000

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

scenerio_dic = {}
def define_scenerios(scenerio_name,mean_frequency=0.1, mean_intensity=10,years=sims, dt=0.1,
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

#-----------------------------------------------------
#project 1, part 1 scenerios
define_scenerios('1',mean_frequency=0.2)
define_scenerios('2',zr=10)
define_scenerios('3',ETmax=2)
save_obj(scenerio_dic,'scenerios_from_pt_1')

#-------------------------------------------------------------------------
#project 1, part 2 plant species
plant_species = {}
def add_species(species_name,gmax='',kmax='',psi50='',beta='',a='',Zr='',Ar=''):
    plant_specie = {}
    plant_specie.update({'gmax':gmax})
    plant_specie.update({'kmax':kmax})
    plant_specie.update({'psi50':psi50})
    plant_specie.update({'beta':beta})
    plant_specie.update({'a':a})
    plant_specie.update({'Zr':Zr})
    plant_specie.update({'Ar':Ar})
    plant_species.update({species_name:plant_specie})
add_species('trait names',gmax='maximum canopy conductance',kmax='maximum step conductance',
    psi50='plant water potential at 50% loss in stem conductance',
    beta='sensitivity of canopy conductance to water potential',
    a='sensitivity of stem conductance to water potential',
    Zr='rooting depth', Ar='rooting area')
add_species('units',gmax='m3/day',kmax='m3/(day-MPa)',psi50='MPa',Zr='m',Ar='m2')
add_species('Species 1',gmax=0.2,kmax=0.002,psi50=-3,beta=1,a=1,Zr=0.3,Ar=1)
add_species('Species 2',gmax=0.2,kmax=0.002,psi50=-1,beta=1,a=1,Zr=1.5,Ar=1)
save_obj(plant_species,'plant_species')
