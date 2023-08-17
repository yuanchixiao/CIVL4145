#==============================================================================
# Example sript showing basic importing and plotting water quality data.
#==============================================================================

# 0.0 ===== IMPORTING PACKAGES / MODULES ======================================
import numpy as np                            # Basic mathematics library
import matplotlib.pyplot as plt               # Imports plotting library
import matplotlib.dates as mdates
import datetime                          # Imports module to convert dates
import csv    #Imports csv module

# 1.0 ===== LOADING INPUT DATA ================================================
# 1.1 ===== Loading Model outputs
infile_name = 'CIVL4145-Tutorial02-Data-ModelOuputs.csv'

# Establishing variables
Date_in = []                                         # Establishes new variable
Model_1_in = []                                      # Establishes new variable
Model_2_in = []                                      # Establishes new variable

# Using for loop to read in data values from csv file sequentially
with open(infile_name) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader)               # This skips the 1st row (header information)
    for row in csvReader:
        Date_in.append(row[0])   # Appends 1st value in row to Date_in variable
        Model_1_in.append(row[1])
        Model_2_in.append(row[2])
        
del infile_name, row                         # Deleting variables to de-clutter

# Converting dates from string to datetime for plotting
dims = np.shape(Date_in)
Date_Models = []
for i in range(0,dims[0]):
    tempDate_str = Date_in[i]
    temp_PD = datetime.datetime.strptime(tempDate_str, '%d/%m/%Y %H:%M')
    Date_Models.append(temp_PD)
del tempDate_str, temp_PD, i, dims, Date_in

# 1.2 ===== Loading Daily monitoring data
infile_name = 'CIVL4145-Tutorial02-Data-EnvironmentalData-Daily.csv'

# Establishing variables
Date_in = []                                         # Establishes new variable
Data_in = []                                         # Establishes new variable

# Using for loop to read in data values from csv file sequentially
with open(infile_name) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader)         # This skips the 1st row (header information)
    for row in csvReader:
        Date_in.append(row[0]) # Appends 1st value in row to Date_in variable
        Data_in.append(row[1]) # Appends 2nd value in row to Data_in variable
        
del infile_name, row      # Deleting variables to de-clutter

# Converting dates from string to datetime for plotting
dims = np.shape(Date_in)                  # Gets dimensions of Date_in variable
Date_EnvDataDaily = []                               # Establishes new variable
for i in range(0,dims[0]):
    tempDate_str = Date_in[i]
    temp_PD = datetime.datetime.strptime(tempDate_str, '%d/%m/%Y %H:%M')
    Date_EnvDataDaily.append(temp_PD)
del tempDate_str, temp_PD, i, dims, Date_in

# Converting gaps in data to "NaN" values
# (only applies to first data values - process shown for future reference)
Data_EnvDataDaily = np.array(Data_in)       # Copies input data to new variable
Data_EnvDataDaily[Data_EnvDataDaily==''] = np.nan  # Converts empty data to NaN
Data_EnvDataDaily=[float(x) for x in Data_EnvDataDaily]
del Data_in                                  # Deleting variables to de-clutter

# 2.0 ===== EXTRACTING MODEL DATA AT DAILY TIME STEPS =========================
# Note that monitoring data is 2 days longer than model output data so be 
# sure to adjust the range overwhich the analysis is performed.
dims = np.shape(Date_EnvDataDaily)
Data_ModelsDaily = np.zeros((dims[0]-2,2))                            # Note -2
for i in range(0,dims[0]-2):                                          # Note -2
    idx = Date_Models.index(Date_EnvDataDaily[i])    # finds row index of match
    Data_ModelsDaily[i,0] = float(Model_1_in[idx])    # replaces with NTU value
    Data_ModelsDaily[i,1] = float(Model_2_in[idx])    # replaces with NTU value
    
del dims, idx

# 2.1 ===== Exporting all daily data to single csv file
outFileName = 'ModelDataDaily.csv'
header1 = ['Date', 'Observed','Predicted_1', 'Predicted_2']
header2 = ['[dd-mm-yyyy]', '[NTU]', '[NTU]', '[NTU]']
# Using "zip" funciton to combine variables
outData = zip(Date_EnvDataDaily[0:-2], Data_EnvDataDaily[0:-2],
              Data_ModelsDaily[:,0], Data_ModelsDaily[:,1])
with open(outFileName,'w') as f:
    writer = csv.writer(f,lineterminator='\n')
    writer.writerow(header1)
    writer.writerow(header2)
    for row in outData:
        writer.writerow(row)

del outFileName, header1, header2, outData

# 3.0 ===== CALCULATING SKILL SCORES ==========================================
# Note the first day's data is excluded for all data as the NaN value in the
# observation data set will cause errors in calculating the mean. Also the last
# 2 days of observed data is discarded so the end date matches the model data.

O = Data_EnvDataDaily[1:-2]              # Observation data without last 2 days
Omean = np.mean(O)                       # Mean of observation data
P1 = Data_ModelsDaily[1:,0]               # Model 1 daily data (first column)
P1mean = np.mean(P1)                     # Mean of model 1 daily data
P2 = Data_ModelsDaily[1:,1]               # Model 2 daily data (2nd column)
P2mean = np.mean(P2)                     # Mean of model 2 daily data
dims = np.shape(P1)
n = dims[0]

