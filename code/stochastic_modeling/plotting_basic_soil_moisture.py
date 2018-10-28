#Project 1

#Part 1, plots

from sm_simulation_funcs import *
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
        
def plotting(*scenerios, soil_type,name_fig,sub_titles,plt_type):
    
    cols,rows = 1,1#len(scenerios)
    colors = ['yellow','blue']
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(9,9))
    plotn = 1
    times,sms,maxers = [],[],[]
    #ymaxs=[]
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
            label=sub_titles[plotn-1])#'normalized histogram, '+str(v['years'])+' yrs with time-step='+str(v['dt'])+' days')
        #save_obj(sm,plt_type+'_ts_'+sc)

        maxer = 1 if plt_type=='soil_moisture' else v['ETmax']
        maxers.append(maxer)
        sm_range = np.linspace(0,maxer,50) 
        if plt_type=='soil_moisture':
            def pdf_fun(s): return steady_state_pdf(s,soil_type,ETmax=v['ETmax'],zr=v['zr'],mean_frequency=v['lam'],mean_intensity=v['alph'])
            sm_pdf = [pdf_fun(s) for s in sm_range]
            plt.plot(sm_range,sm_pdf,colors[plotn-1],alpha=1,label='steady state pdf')
        plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':10})
        #ymaxs.append(1.1*max(sm))
        #plt.title(sub_titles[plotn-1])
        plotn += 1
    fig.text(0.5, 0.04,plt_type, ha='center',fontdict=font)
    fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical',fontdict=font)
    plt.suptitle(plt_type +' for '+soil_type,fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    plt.savefig('g/'+name_fig)
    #plt.show()

#1.
subt=['frequency=0.1/day','frequency=0.2/day']
plotting('baseline','1',soil_type='loamy sand soil',name_fig='1_loam',sub_titles=subt,plt_type='soil_moisture')
plotting('baseline','1',soil_type='loamy sand soil',name_fig='1_loamE',sub_titles=subt,plt_type='evapotranspiration')

#2.
subt=['rooting depth=50mm','rooting depth=10mm']
plotting('baseline','2',soil_type='loamy sand soil',name_fig='2_loam',sub_titles=subt,plt_type='soil_moisture')
plotting('baseline','2',soil_type='loamy sand soil',name_fig='2_loamE',sub_titles=subt,plt_type='evapotranspiration')

#3.
subt=['potential ET=1.5mm','potential ET=2mm']
plotting('baseline','3',soil_type='loamy sand soil',name_fig='3_loam',sub_titles=subt,plt_type='soil_moisture')
plotting('baseline','3',soil_type='loamy sand soil',name_fig='3_loamE',sub_titles=subt,plt_type='evapotranspiration')
