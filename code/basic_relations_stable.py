
#from definitions import *

#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *

sys.path.insert(0, cwd_code+'/inundation_aeration_analysis')
from inundation_aeration_period_definitions import *

def plot_basic(Xvar,Yvar,color='Ts10',deviations_predictor=None,dev_fit_type=btf.func_exp,
    fit_type=btf.func_linear,deviations_applied_to='y',col_map='coolwarm',
    pic_name=None, pic_folder_name=None,save_or_show='show'):
    
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
        X,Y,ColorV = notation_fix(Xvar),notation_fix(Yvar),notation_fix(color)
        ndy,ndx,ndc = 0,0,0
    maxD, minD = max(ColorV), min(ColorV)
    norm = matplotlib.colors.Normalize(vmin=minD, vmax=maxD, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=plt.cm.get_cmap(col_map))
    mapper.set_array([])
    minY,maxY = min(Y),max(Y)
    fig, ax = plt.subplots(ncols=1,nrows=1,  sharex=True, sharey=True, figsize=(15,9))
    plt.subplot(1,1,1)
    
    dicF = btf.fit_2sets(X,Y,fit_func=fit_type)
    fun, print_fun = dicF['function'],dicF['print function']
    Xexp,Yexp = btf.array_span(X, fun,dense=1,specify_points=20)
    plt.plot(Xexp,Yexp,'r',label=print_fun)
    bill = [mapper.to_rgba(val) for val in ColorV]
    plt.scatter(X,Y,s=30,c=bill,cmap=mapper,
        edgecolor=bill,vmin=minD,vmax=maxD,label='all events')
    plt.legend(loc=4,ncol=1, fancybox=True,prop={'size':8})
    plt.colorbar(mapper,label=namer(color,ndc))
    plt.grid()
    fig.text(0.5, 0.04,list_to_name(Xvar,ndx), ha='center',fontdict=font)
    #fig.text(0.04, 0.5, 'CH4 residuals (based on soil temp at -10 cm)', va='center', rotation='vertical',fontdict=font)
    fig.text(0.04, 0.5, list_to_name(Yvar,ndy), va='center', rotation='vertical',fontdict=font)
    #plt.suptitle('Sensitivity to water table at different threshold definitions of '+t_e+' events',fontsize=16,fontdict=font)
    plt.suptitle(list_to_name(Xvar,ndx)+' vs. '+list_to_name(Yvar,ndy),fontsize=16,fontdict=font)
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
#plot_basic(Xvar='NTs10',Yvar='NCH4_S1',color='WT',fit_type=btf.func_exp,
    #col_map='BrBG')#,pic_name='Ts10_vs_CH4',save_or_show='show')

plot_basic(Xvar='NTs10',Yvar='NCH4_S1',color='WT',fit_type=btf.func_exp,
    col_map='BrBG',pic_name='Ts10_vs_CH4_1518',save_or_show='show')
 

  
