from win32com.client import Dispatch
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Creating PHREEQC objects
def GetResult(input_string, db_path = 'WATEQ4F.DAT'):
	dbase = Dispatch('IPhreeqcCOM.Object')
	dbase.LoadDatabase(db_path)
	dbase.RunString(input_string)
	output = dbase.GetSelectedOutputArray()
	return output

# Calculate the RMSE between two arrays
def calculate_rmse(a, b):
	return np.sqrt(np.mean((a - b)**2))

# Create a function that compares two sets of data
def calculate_correlation(a, b):
    corr, _ = pearsonr(a, b)
    return corr

# Calculate RMSE from log_k
def get_fit(K_fitting, Con, SO4_leaching_ex, SeO3_binding_ex):
                        		 # Make sure experimental data has been imported 
	SeO3_binding_f=[]
	SO4_leaching_f=[]
	for Se_con in Con:
		input_str = f'''
			Phase
Ettringite  	# In order to simulate the pH change and 
		#SO42- environment in the experiment
					Ca6Al2(SO4)3(OH)12:26H2O + 12H+ = 2Al+++ + 6Ca++ + 38H2O + 3SO4--
					log_k 57.730
					delta_h -389.36
			SOLUTION 1
				units	mmol/kgw	
				Temp	20	
				ph	7	charge
				water   1
				Se(4) {Se_con}
			EQUILIBRIUM_PHASES 1
				Ettringite 0 0.000797 #Indicates the amount of 
				Save solution 1	  #ettringite in the system at 1 
				End                   #mol/L
			EXCHANGE_MASTER_SPECIES
				Xg Xg+2

			EXCHANGE_SPECIES
				Xg+2 = Xg+2
				log_k = 0
			
				Xg+2 + SO4-2 = XgSO4
				log_k = 0

				XgSO4 + SeO3-2 = XgSeO3 + SO4-2
				-gamma 3.5 0.015
				log_k = {K_fitting}

			USE SOLUTION 1
			EXCHANGE 1
				XgSO4 4e-5     #ettringite contains 0.004 mol/kg of 
			CALCULATE_VALUES	  #exchangeable SO42-
			SeO3(binding) 
			-start
			10 m_Se = MOL("XgSeO3") *1000
			100 SAVE m_Se
			-end
			SO4(leaching)
			-start
			10 m_S = (4e-5-MOL("XgSO4")) *1000
			100 SAVE m_S
			-end	

			SELECTED_OUTPUT
	   		-reset false
			-calculate_values SeO3(binding)
			-calculate_values SO4(leaching)

		'''
		output = GetResult(input_str)
		XgSeO3, SO4 = output[1]
		SeO3_binding_f.append(XgSeO3)
		SO4_leaching_f.append(SO4)
				
	fit = calculate_rmse(SO4_leaching_ex, SO4_leaching_f)
	return fit

#setting parameters  #Arbitrary starting conditions and boundaries can be set
min_fit = 1
K_fitting=0
best_fit=0
left = 0
right = 20
epsilon = 0.0001

# Loop calculation of fit 
while right - left > epsilon:
    mid = (left + right) / 2
    fit = get_fit(mid)
    if fit < min_fit:
        min_fit = fit
        K_fitting = mid
    if fit < get_fit(mid+epsilon):
        right = mid
    else:
        left = mid

best_K_fitting = K_fitting
best_fit = get_fit(best_K_fitting)

plt.plot(x, y)
