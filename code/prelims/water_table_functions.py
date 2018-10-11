import numpy as np
import matplotlib.pyplot as plt
import xlrd
import scipy.special
import scipy.integrate 
from scipy.integrate import quad
import math
import random
import xlwt
import xlrd
                
#PARAMETERS THAT ARE INDEPENDENT OF WATER TABLE Y
#parameter definitions using Laio et al 2009 (L09), Tamea et al. 2010 (T10), Tamea et al. 2009 (T09)
#field capacity soil moisture, L09(2)
def Y_ind(T_p, k_s, m, n, psi_s, rd):
    sfc = ((0.05*T_p)/k_s)**(m/(2+3*m)) #field capacity soil moisture, L09(2)
    #print(sfc)
    B = 1/(1-2*m)*((1-sfc)/(1-sfc**(1/(2*m)))+2*m*sfc) #coeff for DWT, L09 under(30) - eq for specific yield 
    nu_star = T_p/(1+(0.35-0.65*n)*rd) #nu* the z-independent rate of cappillary flux, L09 before(21) - eq for yc
    psi_fc = psi_s*sfc**(-1/m) #soil matric potential at field capacity, L09 under(26) - eq for h 
    #critical depth, L09(21)
    a_F = 1/(2+3*m)
    x1_F = (sfc)**(-(2+3*m)/m)
    F11 = scipy.special.hyp2f1(a_F, 1, 1+a_F, -(nu_star)/k_s*x1_F)
    F12 = scipy.special.hyp2f1(a_F, 1, 1+a_F, -(nu_star)/k_s*1)
    y_c = (psi_fc)*F11 - (psi_s)*F12
    return sfc, B, nu_star, psi_fc, y_c

#depth of seperation between saturated and unsaturated soil, L09(3)
def Y_actual(y_tau, psi_s):
    y_actual = y_tau - psi_s
    return y_actual

#h(y) and s(y)
def h_and_s0(y, T_p, k_s, m, n, psi_s, rd):
    #non-y dependent variables
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    #h(y)
    Atop = psi_fc - psi_s - y_c
    A = Atop/(Atop-5*rd)
    if y >= y_c: #shallow conditions
        h_y = 0
        dh_dy = 0
        s_bar = 'None'
        if (y >= 0): #standing water
            sy_z0 = 1 #saturated at ground surafce if water table over zero
        elif (y < 0): #shallow NOT standing
            #soil moisture at the ground surface
            sy_z0 = (1+(sfc**(-1/(2*m))-1)*(y-0)/y_c)**(-2*m)
    elif (y < y_c): #deep conditions - could be deep or very deep
        #soil moisture at the ground surface
        sy_z0 = (1+(sfc**(-1/(2*m))-1)*(y-0)/y_c)**(-2*m)
        if (y >= (-5*rd+psi_fc-psi_s)): #deep conditions
            h_y = (1-A**(3/4))*(y-y_c) - A**2*(1-A**(-1/4))/(-y_c+psi_fc-psi_s)*(y-y_c)**2
            dh_dy = (1-A**(3/4)) - (2)*A**2*(1-A**(-1/4))/(-y_c+psi_fc-psi_s)*(y-y_c)
        elif (y < (-5*rd+psi_fc-psi_s)): #very deep conditions
            h_y = y - psi_fc + psi_s
            dh_dy = 1
        if (h_y < 0):
            int_sm_z0 = (1+(sfc**(-1/(2*m))-1)*(y-0)/y_c)**(1-2*m)/((sfc**(-1/(2*m))-1)/y_c*(-1+2*m))
            int_sm_zh = (1+(sfc**(-1/(2*m))-1)*(y-h_y)/y_c)**(1-2*m)/((sfc**(-1/(2*m))-1)/y_c*(-1+2*m))
            s_bar = -1/h_y*(int_sm_z0 - int_sm_zh)
        else:
            s_bar = 'None'
    return h_y, dh_dy, sy_z0, s_bar