# 3.1 Pearson's correlation coefficient
# Using equation from table 5 of Moriasi et al 2015)
r1 = (np.sum((O-Omean)*(P1-P1mean)))/(np.sqrt(np.sum((O-Omean)**2))*
      np.sqrt(np.sum((P1-P1mean)**2)))
R1 = r1**2

r2 = (np.sum((O-Omean)*(P2-P2mean)))/(np.sqrt(np.sum((O-Omean)**2))*
      np.sqrt(np.sum((P2-P2mean)**2)))
R2 = r2**2

# 3.2 NSE
# Using equation from table 5 of Moriasi et al 2015)
NSE1 = 1 - ((np.sum((O-P1)**2))/(np.sum((O-Omean)**2)))
NSE2 = 1 - ((np.sum((O-P2)**2))/(np.sum((O-Omean)**2)))

# 3.3 RMSE
# Using equation from table 5 of Moriasi et al 2015)
RMSE1 = np.sqrt((1/n)*np.sum((O-P1)**2))
RMSE2 = np.sqrt((1/n)*np.sum((O-P2)**2))

# 3.4 PBIAS
# Using equation from table 5 of Moriasi et al 2015)
PBIAS1 = ((np.sum(O-P1))/(np.sum(O)))*100
PBIAS2 = ((np.sum(O-P2))/(np.sum(O)))*100

# 3.5 Exporting skill scores to single csv file
outFileName = 'SkillScores.csv'
header1 = ['Skill Score', 'Model 1','Model 2']
ListOfSkillScores = 'r','R_squared','NSE','RMSE','PBIAS'
Model_1_Scores = r1,R1,NSE1,RMSE1,PBIAS1
Model_2_Scores = r2,R2,NSE2,RMSE2,PBIAS2
# Using "zip" funciton to combine variables
outData = zip(ListOfSkillScores, Model_1_Scores,Model_2_Scores)
with open(outFileName,'w') as f:
    writer = csv.writer(f,lineterminator='\n')
    writer.writerow(header1)
    for row in outData:
        writer.writerow(row)

del outFileName, header1, ListOfSkillScores, Model_1_Scores, Model_2_Scores

# 4.0 ===== PLOTTING DATA =====================================================
# A reference source to get started: 
# https://realpython.com/python-matplotlib-guide/
# https://matplotlib.org/api/axes_api.html?highlight=axes%20class#plotting
#
# Need to run the line below once in each session to adjust setting to plot
# in separate window - not at command line.
# %matplotlib qt

# To return to inline plot at command line use %matplotlib inline 

# ===== Setting plot formatting (global settings - applies to all plots) =====
mS = 18 # Used to set marker size
lW = 3 # Used to set linewidth
fS = 28 # Used to set font size
plt.rcParams['font.family'] = 'Times New Roman' # Globally sets the font type
plt.rc('font',size=fS)
plt.rc('axes',titlesize=fS)
plt.rc('axes',labelsize=fS)
plt.rc('xtick',labelsize=fS)
plt.rc('ytick',labelsize=fS)
plt.rc('legend',fontsize=fS)
plt.rc('figure',titlesize=fS)

# Setting dates for use as start and end of x-axes
stDate = datetime.datetime.strptime('2013-3-25 00:00:00', '%Y-%m-%d %H:%M:%S')
enDate = datetime.datetime.strptime('2013-5-11 00:00:00', '%Y-%m-%d %H:%M:%S')

# ===== 4.1 Time series plot
fig, (ax1) = plt.subplots(1, 1, figsize=(14,7), dpi=50)

ax1.plot(Date_EnvDataDaily,Data_EnvDataDaily,'-o',c='b',
         label='Environmental Data', markersize=mS, linewidth=lW)
ax1.plot(Date_EnvDataDaily[0:-2],Data_ModelsDaily[:,0],'-s',c='k',
         label='Model 1 Data', markersize=mS, linewidth=lW)
ax1.plot(Date_EnvDataDaily[0:-2],Data_ModelsDaily[:,1],'-^',c='r',
         label='Model 2 Data', markersize=mS, linewidth=lW)
date_formatter = mdates.DateFormatter('%d-%m')
ax1.xaxis.set_major_formatter(date_formatter)
ax1.grid()
ax1.set_xlim(stDate,enDate)
ax1.set_ylim(-10,500)
ax1.set_xlabel('Date in 2013 [dd-mm]')
ax1.set_ylabel('Turbidity [NTU]')
ax1.set_title('Turbidity time series')
ax1.legend(loc='upper left')

# ===== 4.2 Correlation plot
fig, (ax1) = plt.subplots(1, 1, figsize=(14,14), dpi=50)

ax1.plot(Data_EnvDataDaily[1:-2],Data_ModelsDaily[1:,0],'s',c='k',
         label='Model 1 Data', markersize=mS, linewidth=lW)
ax1.plot(Data_EnvDataDaily[1:-2],Data_ModelsDaily[1:,1],'^',c='r',
         label='Model 2 Data', markersize=mS, linewidth=lW)
ax1.grid()
ax1.set_xlim(-10,500)
ax1.set_ylim(-10,500)
ax1.set_xlabel('Observed [NTU]')
ax1.set_ylabel('Predicted [NTU]')
ax1.set_title('Correlation plot')
ax1.legend(loc='upper left')

# =============================================================================
# ======== END OF SCRIPT ======== END OF SCRIPT ======== END OF SCRIPT ========
# =============================================================================
