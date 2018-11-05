#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------
import basic_fit_funcs as btf
#sys.path.insert(0, cwd_code+'/stochastic_modeling')


#from preamble0 import *
#import imageio
#from easier_objs import *

#v,n = load_obj('easier_params'),load_obj('new_naming')
##from analysis_funcs_newdat import dict_call
##def updater(*params,normalized_to_all_years='no',stats='no'):
    ##for param in params:
        ##dict_call(param,variables, naming,normalized_to_all_years,stats)
    ##return variables, naming
#def updater(*params):
    #return v,n

#adding a default mask of masking nothing
#naming
#mask_typesV = ['outlier removal']
#n.update({'mask types':mask_typesV})
#defN = {}
#defN.update({'outlier removal':[0]})
#n.update({'mask subtypes':defN})

##mask info:
#mask_typesD = {}
#mask0,mask1 = {},{}
#mask1.update({'rationale':'removing outliers in a model should lead to a steady slope at some number of removed outliers'})
#mask0.update({'mask vector':np.zeros_like(v['Ts10'])})
#mask1.update({0:mask0})
#mask_typesD.update({'outlier removal':mask1})
#v.update({'mask':mask_typesD})
#to get the mask:  
   # v['mask'][*mask type*][*ID of mask within mask type*]['mask vector']
#to get rationale behind mask type:
   # v['mask'][*mask type*]['rationale']

#to get ALL mask type names:
   # n['mask types']
#to get ALL mask SUBtype names:
   # n['mask subtypes'][*mask type*]


def threshold_mask(dic,naming_dic,threshold=0,param='WTa'):
    #all points start off NOT masked:
    #dic, naming_dic = updater(param)
    
    #check if units already in dic
    notin=True
    naming=naming_dic
    calls = naming['calls']
    if param=='WTa':
        I,A = 'I','A'
        inundation,aeration = 'inundation','aeration'
        inundated,aerated = 'inundated','aerated'
    elif param=='Ts10':
        I,A = 'H','C'
        inundation,aeration = 'warmer soil temperatures','cooler soil temperatures'
        inundated,aerated = 'warm','cool'
    if 'Po'+I in calls:
        notin=False
    
    poi,poa,pti,pta,mmi,mma,mmw = {},{},{},{},{},{},{}
    poia={}
    years = naming['years']
    #print(naming['calls'])
    for year_ in years:
        
        year = int(year_)
        siz = len(dic[param][year])
        mask_above,mask_below = np.zeros(siz),np.zeros(siz)
        above,below = 0,0
        days_above, days_below,dab = np.zeros(siz),np.zeros(siz),np.zeros(siz)
        permA,permI = [],[]
        mask_winter = np.zeros(siz)
        for idx in range(0, siz):
            #print(dic[param][year][idx])
            pt = dic[param][year][idx]
            #winter condition:
            if dic['Ts10'][year][idx]<0:
                mask_winter[idx]=1
            else:
                None
            if pt>threshold: # inundated
                if idx>0 and dic[param][year][idx-1]<=threshold:
                    permI.append(above)
                    above = 0
                mask_above[idx] = 1 # masks the inundated pt
                above += 1
                days_above[idx],days_below[idx] = above,0
                dab[idx] = above
            else: #aerated
                if idx>0 and dic[param][year][idx-1]>threshold:
                    permA.append(below)
                    below = 0
                mask_below[idx] = 1 # masks the aerated pt
                below += 1
                days_above[idx],days_below[idx] = 0,below
                dab[idx] = -below
            
        #period inundated or saturated:
        poi.update({year:days_above})
        poa.update({year:days_below})
        poia.update({year:dab})
        #print(days_above)
        
        #permanence times:
        pti.update({year:permI})
        pta.update({year:permA})
        
        #masks:
        mmi.update({year:mask_above})
        mma.update({year:mask_below})
        if param=='WTa':
            mmw.update({year:mask_winter})
        #print(mask_above)
        
        
        
    # outside yearly loop
    #add parameters to dictionary
    dic2 = {}
    dic2.update({'Po'+I:poi})
    dic2.update({'Po'+A:poa})
    dic2.update({'Po'+I+A:poia})
    dic2.update({'pt_'+I:pti})
    dic2.update({'pt_'+A:pta})
    dic2.update({'mask'+I:mmi})
    dic2.update({'mask'+A:mma})
    if param=='WTa':
        dic2.update({'maskW':mmw})
    #print(mmi)
    try:
        dic['threshold='].update({threshold:dic2})
    except:
        th = {}
        th.update({threshold:dic2})
        dic.update({'threshold=':th})
    #naming
    if notin:
        naming['full calls'].update({'Po'+I:'period of '+inundation})
        naming['full calls'].update({'Po'+A:'period of '+aeration})
        naming['full calls'].update({'Po'+I+A:'period of '+inundation+'(+) and '+aeration+'(-)'})
        naming['units'].update({'Po'+I:'[days]'})
        naming['units'].update({'Po'+A:'[days]'})
        naming['units'].update({'Po'+I+A:'[days]'})
        calls = np.append(calls,['Po'+I,'Po'+A,'Po'+I+A])
        naming['full calls'].update({'pt_'+I:'permanence time in '+ inundated+' state'})
        naming['full calls'].update({'pt_'+A:'permanence time in '+aerated+' state'})
        naming['units'].update({'pt_'+I:'[days]'})
        naming['units'].update({'pt_'+A:'[days]'})
        calls = np.append(calls,['pt_'+I,'pt_A'])
        naming['full calls'].update({'mask'+I:'mask '+inundated+' state'})
        naming['full calls'].update({'mask'+A:'mask '+aerated+' state'})
        naming['units'].update({'mask'+I:''})
        naming['units'].update({'mask'+A:''})
        if param=='WTa':
            naming['full calls'].update({'maskW':'mask winter'})
            naming['units'].update({'maskW':''})
            calls = np.append(calls,['mask'+I,'mask'+A,'maskW'])
        else:
            calls = np.append(calls,['mask'+I,'mask'+A])
        naming.update({'calls':calls})
    return dic, naming
