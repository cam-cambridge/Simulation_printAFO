import AFO0_Simulation
import AFO1_DesignParameter
import os
import AFO2_MBDModel
import AFO3_ParaTestSelect
import numpy as np
import AFO4_ResultsCollection
import AFO5_DoE
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import itertools

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# New AFO design in the musculoskeletal model with stripe orientations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#AFO0_Simulation.Simulation('AFODroplanding', 'model', 'Simulationoutput')
#AFO0_Simulation.Simulation('Walk_AFO', 'model', 'Gait results collection')
#AFO0_Simulation.Simulation('RRA_run', 'model', 'Gait results collection')
#AFO0_Simulation.Simulation('Run_AFO', 'model', 'Model outputs')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Batch simulation for the DL, walk and run
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(4,5), range(1,2), range(4,5), range(4,5)):
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(0,1), range(5,6), range(0,1), range(0,1)):
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(5,6), range(10,11), range(0,1), range(5,6)):
            # The scaling of force-length relationship
            FL_amplification_1=af_am_1*10
            FL_amplification_2=af_am_2*10
            FL_amplification_3=af_am_3*10
            FL_amplification_4=af_am_4*10
            # The shift of force-length relationship
            FL_shift_1=af_shift_1*0.04-0.2
            FL_shift_2=af_shift_2*0.04-0.2
            FL_shift_3=af_shift_3*0.04-0.2
            FL_shift_4=af_shift_4*0.04-0.2
            # The orientation of AFO strip
            Strip_orientation=np.array([strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4])
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Change the design parameters in the AFO design text file
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_1, FL_shift_1, 'AFO_FLrelationship_one')
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_2, FL_shift_2, 'AFO_FLrelationship_two')
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_3, FL_shift_3, 'AFO_FLrelationship_three')
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_4, FL_shift_4, 'AFO_FLrelationship_four')
            AFO3_ParaTestSelect.AFOmaterialVariables(Strip_orientation,Strip_orientation,'AFO_stripe_orientations')
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # The batch of simulation
            # The drop landing simulation DL
            ResultDirectory_DL='SimulationOutput_DL_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory_DL)
            # The walking simulation Walk
            ResultDirectory_Walk='SimulationOutput_Walk_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            AFO0_Simulation.Simulation('Walk_AFO', 'model', ResultDirectory_Walk)
            # The running simulation Run
            ResultDirectory_Run='SimulationOutput_Run_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            AFO0_Simulation.Simulation('Run_AFO', 'model', ResultDirectory_Run)
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Resume the design parameters to origin value in the AFO design parameter files
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_1, -FL_shift_1, 'AFO_FLrelationship_one')
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_2, -FL_shift_2, 'AFO_FLrelationship_two')
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_3, -FL_shift_3, 'AFO_FLrelationship_three')
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_4, -FL_shift_4, 'AFO_FLrelationship_four')
            AFO3_ParaTestSelect.AFOmaterialVariables(-Strip_orientation,-Strip_orientation,'AFO_stripe_orientations')
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------

            """
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #  Put the simulation results from the results folders to an excel documents
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
            Subtalar_matrix=[]
            for asi in range (4,13):                                        # The number of the amplification variables for side FL relationship
                for afj in range (4,13):                                    # The number of the amplification variables for front FL relationship
                    for ssm in range (0,10):                              # The number of the shift variables for side FL relationship
                        for sfn in range (0,10):                           # The number of the shift variables for front FL relationship
                            output_folder=ResultDirectory='Drop landing_platform30\SimulationOutput_DL_'+str(asi)+str(afj)+str(ssm)+str(sfn)                # The folder of the FD results
                            data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')                        # put the specified results into a matrix
                            if data.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                                continue
                            else:
                                Subtalar_matrix.append([asi*10, afj*10, ssm*0.04-0.2, sfn*0.04-0.2, max(data[:,1]), max(data[:,2])])           # Put the four variables and the subtalar angles into a list
            Subtalar_matrix=np.array(Subtalar_matrix)                                                        # Transform the list to the matrix
            Excel_title=['Side_amplification','Front_amplification','Side_shift','Front_shift','Max subtalar angle', 'Max ankle angle']              # Define the title of the excel
            AFO4_ResultsCollection.DLResultstoExcel('Drop landing_platform30', 'DL Results.xls', 'Platform 30', Excel_title, Subtalar_matrix)          # Put the four variables and subtalar angles to an excel
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            """