def soil_moisture(y,z,T_p, k_s, m, n, psi_s, rd):
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    h,t1,t2,t3 = h_and_s0(y, T_p, k_s, m, n, psi_s, rd)
    if z>=0: #not in soil!
        s = None
    elif z<0 and z>=h: #low moisture zone
        s = (1+(sfc**(-1/(2*m))-1)*(y-z)/y_c)**(-2*m) #Laio (18) 
    elif z<h and z>y: #high moisture zone
        s = (1+(sfc**(-1/(2*m))-1)*(y-z)/(y-h))**(-2*m) #Laio (28) 
    else: #below the water table
        s = 1
    return s

#defining rain series function based on lamda alpha parameters
def Rain_events(lam, alpha, N, dt, interception = 0):
    lam_0 = lam - interception
    depths = np.random.exponential(1/alpha, N)
    event_markers = np.random.random(N)
    rain_events_ = event_markers < (lam_0)*dt
    rain_series = np.zeros(N)
    rain_series[rain_events_] = depths[rain_events_]
    return rain_series

##PARAMETERS DEPENDENT ON Y
def simulation_paramters(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, return_special=None):
    #non-y dependent variables
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    lam0 = lam - interception
    #h(y)
    Atop = psi_fc - psi_s - y_c
    A = Atop/(Atop-5*rd)
    if y >= y_c: #shallow conditions
        h_y = 0
        dh_dy = 0
        s_bar = 'None'
        if (y >= 0): #standing water
            sy_z0 = 1 #saturated at ground surafce if water table over zero
            beta = 1
            f1y = k12*(y_0-y)
        elif (y < 0): #shallow NOT standing
            #soil moisture at the ground surface
            sy_z0 = (1+(sfc**(-1/(2*m))-1)*(y-0)/y_c)**(-2*m)
            beta = n*(1-sy_z0)
            f1y = k1*(y_0-y-psi_s)
        ET_y = T_p
    elif (y < y_c): #deep conditions - could be deep or very deep
        #soil moisture at the ground surface
        sy_z0 = (1+(sfc**(-1/(2*m))-1)*(y-0)/y_c)**(-2*m)
        if (y >= (-5*rd+psi_fc-psi_s)): #deep conditions
            h_y = (1-A**(3/4))*(y-y_c) - A**2*(1-A**(-1/4))/(-y_c+psi_fc-psi_s)*(y-y_c)**2
            dh_dy = (1-A**(3/4)) - (2)*A**2*(1-A**(-1/4))/(-y_c+psi_fc-psi_s)*(y-y_c)
        elif (y < (-5*rd+psi_fc-psi_s)): #very deep conditions
            h_y = y - psi_fc + psi_s
            dh_dy = 1
        if (h_y < 0):
            int_sm_z0 = (1+(sfc**(-1/(2*m))-1)*(y-0)/y_c)**(1-2*m)/((sfc**(-1/(2*m))-1)/y_c*(-1+2*m))
            int_sm_zh = (1+(sfc**(-1/(2*m))-1)*(y-h_y)/y_c)**(1-2*m)/((sfc**(-1/(2*m))-1)/y_c*(-1+2*m))
            s_bar = -1/h_y*(int_sm_z0 - int_sm_zh)
        else:
            s_bar = 'None'
        ET_y = T_p*(np.exp(h_y/rd)-np.exp(y/rd)) #evapotranspiration - T10(3)
        #lambda_y = lam0*np.exp((n*h*(sfc-sbar))/alpha) #recharge rate - T10(2)
        beta = n*(1-sfc) + n*(dh_dy-1)*B #specific yield - L09(20)and(30)
        f1y = k1*(y_0-y-psi_s) #groundwater flux - T10(4)
    if (y < y_c):
        deficit = max(0, n*h_y*(sfc - s_bar))
    else:
        deficit = 0
    if return_special == None:
        return beta, ET_y, f1y, deficit
    elif return_special == 'f-ET':
        ylim_when = f1y - ET_y #=0
        return ylim_when
    elif return_special == 'ylim info':
        return h_y, ET_y, f1y
    else:
        print('Error')

