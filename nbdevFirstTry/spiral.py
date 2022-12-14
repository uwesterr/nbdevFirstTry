# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_spiral.ipynb.

# %% auto 0
__all__ = ['t', 'v', 'B', 'r_max', 't_max', 'dut_pat_loop', 'phi_list_method', 'time_list_method', 'flag_out_list_method',
           'r_list_method', 'spiral_count', 'spiral_count_list_method', 'fig', 'axs', 'dut_pat_loop_extract', 'phi',
           'DutPatLoop']

# %% ../00_spiral.ipynb 2
import numpy as np
import  matplotlib.pyplot as plt
from fastcore.utils import *


# %% ../00_spiral.ipynb 4
t = np.linspace(0,40,100)
v = 0.11 # velocity in rad/s
B = 8.6e-6 # spiral arm distance
r_max=800e-6 # max radius in rad
t_max=3.14*(r_max)**2/(B*v) # calculate resulting spiral duration

# %% ../00_spiral.ipynb 6
def phi(B:float, # spiral arm distance
        v:float, # spiral angular velocity
        t:float, # time
        flag_out:int, # indicated if spiral goes out- or inwards
        t_max:float, # time for one outward spiral_count
        spiral_count:int ):# counts the number of performed spirals
    "compute phi and radius"
    if flag_out:
        phi1 = np.sqrt(4*np.pi/B*v*(t-t_max*(spiral_count)))

        r=B*phi1/(2*np.pi)
       # print(phi1)
        if r >= 800e-6:
            flag_out=0
            spiral_count=spiral_count+1
            #t_max=t
    else:
        if ((4*np.pi/B*v*((spiral_count+1)*t_max-t))>=0):
            phi1 = np.sqrt(4*np.pi/B*v*((spiral_count+1)*t_max-t))
            
        else:
            phi1=0.0
        r=B*phi1/(2*np.pi)
        if r <= 5e-6:
            flag_out=1  
            spiral_count=spiral_count+1  
    return phi1, flag_out, r, spiral_count


# %% ../00_spiral.ipynb 11
class   DutPatLoop:
    """
    Class to implement DUT PAT loop for STB
    """

    
    def __init__(self):
        """
        Initialize LCT values
        

        Args:
            para_lct (dict): parameters for LCT
            para_system (dict): parameters for system, like max time, time steps, ...
            debug_flag (boolean): 1 if debug mode is on and print statements are active
        """
        self.B = 8.6e-6 # spiral arm distance
        self.v = 0.11 # spiral angular velocity
        self.flag_out=1
        self.t_max=0
        self.new_spiral=1
        self.spiral_count=0
        
    def phi_method(self,
            B:float, # spiral arm distance
            v:float, # spiral angular velocity
            r_max:float, # max radius in rad
            t:float): # time
        "compute phi and radius"
        if self.new_spiral:
            self.t_max=3.14*(r_max)**2/(B*v) # calculate resulting spiral duration
        if self.flag_out:
            phi1 = np.sqrt(4*np.pi/B*v*(t-self.t_max*(self.spiral_count)))

            r=B*phi1/(2*np.pi)
        # print(phi1)
            if r >= 800e-6:
                self.flag_out=0
                self.spiral_count=self.spiral_count+1
                #t_max=t
        else:
            if ((4*np.pi/B*v*((self.spiral_count+1)*self.t_max-t))>=0):
                phi1 = np.sqrt(4*np.pi/B*v*((self.spiral_count+1)*self.t_max-t))
                
            else:
                phi1=0.0
            r=B*phi1/(2*np.pi)
            if r <= 5e-6:
                self.flag_out=1  
                self.spiral_count=self.spiral_count+1  
        return phi1, r

# %% ../00_spiral.ipynb 19
dut_pat_loop=DutPatLoop()

# %% ../00_spiral.ipynb 20
t = np.linspace(0,12,1000)
phi_list_method=[]
time_list_method=[]
flag_out_list_method=[]
r_list_method=[]
spiral_count=0
spiral_count_list_method=[]
for i in t:
    #print(i)
    phi1, r=dut_pat_loop.phi_method(B, v, r_max, i)
    #
    # print(phi1, flag_out)
    phi_list_method.append(phi1)
    time_list_method.append(i)
    flag_out_list_method.append(dut_pat_loop.flag_out)
    r_list_method.append(r)
    spiral_count_list_method.append(dut_pat_loop.spiral_count)


# %% ../00_spiral.ipynb 22
#| label: fig-polar-method
#|echo: false
fig, axs = plt.subplots(2,3)

axs[0,0].plot(time_list_method,r_list_method, 'b')
axs[0,1].plot(time_list_method,phi_list_method, 'b')
axs[0,2].plot(time_list_method,flag_out_list_method, 'r')
axs[1,0].plot(time_list_method,spiral_count_list_method, 'r', label='D=1m')

plt.show()

# %% ../00_spiral.ipynb 27
dut_pat_loop_extract=DutPatLoop()

# %% ../00_spiral.ipynb 28
@patch
def phi_method_extract(self:DutPatLoop,
        B:float, # spiral arm distance
        v:float, # spiral angular velocity
        r_max:float, # max radius in rad
        t:float): # time
    "compute phi and radius"
    if self.new_spiral:
        self.t_max=3.14*(r_max)**2/(B*v) # calculate resulting spiral duration
    if self.flag_out:
        phi1 = np.sqrt(4*np.pi/B*v*(t-self.t_max*(self.spiral_count)))

        r=B*phi1/(2*np.pi)
    # print(phi1)
        if r >= 800e-6:
            self.flag_out=0
            self.spiral_count=self.spiral_count+1
            #t_max=t
    else:
        if ((4*np.pi/B*v*((self.spiral_count+1)*self.t_max-t))>=0):
            phi1 = np.sqrt(4*np.pi/B*v*((self.spiral_count+1)*self.t_max-t))
            
        else:
            phi1=0.0
        r=B*phi1/(2*np.pi)
        if r <= 5e-6:
            self.flag_out=1  
            self.spiral_count=self.spiral_count+1  
    return phi1, r