"""delete in 20210912
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Batch simulation for the DL, walk and run
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for a1i in range (4,5):
    for a1j in range (0,1):
        for a2i in range (4,5):
            for a2j in range (0,1):
                for a3i in range (4,5):
                    for a3j in range (0,1):
                        for a4i in range (4,5):
                            for a4j in range (0,1):
                                FL_amplification_1=a1i*10
                                FL_shift_1=a1j*10
                                FL_amplification_2=a2i*10
                                FL_shift_2=a2j*10
                                FL_amplification_3=a3i*10
                                FL_shift_3=a3j*10
                                FL_amplification_4=a4i*10
                                FL_shift_4=a4j*10
                                # Change the AFO material properties in input file
                                AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_1, FL_shift_1, 'AFO_FLrelationship_one')
                                # The drop landing simulation DL
                                ResultDirectory_DL='SimulationOutput_DL_'+str(a1i)+str(a1j)+str(a2i)+str(a2j)
                                AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory_DL)
                                # The walking simulation Walk
                                ResultDirectory_Walk='SimulationOutput_Walk_'+str(a1i)+str(a1j)+str(a2i)+str(a2j)
                                AFO0_Simulation.Simulation('Walk_AFO', 'model', ResultDirectory_Walk)
                                # The running simulation Run
                                ResultDirectory_Run='SimulationOutput_Run_'+str(a1i)+str(a1j)+str(a2i)+str(a2j)
                                AFO0_Simulation.Simulation('Run_AFO', 'model', ResultDirectory_Run)
                                #AFO0_Simulation.Simulation('Run_AFO', 'simulation', ResultDirectory_Run)
#
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Put the simulation results from the results folders to an excel documents
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
Subtalar_matrix=[]
for asi in range (4,13):                                        # The number of the amplification variables for side FL relationship
    for afj in range (4,13):                                    # The number of the amplification variables for front FL relationship
        for ssm in range (0,10):                              # The number of the shift variables for side FL relationship
            for sfn in range (0,10):                           # The number of the shift variables for front FL relationship
                output_folder=ResultDirectory='Drop landing_platform30\SimulationOutput_DL_'+str(asi)+str(afj)+str(ssm)+str(sfn)                # The folder of the FD results
                data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')                        # put the specified results into a matrix
                if data.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    Subtalar_matrix.append([asi*10, afj*10, ssm*0.04-0.2, sfn*0.04-0.2, max(data[:,1]), max(data[:,2])])           # Put the four variables and the subtalar angles into a list
Subtalar_matrix=np.array(Subtalar_matrix)                                                        # Transform the list to the matrix
Excel_title=['Side_amplification','Front_amplification','Side_shift','Front_shift','Max subtalar angle', 'Max ankle angle']              # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel('Drop landing_platform30', 'DL Results.xls', 'Platform 30', Excel_title, Subtalar_matrix)          # Put the four variables and subtalar angles to an excel
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Batch simulation for the drop landing - 20210721
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
# The variables of AFO materials in binary system
FL_amplification_side_Varbin=8                     # The s.t. variables in binary system for side AFO in terms of amplification
FL_amplification_front_Varbin=8                   # The s.t. variables in binary system for front AFO in terms of amplification
FL_shift_side_Varbin=5                                   # The s.t. variables in binary system for side AFO in terms of shift
FL_shift_front_Varbin=5                                 # The s.t. variables in binary system for side AFO in terms of amplification
# Change the variables of AFO materials from binary system to decimal numbers
FL_amplification_side_Vardeci=2**FL_amplification_side_Varbin-1
FL_amplification_front_Vardeci=2**FL_amplification_front_Varbin-1
FL_shift_side_Vardeci=2**FL_shift_side_Varbin-1
FL_shift_front_Vardeci=2**FL_shift_front_Varbin-1
"""
"""
for asi in range (4,5):                                        # The number of the amplification variables for side FL relationship
    for afj in range (4,5):                                    # The number of the amplification variables for front FL relationship
        for ssm in range (0,1):                              # The number of the shift variables for side FL relationship
            for sfn in range (0,1):                           # The number of the shift variables for front FL relationship
                FL_amplification_side_Vardeci=asi*10
                FL_amplification_front_Vardeci=afj*10
                FL_shift_side_Vardeci=ssm*0.04-0.2
                FL_shift_front_Vardeci=sfn*0.04-0.2
                # Change the AFO material properties in input file
                AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_side_Vardeci, FL_shift_side_Vardeci, FL_amplification_front_Vardeci, FL_shift_front_Vardeci)
                ResultDirectory='SimulationOutput_DL_'+str(asi)+str(afj)+str(ssm)+str(sfn)
                AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory)
                # Restore the AFO material properties in input file to the baseline materials
                AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_side_Vardeci, -FL_shift_side_Vardeci, 1/FL_amplification_front_Vardeci, -FL_shift_front_Vardeci)
                # print(ResultDirectory)
"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Put the simulation results from the results folders to an excel documents
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
Subtalar_matrix=[]
for asi in range (4,13):                                        # The number of the amplification variables for side FL relationship
    for afj in range (4,13):                                    # The number of the amplification variables for front FL relationship
        for ssm in range (0,10):                              # The number of the shift variables for side FL relationship
            for sfn in range (0,10):                           # The number of the shift variables for front FL relationship
                output_folder=ResultDirectory='Drop landing_platform30\SimulationOutput_DL_'+str(asi)+str(afj)+str(ssm)+str(sfn)                # The folder of the FD results
                data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')                        # put the specified results into a matrix
                if data.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    Subtalar_matrix.append([asi*10, afj*10, ssm*0.04-0.2, sfn*0.04-0.2, max(data[:,1]), max(data[:,2])])           # Put the four variables and the subtalar angles into a list
Subtalar_matrix=np.array(Subtalar_matrix)                                                        # Transform the list to the matrix
Excel_title=['Side_amplification','Front_amplification','Side_shift','Front_shift','Max subtalar angle', 'Max ankle angle']              # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel('Drop landing_platform30', 'DL Results.xls', 'Platform 30', Excel_title, Subtalar_matrix)          # Put the four variables and subtalar angles to an excel
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Put the results in a matrix from an excel file and plot the results in a 4D scatter figures
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Put the results from an excel file into a matrix
Result_folder='Drop landing_platform30'
Result_file='DL Results.xls'
Result_sheet_name='Platform 30'
data=AFO4_ResultsCollection.ReadExcel(Result_folder, Result_file, Result_sheet_name)
data_smallthan30=data[data['Max subtalar']<30].values                          # Matix including subtalar angles smaller than 30 degree
data_bigthan30=data[data['Max subtalar']>=30].values                           # Matix including subtalar angles bigger than 30 degree
# Plot 4D scrater figures for the results
fig=plt.figure()
ax = fig.add_subplot(111, projection='3d')
x1=data_smallthan30[:,0]
x2=data_bigthan30[:,0]
y1=data_smallthan30[:,1]
y2=data_bigthan30[:,1]
z1=data_smallthan30[:,2]
z2=data_bigthan30[:,2]
z11=data_smallthan30[:,3]
z22=data_bigthan30[:,3]
c1=data_smallthan30[:,4]
c2=data_bigthan30[:,4]
#img=ax.scatter(x2,y2,z2,s=100,c=c2,cmap=plt.bone())
img=ax.scatter(x1,y1,z11,s=100,c=c1,cmap=plt.autumn())
# Choice available: hot, cool, gray, bone, white, spring, summer, autumn, winter
ax.set_xlabel("Side_amplifcation")
ax.set_ylabel("Front_amplification")
ax.set_zlabel("Front_shift")
fig.colorbar(img)

plt.show()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

#AFO0_Simulation.Simulation('walk', 'simulation', 'directory')
#AFO0_Simulation.Simulation('AFODroplanding', 'model', 'directory')
#AFO0_Simulation.Simulation('gait_AFO', 'model', 'directory')
"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Gait simulation
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ----------------------------------------------------------------------------------------------------------------------
 # (1) Perform gait simulation, including scaling, inverse dynamics, RRA, CMC, forward dynamics
#AFO0_Simulation.Simulation('Walk', 'simulation', 'directory')
# ----------------------------------------------------------------------------------------------------------------------
# (2) Put the simulation results from the results folders to an excel documents
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
output_folder='Gait simulation data\Model outputs\\5_ForwardDynamics'                                                                                                     # The folder of the FD results
data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'Walk_states_degrees.mot')                        # put the specified results into a matrix
AFO4_ResultsCollection.DLResultstoExcel('Gait simulation data\Model outputs\Gait results collection'  , 'Gait Results.xls', 'Gait', Results_parameter, data)
# Gait simulation
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
#  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Drop landing DoE
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ----------------------------------------------------------------------------------------------------------------------
# (1) Determin factor levels, perform MBD simulation for DoE based on the factor levels
# Two factor levels: high level: level=1, low level: level=0
for i in range (2):
    for j in range (2):
        for m in range (2):
            for n in range (2):
                print(i,j,m,n)
                ResultDirectory='SimulationOutput_DOE_'+str(i)+str(j)+str(m)+str(n)
                AFO5_DoE.DoESimulation(i, j, m, n, 'model', ResultDirectory)
# ----------------------------------------------------------------------------------------------------------------------
# (2) Put the simulation results from the results folders to an excel documents
# Inputs: output_folder_prefix, Results_parameter
output_folder_prefix='SimulationOutput_DOE_'
for i in range (2):
    for j in range (2):
        for m in range (2):
            for n in range (2):
                output_folder_sheetname=output_folder_prefix+str(i)+str(j)+str(m)+str(n)
                output_folder=os.path.join('Drop landing', output_folder_sheetname)
                Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']
                data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')
                AFO4_ResultsCollection.DLResultstoExcel('Drop landing\MBD Results', 'DoE Results.xls', output_folder_sheetname, Results_parameter, data)
# ----------------------------------------------------------------------------------------------------------------------
# (3) Export the MBD simulation results from the excel file .xls, and pick up important value such as maximum value
# Inputs: # File_folder: the folder that include the results excel file, default='MBD Results'
               # File_excel: the name of the results excel, default='DoE Results.xls'
               # Results_collect_parameters: the results of interest that will be collected from the results excel, default=['time', '/jointset/subtalar_r/subtalar_angle_r/value']
# Output: # M_DoEInput: the matrix that includes the import value of simulation results
File_folder='MBD Results'
File_excel='DOE Results.xls'
Results_collect_parameters='/jointset/ankle_r/ankle_angle_r/value'
Simulation_results=AFO4_ResultsCollection.DoEResultsfromExcel (File_folder, File_excel, Results_collect_parameters)
print(Simulation_results)
# ----------------------------------------------------------------------------------------------------------------------
# (4) Perform DoE analysis
inputs_labels = {'x1' : 'Mechanical amplifcation_side (A)',
                 'x2' : 'Mechanical_shift_side (B)',
                 'x3' : 'Mechanical amplification_front (C)',
                 'x4': 'Mechanical_shift_front (D)'}
factors_value = [('x1',3,60),
        ('x2',0,-0.4),
        ('x3',3,60),
        ('x4', 0, -0.4)]
s=AFO5_DoE.StatiAna(inputs_labels, factors_value, Simulation_results)
print(s)
# Drop landing DoE
#  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""


# Previous old code
"""
output_folder_prefix='SimulationOutput_DOE_'
for i in range (0,5):
    output_folder=output_folder_prefix+str(i)
    output_folder=os.path.join('Drop landing', output_folder)
    Results_parameter=['time', '/jointset/ankle_r/ankle_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']
    data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')
    AFO4_ResultsCollection.DLResultstoExcel('Drop landing\MBD Results', 'DL Results11.xls', output_folder, Results_parameter, data)
