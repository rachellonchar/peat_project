
##regular code directory setup:
#import sys, os, os.path
#cwd = os.getcwd()
#main_dirc = cwd.split('code', 1)[0]
#cwd_code = main_dirc + 'code'
#sys.path.insert(0, cwd_code+'/prelims')
#from save_funcs import *
##-------------------------------------------

#from water_table_functions import *
#from substrate_directory import *

#from preamble import *
from inundation_aeration_period_definitions import *

#def per(Xvar,threshold):
    #if Xvar=='period of aeration':
        #Xvar = ['period of aeration',threshold]
    #elif Xvar=='period of inundation':
        #Xvar = ['period of inundation',threshold]
    #return Xvar

#def namer(Xvar,dev=0):
    #ro = list_to_name(Xvar,base=1)
    #if dev==1:
        #ro = 'deviations of ' +ro
    #return ro
    

def slope_at_thresholds(thresholds_array=[-5,10,14.1,25],Xvar='period of aeration',Yvar='CH4_S1',color='NTs10',col_map='coolwarm',
    deviations_predictor='NTs10',dev_fit_type=btf.func_exp,mask_events='inundated',show_masked_pts=0,
    pic_name=None, pic_folder_name='net_inundation_aeration_periods',save_or_show='show',cwd=cwd,deviations_applied_to='y'):
        
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
            ndy,ndx,ndc = 1,0,0
        else:
            Y = notation_fix(Yvar)
        if deviations_applied_to=='x':
            X = deviations_from_fit(deviations_predictor, Xvar, fit_type=dev_fit_type,mask=None)
            Xvar = 'dev'
            ndy,ndx,ndc = 0,1,0
        else:
            None
        if deviations_applied_to=='c':
            ColorV = deviations_from_fit(deviations_predictor, color, fit_type=dev_fit_type,mask=None)
            ndy,ndx,ndc = 0,0,1
        else:
            ColorV = notation_fix(color)
    else:
        Y,ColorV = notation_fix(Yvar),notation_fix(color)
        ndy,ndx,ndc = 0,0,0
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
        
        ##linear model
        fun, print_fun = btf.lin_fit(X,Y,mask=mask,type_return='function and print')
        
        #quad model, fixed extrema
        #pick_minx = 9.3
        #dicF = btf.fit_2sets(X,Y, fit_func=btf.func_poly2_EX(pick_minx), mask=mask)
        #fun, print_fun = dicF['function'],dicF['print function']
        #popt = dicF['parameters']
        #xopt = pick_minx#-popt[1]/(2*popt[2])
        #yopt = fun(xopt)
        #plt.plot([xopt],[yopt],'yo',label='min:('+str(round(xopt,4))+','+str(round(yopt,4))+')')
        
        #quad model, regular
        #dicF = btf.fit_2sets(X,Y, fit_func=btf.func_poly2, mask=mask)
        #fun, print_fun = dicF['function'],dicF['print function']
        #popt = dicF['parameters']
        #xopt = -popt[1]/(2*popt[2])
        #yopt = fun(xopt)
        #plt.plot([xopt],[yopt],'yo',label='min:('+str(round(xopt,4))+','+str(round(yopt,4))+')')
        
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
        plt.legend(loc=4,ncol=1, fancybox=True,prop={'size':8})
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
        #print(color)
        plt.colorbar(mapper,label=namer(color,ndc))
        plt.grid()
        ct+=1
    fig.text(0.5, 0.04,list_to_name(Xvar,ndx)+' of '+t_e+' events', ha='center',fontdict=font)
    #fig.text(0.04, 0.5, 'CH4 residuals (based on soil temp at -10 cm)', va='center', rotation='vertical',fontdict=font)
    fig.text(0.04, 0.5, list_to_name(Yvar,ndy), va='center', rotation='vertical',fontdict=font)
    #plt.suptitle('Sensitivity to water table at different threshold definitions of '+t_e+' events',fontsize=16,fontdict=font)
    plt.suptitle('Sensitivity at different threshold definitions \n(to define '+t_e+' events)',fontsize=16,fontdict=font)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9,bottom=.1,left=.13)
    if pic_name==None:
        if save_or_show=='save':
            
            plt.savefig(gn(), bbox_inches='tight')
            plt.close(fig)
        else:
            plt.show()
    else:
        #pnam = pic_namer(pic_name, pic_folder_name)
        plt.savefig(gn(pic_name,pic_folder_name), bbox_inches='tight')

