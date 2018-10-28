#Project 1

#Part 2, plots

from part_23_funcs import *

def store_realizations(species='Species 1',VPD=2,soil_type='loamy sand soil',realizations=100):
    v = scenerio_dic['baseline']
    dic = {}
    for rr in range(0,realizations):
        scenerio = rain_events(mean_frequency=v['lam'],mean_intensity=v['alph'], years=1, dt=v['dt'])
        sim_dic = soil_moisture_series(scenerio,soil_type,s0=v['s0'],species=species,VPD=VPD,dt=v['dt'],yrs=1)#,zr=v['zr'])
        dic.update({rr:sim_dic})
    return dic

ultimate_arch = {}
realization_storage = {}
soilz, vps = {},{}

Species_1_relz = store_realizations()
Species_2_relz = store_realizations(species='Species 2')
realization_storage.update({'Species 1':Species_1_relz})
realization_storage.update({'Species 2':Species_2_relz})
vps.update({2:realization_storage})
#-
realization_storage = {}
Species_1_relz = store_realizations(VPD=4)
Species_2_relz = store_realizations(species='Species 2',VPD=4)
realization_storage.update({'Species 1':Species_1_relz})
realization_storage.update({'Species 2':Species_2_relz})
#-
vps.update({4:realization_storage})
soilz.update({'loamy sand soil':vps})

#----------------------------------------------------------------
vps = {}
realization_storage = {}
Species_1_relz = store_realizations(soil_type='sandy soil')
Species_2_relz = store_realizations(species='Species 2',soil_type='sandy soil')
realization_storage.update({'Species 1':Species_1_relz})
realization_storage.update({'Species 2':Species_2_relz})
vps.update({2:realization_storage})
#-
realization_storage = {}
Species_1_relz = store_realizations(VPD=4,soil_type='sandy soil')
Species_2_relz = store_realizations(species='Species 2',VPD=4,soil_type='sandy soil')
realization_storage.update({'Species 1':Species_1_relz})
realization_storage.update({'Species 2':Species_2_relz})
#save_obj(realization_storage,'loamy_sims_4kpa')
vps.update({4:realization_storage})
soilz.update({'sandy soil':vps})

ultimate_arch = soilz
save_obj(ultimate_arch,'stored')