"""
"""
#--------------------------------------------------------------------------------------------------------------------------------------------
# For force-length relationship_amplification
AFO_FLrelationship=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input_default.txt', 'AFO_FLrelationship')
for i in range (5):
    AFO_FLrelationship[0]=AFO_FLrelationship[0]-0.1*(i+1)
    print(AFO_FLrelationship[0])
    print(AFO_FLrelationship[1])
    ResultDirectory='SimulationOutput_'+'AFO_FLrelationship'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', 'AFO_FLrelationship', AFO_FLrelationship)
    AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory)
#--------------------------------------------------------------------------------------------------------------------------------------------
# For force-length relationship_amplification
AFO_FLrelationship=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'AFO_FLrelationship')
for i in range (2):
    AFO_FLrelationship[0]=AFO_FLrelationship[0]-0.1*(i+1)
    print(AFO_FLrelationship[0])
    print(AFO_FLrelationship[1])
    ResultDirectory='SimulationOutput_'+'AFO_FLrelationship'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_FLrelationship', AFO_FLrelationship)
    AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory)
#--------------------------------------------------------------------------------------------------------------------------------------------
# For force-length relationship_amplification
AFO_FLrelationship=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'AFO_FLrelationship')
for i in range (10):
    AFO_FLrelationship[1]=AFO_FLrelationship[1]*(i/20+1)
    print(AFO_FLrelationship[1])
    ResultDirectory='SimulationOutput_'+'AFO_FLrelationship'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_FLrelationship', AFO_FLrelationship)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory)
