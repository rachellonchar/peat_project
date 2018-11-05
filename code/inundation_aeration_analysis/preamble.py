
#regular code directory setup:
import sys, os, os.path
cwd = os.getcwd()
main_dirc = cwd.split('code', 1)[0]
cwd_code = main_dirc + 'code'
sys.path.insert(0, cwd_code+'/prelims')
from save_funcs import *
#-------------------------------------------
import basic_fit_funcs as btf
sys.path.insert(0, cwd_code+'/stochastic_modeling')


##-----------------------------------------------------------------------
#variables,naming = load_obj('parameters_09_18'),load_obj('parameter_index_09_18')
#var,nam = load_obj('hold_parameters'),load_obj('hold_naming')
#var,nam = load_obj('adj_parameters'),load_obj('adj_naming')
var,nam = load_obj('params_4states'),load_obj('names_4states')

ycs = nam['years']
ycs2 = [yr for yr in ycs if yr not in [2011,2013,0]]
#print(ycs2)
nc = nam['calls']

#print(var['threshold='][0]['pt_A'])

def vpre(*params):
    ret = var
    st=0
    for param in params:
        st += 1
        if st==len(params):
            if type(param)==list:
                holder=[]
                for p in param:
                    holder = np.append(holder, ret[p])
                ret = holder
            else:
                ret = ret[param]
        else:
            ret = ret[param]
    if type(ret)==dict:
        try:
            ret = ret[2]
            #print('No years specified...using all years, minus 2011 and 2013.')
        except:
            print('FULL PARAMETER CALL NOT SPECIFIED.')
    return ret

            
def nf(*params): 
    ret = ''
    breaker=False
    for param in params:
        if param == params[0] and len(param)>=3:
            if param[0:3]=='exp' or param[0:3]=='dev' or param[0:3]=='log':
                ret += nam['full calls'][param]
                breaker=True
        if breaker==False:
            if type(param)==str and param in nc:
                ret += nam['full calls'][param]
    return ret
    
def nu(*params): 
    ret = ''
    breaker=False
    for param in params:
        if param == params[0] and len(param)>=3:
            if param[0:3]=='exp' or param[0:3]=='dev' or param[0:3]=='log':
                ret += nam['units'][param]
                breaker=True
        if breaker==False:
            if type(param)==str and param in nc:
                ret += nam['units'][param]
    return ret

def yname(*yr_calls):
    ret = ''
    for yrc in yr_calls:
        ret += nam['year names'][yrc]
    return ret

def quick_mask0(arg,years=2):
    if type(arg)==list:
        if len(arg)==2:# or len(arg)==3:
            if arg[0][0]=='a' or arg[0][0]=='A':
                fin = 'maskA'
            elif arg[0][0]=='i' or arg[0][0]=='I':
                fin = 'maskI'
            elif arg[0][0]=='h' or arg[0][0]=='H':
                fin = 'maskH'
            elif arg[0][0]=='c' or arg[0][0]=='C':
                fin = 'maskC'
            #fin = 'maskA' if (arg[0][0]=='a' or arg[0][0]=='A') else 'maskI'
            th = arg[1] 
            mask = vpre('threshold=',th,fin,years)
            modf = nf('threshold=',th,fin,years)
        #elif len(arg)==3:
            #fin = 'maskA' if (arg[0][0]=='a' or arg[0][0]=='A') else 'maskI'
            #th = arg[2]
            #mask1 = vpre('threshold=',th,fin,years)
            #modf1 = nf('threshold=',th,fin,years)
            #mask2 = vpre('threshold=',th,'maskW',years)
            #mask = btf.mult_masks(mask1,mask2)
            #modf = modf1 + ' and freezing temperatures'
        else:
            mask = arg
            modf = ' (custom mask)'
    elif type(arg)==type(None):
        #mask = np.zeros_like(vpre('DoY',years))
        mask = None
        #print(type(mask))
        modf = ''
    elif type(arg)==str:
        if arg[0]=='w' or arg[0]=='W':
            mask = vpre('threshold=',0,'maskW',years)
            modf = nf('threshold=',0,'maskW',years)
    elif type(arg)==type(np.zeros(3)):
        mask = arg
        modf = ' (custom mask)'
    return mask, modf

def mult_masks(*masks):
    #inc_mask = np.zeros_like(masks[0])

    inc_mask = None
    for mask in masks:
        #print(mask)
        if type(mask)!=type(None):
            inc_mask = np.zeros(len(mask))
    if type(inc_mask)==type(None):
        None
        #print('ok')
    else:
        for mask in masks:
            for idx in range(0,len(inc_mask)):
                if mask[idx]==1:
                    inc_mask[idx] = 1
    #print(inc_mask)
    return inc_mask
        
    


def add_devs_dicP(*desired,param1='NTs10',param2='NCH4_S1',years=2,
    mask=None, fit='exp',stickyX=0,stickyY=0,
    clipped=0,clipped_devs=0):
    
    if stickyX==0:
        p1 = param1 if type(param1)==list else [param1]
        p1.append(years)
        X = vpre(*tuple(p1))
    else:
        X = param1
    if stickyY==0:
        p2 = param2 if type(param2)==list else [param2]
        p2.append(years)
        Y = vpre(*tuple(p2))
    else:
        Y = param2
    if fit=='exp':
        fit_type = btf.func_exp
    elif fit=='quad':
        fit_type = btf.func_poly2
    else:
        fit_type = btf.func_linear
    dev_dic = btf.deviations_from_fit(X,Y,fit_type=fit_type,mask=mask,
        clipped=clipped,clipped_devs=clipped_devs)
    ret = []
    for des in desired:
        ret.append(dev_dic[des])
    return ret