#v,n = threshold_mask()
#for idx in range(0,len(v['period of aeration'][0])):
    ##if v['period of aeration'][0][idx]!=v['mask']['mask aerated events'][0]['mask vector'][idx]:
    #print(v['period of aeration'][0][idx],v['mask']['mask aerated events'][0]['mask vector'][idx])
    




#def outlier_loop(X,Y,fit_type=btf.func_linear,num_of_outliers=10):
    ##v,n = updater(X,Y)
    #fit_dic, new_mask,outs_removed = general_fit_pre(X=X,Y=Y,fit_type=fit_type,mask=None)
    #fun_info = {}
    #fun_info.update({0:fit_dic})
    
    #mask_types = n['mask types']
    #typee = 'outlier removal, '+X+' vs. '+Y
    #mask_types.append(typee)
    #n.update({'mask types':mask_types})
    #defN = {}
    #n['mask subtypes'].update({typee:[i for i in range(0,num_of_outliers+1)]})
    ##mask info:
    #mask_typesD = {}
    #mask0,mask1 = {},{}
    #mask1.update({'rationale':'removing outliers in a model should lead to a steady slope at some number of removed outliers'})
    #mask0.update({'mask vector':np.zeros_like(v['Ts10'])})
    #mask1.update({0:mask0})
    #mask_typesD.update({typee:mask1})
    #v.update({'mask':mask_typesD})
    #for ii in range(1,num_of_outliers+2):
        #tempD = {}
        #tempD.update({'mask vector':np.copy(new_mask)})
        #fit_dic, new_mask, outs_removed = general_fit_pre(X=X,Y=Y,fit_type=fit_type,mask=new_mask)
        #tempD.update({'function info':fit_dic})
        #v['mask'][typee].update({ii:tempD})
    #return v,n 

#def find_stable_slope(X,Y,deviations_predictor=None,dev_fit_type=btf.func_exp,
    #fit_type=btf.func_linear,num_of_outliers=30,dec_places=3):
    
    ##if type(X)==list:
    ##Xtyp = X if type(X)!=list else str(X[0])
    #typee = 'outlier removal, '+list_to_name(X)+' vs. '+list_to_name(Y)
    #if deviations_predictor!=None:
        #dp = deviations_predictor
        #devs = deviations_from_fit(X=dp,Y=Y,fit_type=dev_fit_type)
        #outlier_loop(X=dp,Y=Y,fit_type=dev_fit_type,num_of_outliers=num_of_outliers)
        #typee = 'outlier removal, '+list_to_name(dp)+' vs. '+list_to_name(Y)
        #v.update({'devs':devs})
        #Y='devs'
        #fd = v['mask'][typee]
    #fdic,mask_toss,orr = general_fit_pre(X=X,Y=Y,fit_type=fit_type)
    #slp = round(fdic['slope'],dec_places)
    #pslp = slp
    #converged=False
    #ct=0
    #while converged==False:
        #if deviations_predictor!=None:
            #nmask = fd[ct+1]['mask vector'] #mask from deviation outlier
        #else:
            #nmask=mask_toss
            #nmask = np.zeros_like(v['Ts10'])
        #fdic,mask_toss,orr = general_fit_pre(X=X,Y=Y,fit_type=fit_type,mask=nmask) #X vs dev function with that mask
        #nslp = round(fdic['slope'],dec_places)
        #if (abs(slp-nslp)/abs(slp)<=10**(-1*dec_places)) and (abs(pslp-slp)/abs(pslp)<=10**(-1*dec_places)) and (ct>=1):
            #converged=True
            #outs_removed = ct
            #outs_removed = sum(nmask)
        #pslp=slp
        #slp=nslp
        #ct+=1
        #if ct>num_of_outliers-1:
            #converged = True
            #outs_removed = 'does not converge after '+str(num_of_outliers-1)
    #return fdic, nmask,outs_removed

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
    