#--------------------------------------------------------------------------------------------------------------------------------------------
# For number of strips in side
num_side=int(AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'num_side'))
for i in range (5):
    print(num_side)
    ResultDirectory='SimulationOutput_'+'num_side'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'num_side', num_side)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory)
    num_side=num_side+1
#--------------------------------------------------------------------------------------------------------------------------------------------
# For number of strips in front
num_front=int(AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'num_front'))
for i in range (5):
    print(num_front)
    ResultDirectory='SimulationOutput_'+'num_front'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'num_front', num_front)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory)
    num_front=num_front+1
Platform_inclination=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'Platform_inclination')
Inclination_increment=[5,0,0]
for i in range (2):
    Platform_inclination=Platform_inclination+Inclination_increment
    print(Platform_inclination)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'Platform_inclination', Platform_inclination)
    AFO0_Simulation.Simulation('AFODroplanding', 'model')
AFO_side_top_iniPosAngle=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'Platform_inclination')
angle_increment=1
for i in range (10):
    AFO_side_top_iniPosAngle=AFO_side_top_iniPosAngle+angle_increment
    print(AFO_side_top_iniPosAngle)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_side_top_iniPosAngle', AFO_side_top_iniPosAngle)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation')
AFO_side_bottom_iniPosAngle=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'Platform_inclination')
angle_increment=1
for i in range (10):
    AFO_side_bottom_iniPosAngle=AFO_side_bottom_iniPosAngle+angle_increment
    print(AFO_side_bottom_iniPosAngle)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_side_bottom_iniPosAngle', AFO_side_bottom_iniPosAngle)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation')
"""