def ftup(arg):
    if type(arg)==list:
        return tuple(arg)
    elif type(arg)==tuple:
        return arg
    elif type(arg)==str:
        return arg
    else:
        return tuple([arg])

def quick_mask(*mask_args,years):
    allM = []
    mod = ''
    ct=0
    for ma in mask_args:
        mask, modf = quick_mask0(ma,years=years)
        allM.append(mask)
        if modf!='':
            if ct!=0:
                mod += ', '+modf
            else:
                mod += modf
        ct+=1
    nmask = mult_masks(*ftup(allM))
    return nmask, mod
    

desired_types = ['X','Y','Yexp','Xs','Ys','Ysexp','log Y','log Yexp','log Ysexp','print function', 
    'print log function','deviations']

def add_devs_dic(*desired,param1='NTs10',param2='NCH4_S1',years=2,
    mask=None, fit_type=btf.func_exp,clipped=0,clipped_devs=0):
    
    devis,ss = [],[]
    for param in [param1,param2]:
        if type(param)==list and param[0] in desired_types:
            devis.append(add_devs_dicP(param[0],param1=param[1],param2=param[2],years=years,
                fit=param[3],clipped=0,clipped_devs=0)[0])
            ss.append(1)
        else:
            devis.append(param)
            ss.append(0)
    ret = add_devs_dicP(*desired,param1=devis[0],param2=devis[1],years=years,
        mask=mask,fit=fit_type,stickyX=ss[0],stickyY=ss[1],clipped=clipped,clipped_devs=clipped_devs)
    return ret 
    
        
        

def vnu(*params,mask=None,out=4):
    ct,add,adv = 1,False,0
    for param in params:
        #if type
        if ct==1:
            fit = 'lin'
            if type(param)==str and (param in desired_types):
                add=True
                if param[0]=='X':
                    dezi = [param]
                elif param[0]=='l':
                    dezi = [param,'print log function']
                else:
                    dezi = [param,'print function']
                    
        if ct==4 and add==True:
            fit = param
        if ct==len(params):
            if type(param)==int or (type(param)==list and type(param[0])==int):
                years = param 
            else:
                years = 2
        ct+=1
    
    #if type(mask)==type(None):
    
    if type(mask)==list and type(mask[0])==list:
        masker = tuple(mask)
        tmask,mask_modf = quick_mask(*masker,years=years)
    else:
        masker = mask
        tmask,mask_modf = quick_mask(masker,years=years)
    if add:
        for param in params[1:3]:
            if type(param)==list:
                if type(param[-1])==int:
                    param = param.pop()
        if len(dezi)>1:
            d = add_devs_dic(*ftup(dezi),param1=params[1],param2=params[2],
                years=years, fit_type=fit,mask=tmask)
            array0, fit_modf = d[0],d[1]
            full_y = 'expected '+nf(*ftup(params[2]))+'\n'+fit_modf
            fu = nu(*ftup(params[2]))
        else:
            array0 = add_devs_dic(*ftup(dezi),param1=params[1],param2=params[2],
                years=years, fit_type=fit,mask=tmask)[0]
            full_y = nf(*ftup(params[2]))
            fu = nu(*ftup(params[2]))
    else:
        array0, full_y, fu = vpre(*ftup(params)), nf(*ftup(params)), nu(*ftup(params))
    if type(tmask)==type(None) or len(array0)!=len(tmask):
        array=array0
    else:
        #array = btf.mask_array(array0,mask=tmask)
        array = np.ma.masked_array(array0,mask=tmask)
    if out==1:
        return array
    else:
        return array, full_y, fu, mask_modf
        
def v(*params,mask=None):
    return vnu(*params,mask=mask,out=1)

#all_yrs = [   2009    2010    2011    2012    2013    2014   20150    2015    2016
   #20170    2017    2018   11130    1113    1517   15170 4409170  441518
  #441517 4415170]

def inclusive_yr_call(*year_calls):
    lf = nam['years included']
    alll = lf[0]
    ally = []
    for yp in year_calls:
        for yy in lf[yp]:
            if yy not in ally:
                ally.append(yy)

    len_hit,hit = len(alll),0
    for call in nam['years']:
        callN = lf[call]
        if set(ally).issubset(set(callN)):
            if len(callN)<len_hit:
                len_hit,hit = len(callN),call
    return hit
        
    #print(alll)



#inclusive_yr_call(2009,11130)

#print(vpre('exp CH4_S1','NTs10',2009))
vnu('exp CH4_S1','NTs10',2009,mask=['a',0])

#plt.plot(v('DoY',[2011,2013]),v('Ts10',[2011,2013]))
#plt.show()




            
        
            

#print(nf('WTa'))
#plt.plot(
#nf('DoY',2011)
#nu('threshold=',0,'PoA')


            
            