#finding the lower limit of y
#this is when ET = lateral flow
def lowerlim(starting_value, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0):
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    #start_eval = -5*rd+psi_fc-psi_s+1
    #start_eval = 50
    y_lower_limit = scipy.optimize.fsolve(simulation_paramters, starting_value, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, 'f-ET',))
    return y_lower_limit

#ANALYTICAL SOLUTIONS EQUATIONS
#first define the integrand
def integrand(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0):
    lam0 = lam-interception
    beta, ET_y, f1y, deficit = simulation_paramters(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    f_integrand = (beta/alpha) - lam0*beta/(ET_y - f1y)
    return f_integrand

def py(u , T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, C=1):
    #f= lambda y: integrand(y)
    beta_u, ET_u, f1_u, deficit = simulation_paramters(u, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    if ET_u != f1_u:
        integrand_val_error = quad(integrand, 0, u, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception,))
        #print(integrand_val_error)
        integrand_val = integrand_val_error[0]
        upper_bound = integrand_val_error[1]
        p_u = (1/C)*beta_u/(ET_u - f1_u)*np.exp(-integrand_val)
    else:
        p_u = 0
    return p_u
    
def Py(y, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, C=1):
    #pdf = lambda x: py(x , T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C)
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    tol = 0.5
    if y < ylim:
        val_bound = [0,0]
    elif (y >= ylim) and (y < y_c-tol):
        test_for_negative = quad(py, ylim+tol, y, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
        if test_for_negative[0] < 0:
            val_bound = [0,0]
        else:
            val_bound = test_for_negative
    elif (y >= y_c-tol) and (y <= y_c+tol):
        val_bound = quad(py, ylim+tol, y_c-tol, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
    elif (y > y_c+tol) and (y < 0-tol):
        val_bound = quad(py, ylim+tol, y_c-tol, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))+\
            quad(py, y_c+tol, y, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
    elif (y >= -tol) and (y <= tol):
        val_bound = quad(py, ylim+tol, y_c-tol, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))+\
            quad(py, y_c+tol, -tol, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
    elif y > tol:
        val_bound = quad(py, ylim+tol, y_c-tol, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))+\
            quad(py, y_c+tol, -tol, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))+\
            quad(py, tol, y, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
    #val_bound = quad(py, yLB, yUP, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
    integral_value = val_bound[0]
    upper_bound_error = val_bound[1]
    return integral_value

def y_practicalbound(ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, C=1):
    #sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    #step = (y_c-ylim)/50
    ytest = ylim+0.5
    step = 3
    too_small = True
    while too_small:
        p_test = quad(py, ylim+0.5, ytest, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
        if p_test[0] < 0.01:
            y_out = ytest
            ytest += step
        else:
            y_out = ytest
            too_small = False
    return y_out

def y_practicalbound_upper(ylower, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, C=1):
    #sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    #step = (y_c-ylim)/50
    ytest = 0+0.5
    step = 3
    small_enough = True
    count = 0
    while small_enough:
        p_test = quad(py, ylower, ytest, args=(T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C,))
        if p_test[0] < 0.99:
            y_out = ytest
            ytest += step
        elif p_test[0] >= 0.99:
            y_out = ytest
            small_enough = False
        if ytest < 200:
            y_out = ytest 
        else:
            small_enough = False
            y_out = np.inf
    return y_out

#finding the C value 
#eg normalizing the pdf
def cons(ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0):
    #non-y dependent variables
    #sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    #vd_cutoff = -5*rd+psi_fc-psi_s
    #c_vdeep = Py(ylim , vd_cutoff, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    #c_deep = Py(vd_cutoff , y_c, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    #c_shal = Py(y_c , 0, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    #c = Py(ylim , np.inf, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    #Cval = c_vdeep + c_deep + c_shal + c_stan
    c = Py(np.inf, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    return c

#PDF AND CDF DEFINITIONS (finds C value for you)
def pdfCDF(y, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, C=1):
    #C = cons(ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    pdf_y = py(y , T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C)
    cdf_y = Py(y, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C)
    return pdf_y, cdf_y
#
#MODELING AS LINEAR
#NEED TO DEFINE LINEAR SYSTEMS FOR EACH PART
#first the nonlinear transformation x(y)
#this is a transformation of the deterministic loss part of the ODE for dy/dt
def xexact(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0):
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    h_y, dh_dy, sy_z0, s_bar = h_and_s0(y, T_p, k_s, m, n, psi_s, rd)
    #beta, ET, f, h, dhdy, s0, sbar = maineq("x transformation", y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    if y >= 0: #standing
        x = y
    elif (y < 0) and (y >= y_c): #shallow
        x = n*y - n*y_c/((sfc**(-1/(2*m))-1)*(-2*m+1))*(1+(sfc**(-1/(2*m))-1)*y/y_c)**(-2*m+1)
    else: #deep
        x = n*y*(1-sfc) - n/(2*m-1)*((1-sfc)/(1-sfc**(1/(2*m))) - 2*m*sfc + sfc - 1)*(h_y - y)
    return x

#line between two points
def xlinfit(y, y1, y2, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0):
    x = xexact(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    x1 = xexact(y1, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    x2 = xexact(y2, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    slope = (x2-x1)/(y2-y1)
    intercept = y1 - slope*x1
    return slope, intercept
#defining x(y)
def xlin(y, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0):
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    e = .0001
    if y >= 0:
        m = 1
        b = 0 
    elif (y < 0) and (y >= y_c): #shallow
        #just use one line for shallow for now---can extend it to be more precise later
        m, b = xlinfit(y, 0-e, y_c, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    else: 
        m, b = xlinfit(y, y_c-e, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    x = m*y - b
    return x, m, b

def ylin(ret, x, ylim , T_p, k_s, m, n, psi_s, rd, k1, k12, y_0):
    sfc, B, nu_star, psi_fc, y_c = Y_ind(T_p, k_s, m, n, psi_s, rd)
    x_0, m_stan, b_stan = xlin(0, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    x_yc, m_shal, b_shal = xlin(y_c, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    mid_deep = (ylim - y_c)/2 + y_c
    x_md, m_deep, b_deep = xlin(mid_deep, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    if x >= x_0: #y >= 0:
        m = m_stan
        b = b_stan
    elif (x < x_0) and (x >= x_yc): #shallow
        #just use one line for shallow for now---can extend it to be more precise later
        m = m_shal
        b = b_shal
    else: 
        m = m_deep
        b = b_deep
    y = m*x - b
    if ret == "mx+b":
        return y, m, b #note: here m = dy/dx
    elif ret == "x values":
        xlim, m_xlim, b_xlim = xlin(ylim, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
        return x_0, x_yc, x_lim
    else:
        print("Define returned values")

def ymb(x, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0):
    y, m, b = ylin("mx+b", x, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    return y, m, b
def x_lim_yc_0(x, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0):
    x_0, x_yc, x_lim = ylin("x values", x, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    return x_lim, x_yc, x_0
    
def MCTxlin(x, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, C=1):
    #output y(x) and dy/dx as well as the MCT
    y, dydx, x_intercept = ymb(x, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    pdfy, cdfy = pdfCDF(y, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C)
    pdf_x = pdfy*(dydx)
    cdf_x = (dydx)*cdfy #since dy/dx is just a constant in this case
    #yx means y(x)
    beta_yx, ET_yx, f1_yx, det = simulation_paramters(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    #the loss for the additive noise process x:
    loss_x = (ET_yx - f1_yx)/beta_yx
    MCT_x = cdf_x/(pdf_x*loss_x)
    return MCT_x, y, dydx

def MCTy(y, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception=0, C=1):
    beta_yx, ET_yx, f1_yx, det = simulation_paramters(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception)
    pdfy, cdfy = pdfCDF(y, ylim, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0, alpha, lam, interception, C)
    loss_y = (ET_yx - f1_yx)
    #x = xexact(y, T_p, k_s, m, n, psi_s, rd, k1, k12, y_0)
    MCT_y = cdfy/(pdfy*loss_y)
    return MCT_y
