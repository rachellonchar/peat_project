
from definitions import *
cwd = os.getcwd()

def per(Xvar,threshold):
    if Xvar=='period of aeration':
        Xvar = ['period of aeration',threshold]
    elif Xvar=='period of inundation':
        Xvar = ['period of inundation',threshold]
    return Xvar

def slope_at_thresholds(thresholds_array=[0,5,7,8,10],Xvar='period of aeration',Yvar='CH4_S1',color='NTs10',col_map='coolwarm',
    deviations_predictor='NTs10',dev_fit_type=btf.func_exp,mask_events='inundated',show_masked_pts=0,
    pic_name=None, pic_folder_name=None,save_or_show='show',cwd=cwd,deviations_applied_to='y'):
        
    if Xvar=='period of aeration' or Yvar=='period of aeration':
        mask_events = 'inundated'
    if Xvar=='period of inundation' or Yvar=='period of inundation':
        mask_events = 'aerated'
    #thresholds_array = np.append(max(v['WT'])+1,thresholds_array) if mask_events=='inundated' else np.append(min(v['WT'])-1,thresholds_array)
    t_e = 'aerated' if mask_events=='inundated' else 'inundated'
    num_plots=len(thresholds_array)
    cols = math.floor(np.sqrt(num_plots))
    rows = math.ceil(num_plots/cols)
    if cols<rows:
        f1,f2=11.7,8.3
    else:
        f1,f2=8.3,11.7
    if type(deviations_predictor) != type(None):
        if deviations_applied_to=='y':
            Y = deviations_from_fit(deviations_predictor, Yvar, fit_type=dev_fit_type,mask=None)
        else:
            Y = notation_fix(Yvar)
        if deviations_applied_to=='x':
            X = deviations_from_fit(deviations_predictor, Xvar, fit_type=dev_fit_type,mask=None)
            Xvar = 'dev'
        else:
            None
        if deviations_applied_to=='c':
            ColorV = deviations_from_fit(deviations_predictor, color, fit_type=dev_fit_type,mask=None)
        else:
            ColorV = notation_fix(color)
    else:
        Y,ColorV = notation_fix(Yvar),notation_fix(color)
    maxD, minD = max(ColorV), min(ColorV)
    norm = matplotlib.colors.Normalize(vmin=minD, vmax=maxD, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=plt.cm.get_cmap(col_map))
    mapper.set_array([])
    minY,maxY = min(Y),max(Y)
    fig, ax = plt.subplots(ncols=cols,nrows=rows,  sharex=True, sharey=True, figsize=(f1,f2))
    ct = 1
    for threshold in thresholds_array:
        plt.subplot(cols,rows,ct)
        if mask_events=='inundated' or mask_events=='aerated':
            mask,dic,ndic = notation_fix(['mask','mask '+mask_events+' events',threshold],ret_dics=1)
        else:
            mask = [0 for idx in range(0,len(Y))] #masks nothing
            dic,ndic = v,n
        def nf(string): return notation_fix(string,dic=dic,naming_dic=ndic)
        #Xvar,Yvar,color = per(Xvar,threshold),per(Yvar,threshold),per(color,threshold)
        Xvar = per(Xvar,threshold)
        if Xvar != 'dev':
            X = nf(Xvar)
        fun, print_fun = btf.lin_fit(X,Y,mask=mask,type_return='function and print')
        Xexp,Yexp = btf.array_span(X, fun,dense=1,specify_points=20)
        if show_masked_pts==1:
            plt.scatter(X,Y,c='white',edgecolor='darkgrey')
        
        Xmsk = np.ma.masked_array(X,mask=mask)
        Ymsk = np.ma.masked_array(Y,mask=mask)
        plt.plot(Xexp,Yexp,'r',label=print_fun)
        col_msk = np.ma.masked_array(ColorV,mask=mask)
        bill = [mapper.to_rgba(val) for val in col_msk.compressed()]
        plt.scatter(Xmsk.compressed(),Ymsk.compressed(),s=30,c=bill,cmap=mapper,
            edgecolor=bill,vmin=minD,vmax=maxD,label='all '+t_e+' events')
        plt.legend(loc=2,ncol=1, fancybox=True,prop={'size':10})
        #if ct>1:
        plt.title('threshold='+str(threshold))
        if type(Xvar)==str and (Xvar=='WT' or Xvar=='NWT'):
            plt.vlines(threshold,minY,maxY)
        #else:
            #plt.title('no masking')
        plt.ylim(ymin=minY,ymax=maxY)
        if type(Xvar)==list:
            if Xvar[0]=='period of aeration':
                plt.xlim(xmin=0,xmax=41)
        else:
            plt.xlim(xmin=min(Xexp),xmax=max(Xexp))
        plt.colorbar(mapper,label='soil temp')
        plt.grid()
        ct+=1
    fig.text(0.5, 0.04,list_to_name(Xvar,base=1)+' of '+t_e+' events', ha='center',fontdict=font)
    fig.text(0.04, 0.5, 'CH4 residuals (based on soil temp at -10 cm)', va='center', rotation='vertical',fontdict=font)
    plt.suptitle('Sensitivity to water table at different threshold definitions of '+t_e+' events',fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    if pic_name==None:
        if save_or_show=='save':
            
            plt.savefig(gn(), bbox_inches='tight')
            plt.close(fig)
        else:
            plt.show()
    else:
        pnam = pic_namer(pic_name, pic_folder_name)
        plt.savefig(gn(pic_name,pic_folder_name), bbox_inches='tight')
        
#slope_at_thresholds(Xvar='period of inundation',Yvar='WT',color='NCH4_S1',deviations_applied_to='c',save_or_show='show',col_map='Blues')
from marked_poisson_process import *

#for thres in [0,3,5,7,9,10,11,12]:
    #depths_array,arrival_times = time_series(notation_fix(['period of aeration',thres]))
    #fit_exp(depths_array,arrival_times,save_or_show='hold')
#plt.show()

#depths_array,arrival_times = time_series(notation_fix('WT'))
#fit_exp(notation_fix('WT'),save_or_show='hold')
plt.hist(notation_fix('WT'), 50, histtype='bar',  normed=True)#,label='histogram of actual rainfall depths')
plt.show()










##plot function
#from scipy.stats import expon, gamma
#def fit_exp(Xvar,waiting_times=None,name_fig='exp',mask=None):
    #XX = notation_fix(Xvar)
    ##print(depths)
    ##mean_time = sum(waiting_times) / len(waiting_times)
    ##if max(depths)>40:
        ##bars = math.ceil(max(depths))
    ##else:
        ##bars = 40
    #mask_events = 'aerated'
    #mask,dic,ndic = notation_fix(['mask','mask '+mask_events+' events',9],ret_dics=1)
    #bars=30
    ##if mask!=None:
    #Xmsk = np.ma.masked_array(XX,mask=mask)
    #depths = Xmsk.compressed()
    ##else:
        ##depths = XX
    #mean_depth = sum(depths) / len(depths)
    
    #if type(waiting_times)==type(None):
        #fig, ax = plt.subplots(ncols=1,nrows=1,  sharex=True, sharey=True, figsize=(9,9))
        #plt.subplot(1,1,1)
    #else:
        #fig, ax = plt.subplots(ncols=1,nrows=2,  sharex=True, sharey=True, figsize=(17,9))
        #plt.subplot(1,2,1)
    #plt.hist(depths, bars, histtype='bar',  normed=True,label='histogram of actual rainfall depths')
    #loc, scale = expon.fit(depths.astype(np.float64), floc=0)
    #x = np.linspace(expon.ppf(0.01,loc=loc,scale=scale),expon.ppf(0.99,loc=loc,scale=scale), 100)
    #plt.plot(x, expon.pdf(x,loc=loc,scale=scale),'r-', lw=5, alpha=0.6, label='fitted pdf')
    #print_on = 'FIT PARAMETERS\nlocation paramter: '+str(loc)+'\nscale parameter: '+str(scale)
    #plt.annotate(print_on, xy=(40,.15), xycoords='data',color='darkred')
    #plt.annotate('actual mean event depth (mm):\n'+str(mean_depth),xy=(40,.1), xycoords='data',color='darkblue')
    #plt.legend()
    #plt.xlabel('depth (mm)')
    #plt.title('Rainfall depth fitted to an exponential distribution')
    #plt.grid()
    #plt.show()
    ##if type(waiting_times)!=type(None):
        ##plt.subplot(1,2,2)
        ##plt.hist(waiting_times, 30, histtype='bar',  normed=True,label='histogram of actual waiting times')
        ##loc, scale = expon.fit(waiting_times.astype(np.float64), floc=0)
        ##x = np.linspace(expon.ppf(0.01,loc=loc,scale=scale),expon.ppf(0.99,loc=loc,scale=scale), 100)
        ##plt.plot(x, expon.pdf(x,loc=loc,scale=scale),'r-', lw=5, alpha=0.6, label='fitting pdf')
        ##print_on = 'FIT PARAMETERS\nlocation paramter: '+str(loc)+'\nscale parameter: '+str(scale)
        ##plt.annotate(print_on, xy=(10,.3), xycoords='data',color='darkred')
        ##plt.annotate('actual mean waiting time between events (days):\n'+str(mean_time),xy=(10,.2), xycoords='data',color='darkblue')
        ##plt.legend()
        ##plt.xlabel('time between rainfall events (days)')
        ##plt.title('Waiting time for rainfall events fitted to an exponential distribution')
        ##plt.grid()
    ##fig.text(0.5, 0.04,'rainfall paramter', ha='center',fontdict=font)
    ##fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical',fontdict=font)
    ##plt.suptitle('Rainfall distributions',fontsize=16,fontdict=font)
    ##plt.tight_layout()
    ##plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    ##plt.savefig(name_fig)
#fit_exp(['period of inundation',9])