xx='WT'
yy='NCH4_S2'
#yy='NCH4'
co='Ts10'

slope_at_thresholds(thresholds_array=[27,9.3],Xvar=xx,Yvar=yy,color=co,
    deviations_applied_to='y',mask_events='inundated',pic_name='A2l',save_or_show='show')#,col_map='Blues')
slope_at_thresholds(thresholds_array=[-9,9.3],Xvar=xx,Yvar=yy,color=co,
    deviations_applied_to='y',mask_events='aerated',pic_name='I2l',save_or_show='show')#,col_map='Blues')
plt.show()

        
#slope_at_thresholds(Xvar='WT',Yvar='NCH4_S1',color='Ts10',
    #pic_name='WT_vs_dev_maskI',deviations_applied_to='y',mask_events='inundated',save_or_show='show')#,col_map='Blues')
#from marked_poisson_process import *

#var = 'period of aeration'
#var2 = 'period of inundation'
#for thres in [0,3,5,7,8,9,10,11,12,15]:
    #val_array,arrival_times = time_series(notation_fix([var,thres]))
    #fit_exp(val_array,arrival_times,var_name=var+' (threshold='+str(thres)+')',
        #name_fig='po'+var[10]+ str(thres),name_fig_dirc='net_inundation_aeration_periods/periods_as_MPPs',save_or_show='save')
    #fit_exp(notation_fix([var,thres]),waiting_times=None,var_name=var+' (threshold='+str(thres)+')',
        #name_fig='BULK_po'+var[10]+ str(thres),name_fig_dirc='net_inundation_aeration_periods/periods_as_MPPs',save_or_show='save')

#for thres in [10]:
    #val_array,arrival_times = time_series(notation_fix([var,thres]))
    #fit_exp(val_array,arrival_times,var_name=var+' (threshold='+str(thres)+')',
        #name_fig='po'+var[10]+ str(thres),name_fig_dirc='net_inundation_aeration_periods/periods_as_MPPs',save_or_show='hold')
    #fit_exp(notation_fix([var,thres]),waiting_times=None,var_name=var+' (threshold='+str(thres)+')',
        #name_fig='BULK_po'+var[10]+ str(thres),name_fig_dirc='net_inundation_aeration_periods/periods_as_MPPs',save_or_show='hold')
#plt.show()

#PoI = notation_fix([var2,5])
#PoA = notation_fix([var,5])
#TD = notation_fix('TotDays')
#plt.plot(TD,PoI,'r',label=var2)
#plt.plot(TD,PoA,'b',label=var)
#plt.ylim(ymin=-25)
#plt.legend()
#plt.show()

#for idx in range(0,len(notation_fix([var,5]))):
    #if PoI[idx]!=0 and PoA[idx]!=0:
        #print(idx,PoI[idx],PoA[idx])

#for thres in [0,3,5,7,8,9,10,11,12,15]:
    #fit_exp(notation_fix([var,thres]),waiting_times=None,var_name=var+' (threshold='+str(thres)+')',
        #name_fig='BULK_po'+var[10]+ str(thres),name_fig_dirc='net_inundation_aeration_periods/periods_as_MPPs',save_or_show='save')


#depths_array,arrival_times = time_series(notation_fix('WT'))
#fit_exp(notation_fix('WT'),save_or_show='hold')
#plt.hist(notation_fix('WT'), 30, histtype='bar',  normed=True)#,label='histogram of actual rainfall depths')
#plt.show()