#def notation_fix(Tsoil,dic=v,naming_dic=n,ret_dics=0):
    #Tsil = dic
    #if type(Tsoil)!=list:
        #Tsoil = [Tsoil]
    #dic,naming_dic = updater(Tsoil[0])
    ##add inundation periods to dictionary
    #if (len(Tsoil)>1 and Tsoil[0]!='mask') or (len(Tsoil)>1 and Tsoil[0]=='mask'):
        #if len(Tsoil)>1 and Tsoil[0]!='mask':
            #thres = Tsoil[1]
        #else:
            #thres = Tsoil[2]
            #Tsoil.append('mask vector')
        #try:
            #dic['period of aeration'][thres]
        #except:
            #dic,naming_dic = threshold_mask(threshold=thres)
    ##elif len(Tsoil)>1 and Tsoil[0]=='mask':
        ##dic,naming_dic = threshold_mask(threshold=Tsoil[2])
        ##Tsoil.append('mask vector')
    #for modifier in Tsoil:
        #new = Tsil[modifier]
        #Tsil = new
    #if ret_dics==0:
        #return Tsil
    #else:
        #return Tsil, dic, naming_dic
#def list_to_name(Tsoil,base=0):
    #Tstring = ''
    #if type(Tsoil)!=list:
        #try:
            #Tsoil = [n['full names'][Tsoil]]
        #except:
            #Tsoil = [Tsoil]
        ##print(Tsoil)
    #if base==1:
        #for modifier in [Tsoil[0]]:
            #Tstring += ' '+str(modifier)
    #else:
        #for modifier in Tsoil:
            #Tstring += ' '+str(modifier)
    #return Tstring
        
##outlier_analysis_funcs = {}
#def expected_CH4(Tsoil='NTs10',CH4='NCH4_S1',fit_type=btf.func_exp,dic=v,naming_dic=n,mask=None):
    
    #Tsil,Csil = notation_fix(Tsoil), notation_fix(CH4)
    #fic = btf.fit_2sets(Tsil,Csil, fit_func=fit_type, mask=mask)
    #exp_fun = fic['function']
    #exp_labe = fic['print function']
    #popt = fic['parameters']
    #dic_Ts,dic_Ts2 = fic,{}
    #dicT = {}
    ##dicT.update({'f':dic_Ts})
    #fun = exp_fun
    #if fit_type == btf.func_exp:
        #lin_labe = btf.pre_plot(popt) #default model is polynomial
        #def lin_fun(xx): return np.log(popt[0])+popt[1]*xx
        #lin_popt = tuple((np.log(popt[0]),popt[1]))
        #dic_Ts2.update({'function':lin_fun})
        #dic_Ts2.update({'print function':lin_labe})
        #dic_Ts2.update({'parameters':lin_popt})
        #dicT = dic_Ts2
        #fun = lin_fun
    #else:
        #dicT = dic_Ts
    #if type(mask) == type(None):
        #mask,new_mask = np.zeros_like(Tsil),np.zeros_like(Tsil)
    #else:
        #new_mask = mask
    #exp = [fun(Tsil[ii]) for ii in range(0,len(Tsil))]
    #if fit_type!=btf.func_exp:
        #res_squared = [abs(Csil[ii]-exp[ii]) for ii in range(0,len(Tsil))]
    #else:
        #res_squared = [abs(np.log(Csil[ii])-exp[ii]) for ii in range(0,len(Tsil))]
        ##res_squared = [abs(np.exp(np.log(v[CH4][ii])-exp[ii])) for ii in range(0,len(v[Tsoil]))]
    #for ii in range(0,len(res_squared)):
        #if mask[ii]==1:
            #res_squared[ii]=0
    #mark_outlier = np.argmax(res_squared)
    #new_mask[mark_outlier] = 1
    #outs_removed = sum(new_mask)
    #dicT.update({'new mask':new_mask})
    #return dicT, new_mask, outs_removed
#def general_fit_pre(X,Y,fit_type=btf.func_linear,mask=None,just_slope=0):
    ##v,n = updater(X,Y)
    #func_fit_dic, new_mask, outs_removed = expected_CH4(Tsoil=X,CH4=Y,fit_type=fit_type,
        #dic=v,naming_dic=n,mask=mask)
    #popt = func_fit_dic['parameters'] 
    #slopef = popt[1]
    #if just_slope==1:
        #return slopef
    #else:
        #func_fit_dic.update({'slope':slopef})
        #return func_fit_dic, new_mask, outs_removed