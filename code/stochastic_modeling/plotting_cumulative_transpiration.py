#Project 1

#Part 2, plots

from pickle_funcs import *
import math
sims = load_obj('stored')
scenerio_dic = load_obj('scenerios_from_pt_1')
#from part_2_sm_simulation_funcs import *
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

        
def plot_sm_T(*soil_VPDs,name_fig,plt_type_x='soil moisture',plt_units_x='',
    plt_type='transpiration',plt_units=' (mm)',
    sub_titles=0,sub_units='',sub_heading='',
    species='Species 1',realizations=10):
    
    cols,rows = 1,len(soil_VPDs)
    #colors = ['yellow','blue']
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(15,9))
    v = scenerio_dic['baseline']
    plotn = 1
    for sc in soil_VPDs:
        soil_type, VPD = sc[0], sc[1]
        simuls = sims[soil_type][VPD]
        for rr in range(0,realizations):
            sim_dic = simuls[species][rr]
            xx,sm = sim_dic[plt_type_x], sim_dic[plt_type]
            plt.subplot(cols,rows,plotn)
            plt.plot(xx,sm,'b.')
        plt.title(sub_heading+str(sc[sub_titles])+sub_units)
        plotn += 1
        #plt.ylim(ymin=0,ymax=ytop)
        plt.xlim(xmin=0,xmax=1)
    fig.text(0.5, 0.04,plt_type_x+plt_units_x, ha='center',fontdict=font)
    fig.text(0.04, 0.5, plt_type+plt_units, va='center', rotation='vertical',fontdict=font)
    plt.suptitle('Relationship between soil moisture and transpiration\n'+species,fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    plt.savefig('g/'+name_fig)
    #plt.show()

def plot_sm(species):
    #1
    soil1 = 'loamy sand soil'
    soil2 = soil1
    vp1 = 2
    vp2 = 4
    plot_sm_T([soil1,vp1],[soil2,vp2],name_fig='23/sm_T_kpa_sp'+species[-1],
        sub_titles=1,sub_units=' kPa',sub_heading='vapor pressure deficit=',
        species=species)
    #2
    soil1 = 'loamy sand soil'
    soil2 = 'sandy soil'
    vp1 = 2
    vp2 = vp1
    plot_sm_T([soil1,vp1],[soil2,vp2],name_fig='23/sm_T_soil_sp'+species[-1],
        sub_titles=0,sub_units='',sub_heading='',species=species)
    #plt.show()

def plot_time_series(*species_,name_fig,plt_type,plt_units='',
    soil_type='loamy sand soil',VPD=2,
    realizations=10):
    
    cols,rows = 1,len(species_)
    #colors = ['yellow','blue']
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(15,9))
    v = scenerio_dic['baseline']
    plotn = 1
    for species in species_:
        simuls = sims[soil_type][VPD]
        for rr in range(0,realizations):
            sim_dic = simuls[species][rr]
            time,sm = sim_dic['time series'], sim_dic[plt_type]
            plt.subplot(cols,rows,plotn)
            plt.plot(time,sm)
            plt.title(species)
        plotn += 1
    fig.text(0.5, 0.04,'time (days)', ha='center',fontdict=font)
    fig.text(0.04, 0.5, plt_type+plt_units, va='center', rotation='vertical',fontdict=font)
    plt.suptitle(plt_type +' for '+soil_type,fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    plt.savefig('g/'+name_fig)
    #plt.show()

def plot_series(plot_variable='soil moisture'):
    var=plot_variable
    plot_v_units = ' (unitless)' if var!='plant water potential' else ' (MPa)'
    plot_v_units = plot_v_units if var!='transpiration' else ' (mm)'
    name_plt = 'sm_' if var=='soil moisture' else 'T_'
    name_plt = name_plt if var!='plant water potential' else 'pw_'
    plot_time_series('Species 1','Species 2',name_fig='23/time_'+name_plt,
        plt_type=plot_variable, plt_units=plot_v_units,realizations=10)

def plot_his(*species_,name_fig='',plt_type='',plt_units='',
    soil_type='loamy sand soil',VPD=2,
    realizations=100):
    
    cols,rows = 1,1#len(scenerios)
    colors = ['yellow','blue']
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(9,9))
    plotn = 1
    times,sms,maxers = [],[],[]
    v = scenerio_dic['baseline']
    #ymaxs=[]
    for species in species_:
        #species,soil_type, VPD = sc[0], sc[1],sc[2]
        simuls = sims[soil_type][VPD]
        holder = []
        for rr in range(0,realizations):
            sim_dic = simuls[species][rr]
            trans = sim_dic['transpiration']
            cum_trans = sum(trans)#cum_tran(trans)
            holder = np.append(holder,cum_trans)
        plt.subplot(cols,rows,1)
        plt.hist(holder, 15, color=colors[plotn-1],alpha=0.6,histtype='bar',  normed=True,
            label=species)
        plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':10})
        plotn += 1
    fig.text(0.5, 0.04,'cumulative annual transpiration (meters)', ha='center',fontdict=font)
    fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical',fontdict=font)
    plt.suptitle('Cumulative transpiration distribution for plants in '+soil_type+'\nwith a vapor pressure deficit='+str(VPD)+' kPa',
        fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    plt.savefig('g/23/'+name_fig)
    #plt.show()

plot_his('Species 1','Species 2',name_fig='3_base')
plot_his('Species 1','Species 2',name_fig='3_VPD',VPD=4)
plot_his('Species 1','Species 2',name_fig='3_soil',soil_type='sandy soil')

#soil moisture vs. transpiration:
for idx in [1,2]:
    plot_sm('Species '+str(idx))

#time series:
time_vs = ['soil moisture','transpiration','plant water potential']
for tv in time_vs:
    plot_series(tv)



##soil moisture
#plot_variable = 'soil moisture'
#plot_v_units = ''
#name_plt = 'sm_'
##ET:
#plot_variable = 'transpiration'
#plot_v_units = ' (unitless)'
#name_plt = 'T_'
#plant water potential:




