# Simulation_printAFO
This repository mainly includes the python codes, OpenSim musculoskeletal models and associated files for the musculoskeletal simulation of the 3D printed AFO.

## **1. Python installation** <br/>

(1) It should be noted that starting with 4.0, OpenSim is distributed as 64-bit only, so you must use 64-bit Python. If you are using 4.0, you need Python 2.7.x. If you are using 4.1 or 4.2, you need Python 3.7.x. <br/>
(2) After installing the python 3.7.x, install modules "numpy","pandas", "mpl_toolkits", "xlwt", "xlrd", xlutils", "openpyxl".

## **2. Architecture of the files and folders** <br/>

![image](https://user-images.githubusercontent.com/14294455/143143898-af1cb7da-dccf-4e96-b800-2dfbe2634f57.png)

The batch simulation pipeline is stricted to the architecture of the files and folers, as shown in the figure above: <br/>
***Simulation_printeAFO:*** the folder for all the simulation pipeline files. All the folders and codes should be put in this folder in the architecture shown above. The folder include AFO Design folder, Drop landing folder, Gait simulation folder, Running simulation folder, Batch simulation code folder. <br/>
***AFO Design:*** the design parameters for the AFO in .txt format. It includes two files: AFO input_default: the original design parameters; AFO input: the desgin paraeters for the AFO models in the musculoskeletal models. The AFO Design folder can be downloaded directly from the repo. <br/>
***Drop landing:*** the drop landing model and associated files. The Drop landing folder can be downloaded directly from the repo. <br/>
***Gait simulation:*** the musculoskeletal models and files required for the gait simulation. Due to the large size of the files, the files were separated into two folders, one is "Gait Simulation.rar", which should be decompressed after downloaded, the second one is "4_CMC.rar", which should be decrompressed and then putted into the "Gait simulation" folder. <br/>
***Running simulation:*** the musculoskeletal models (same with the model for gait simulation) and files required for the running simulation. It should be decompressed after downloaded. <br/>
***Batch simulation code:*** the code for the batch simulation. Apart from the above folders, all the codes should be downloaded and put in the "Batch simulation code" folder.

## **3. Batch simulation code** <br/>

The batch simulation code will change the design parameters, develop the AFO representation in the model and run the simulations automatically. It includes:<br/>

*---  (Code 0):* The normal whole process of walk and running simulation (no AFO), including model scaling, inverse kinematics (IK), residual reduction algorithm (RRA), and forward dynamics (FD);<br/>
*---  (Code 1):* The determination of ranges of the design variables and the step sizes for each variable during optimization. This was also the nessary inputs for the following codes (3-6);<br/>
*---  (Code 2):* The running of walk and run simulation for models without AFO; <br/>
*---  (Code 3):* The batch simulation for the drop landing, walk and running, using a loop to run the simulations autormatically; <br/>
*---  (Code 4):* Put the drop landing simulation results from the simulation results folders to an excel documents; <br/>
*---  (Code 5):* Put the walk simulation results from the simulation results folders to an excel documents; <br/>
*---  (Code 6):* Put the running simulation results from the simulation results folders to an excel documents. <br/>

***(Code 0): The normal whole process of walk and running simulation:*** <br/>
This part of codes is a normal simulation process for the walk and running activities, which will perform model scaling, inverse kinematics (IK), residual reduction algorithm (RRA), computed muscle control (CMC) and forward dynamics. The results of the model scaling, IK and RRA will be used in the following codes. The simulation results will be stored in: Simulation_printAFO\Gait simulation\Model outputs.<br/>

***(Code 1): The determination of ranges of the design variables and step size for each variable for optimization:*** <br/>
This part of codes is to provide the values or the ranges of the design variables for the AFO representation in the model and simulation, using the following equations:
```
# The ranges for design variables
Var_range_FL_amplification=[range(1,2), range(1,2), range(1,2), range(1,2)]         # Range of design variables: force-length amplification (fl_am)
Var_rang_FL_shift=[range(0,1), range(0,1), range(0,1), range(0,1)]                  # Range of design variables: force-length shift (fl_shift)
Var_range_stripe_orientation=[range(0,1), range(0,1), range(0,1), range(0,1)]       # Range of design variables: stripe orientation (strip_ori)
Var_range_bottom_location=[range(0,1), range(0,1), range (0,1), range(0,1)]         # Range of design variables: bottom endpoint location (bottom_location)
```
This part of code is also to provide the step sizes for the design variables for batch simulation and optimization:<br/>
```
# The step size for each design variable during optimization
FL_amplification_stepsize=60                      # The step size for the design parameter: force-length amplification, can be changed to any number
FL_shift_stepsize=0.2                             # The step size for the design parameter: force-length shift, can be changed to any number
strip_orientation_stepsize=5                      # The step size for the design parameter: strap orientation, can be changed to any number
bottom_location_stepsize=5                        # The step size for the design parameter: bottom endpoint location, can be changed to any number
```
This part of codes will be used as input in the following steps (Codes 3-6), the explaination of which will be elaborated below. <br/>

***(Code 2): The walk and running simulation for the models with and without AFO:*** <br/>
This part of codes will run the CMC simulation of walk and running activities for the model without AFO. These simulations should be performed based on the results from the model scaling, IK, RRA in code 0, the results of which will be used to compute the differences of muscle forces or demand between the models with and without AFO.
The results of this part of simulation will store in: Simulation_printAFO\Gait simulation\Model outputs\4_CMC\SimulationOutput_Walk_0000000000000000.<br/>

***(Code 3): Batch simulation for the drop landing, walk and run:*** <br/>
This part of codes will develop AFO representation in the MSK model based on a series of design parameters and run the model automatically, the processes are: (1) a set of design parameters for the AFO will be provided in a text file - AFO input.txt, located in: Simulation_printAFO\AFO Design; (2) an AFO representation will be created in the MSK model based on the design parameters in the AFO input.txt file; (3) the codes will change the design parameters of the AFO in the AFO input.txt file and a new AFO representation will be created in the MSK model automatically; (4) the codes will then run the simulation of drop landing, walk and running. All of these will be achieved through a loop code: <br/>

***(i) The change of design parameters in the AFO design.txt file in the AFO Design folder:***<br/>

```
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product (*Var_range_FL_amplification):            # Design variable: force-length amplification (fl_am)
```
This code will determine the amplification parameters of the AFO materials (force-length relationship) for the four stripes based on the range of design variables of the force-length amplification defined in ***Code 1*** (Var_range_FL_amplification). The amplification is defined as the scaling factors of the force generated by the AFO strape with the same extension, and is determined using the following equation:
```
# The amplification (scaling) of the force-length relationship
FL_amplification_1=fl_am_1*FL_amplification_stepsize
FL_amplification_2=fl_am_2*FL_amplification_stepsize
FL_amplification_3=fl_am_3*FL_amplification_stepsize
FL_amplification_4=fl_am_4*FL_amplification_stepsize
```
where the FL_amplification_stepsize is the step size of the design variable (FL_amplification) during the optimization, which was defined in ***Code (1)***. It can be changed and defined as needed during the optimization.<br/>
The design varibale FL_amplifcation represents the number of the fibres in each strip of the AFO. e.g., in the current case, the amplification variables of the four stripes of the AFO are 60, 60, 60 and 60, respectively, representing the fibres for the four stripes are 60, 60, 60 and 60.<br/>

```
for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(*Var_rang_FL_shift):    # Design variable: force-length shift (fl_shift)
```
This code will determine the shift parameters of the AFO materials for the four stripes based on the range of design variables of the force-length shift defined in ***Code 1*** (Var_rang_FL_shift). The shift parameters can be determined using the following equation:
```
FL_shift_1=fl_shift_1*FL_shift_stepsize-0.2
FL_shift_2=fl_shift_2*FL_shift_stepsize-0.2
FL_shift_3=fl_shift_3*FL_shift_stepsize-0.2
FL_shift_4=fl_shift_4*FL_shift_stepsize-0.2
```
where the FL_shift_stepsize is the step size of the design variable of FL_shift during the optimization. It was defined in ***Code (1)*** and can be changed as needed for the optimization.<br/>
The shift parameters of the AFO are defined as the translation of the force-length curve of the AFO materials. E.g., in the current case, the shift parameters for the four stripes are -0.2 (0x0.2-0.2), -0.2 (0x0.2-0.2), -0.2 (0x0.2-0.2) and -0.2 (0x0.2-0.2), respectively, which means the force-length curve will move 0.2 units to the left.<br/>

```
for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product (*Var_range_stripe_orientation):         # Deisgn variable: stripe orientation (strip_ori)
```
This code will determine the orientations of the stripes of the AFO for the four stripes, which can be determined using the following equation:
```
Strip_orientation=np.array([strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4])*strip_orientation_stepsize
```
where the strip_orientation_stepsize is the step size of the design variable of Strip_orientation in the optimization. It was defined in ***Code (1)*** and can be changed as needed for the optmization.<br/>

```
for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product (*Var_range_bottom_location):    # Design variable: bottom endpoint location (bottom_location)
```
This code will determine the locations of the endpoints of the AFO representations at the bottom side (e.g. the location of the AFO representation relative to the leg segment). The locations can be determined using the following equation:
```
bottom_location_angle=np.array([bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4])*bottom_location_stepsize
```
where the bottom_location_stepsize was defined in ***Code (1)***, and can be changed as needed during the optimization.<br/>

The definations of the design parameters in the AFO can be found in the Guidelines in the repo.<br/>

***(ii) The development of AFO in the musculoskeletal model and run the simulation:***<br/>

After the design parameters in the AFO design'txt file were changed, the main code will call the module "AFO0_Simulation" module to create AFO representation in the musculoskeletal model and run the simulation: <br/>
```
AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory_DL)
```
This code will call the module "AFO0_Simulation" module to demonstrate the musculoskeletal model with AFO representation and run the simulation of activities. There are three parameters that can be changed when calling the module for different purposes: <br/>
*First parameter:* to determine the simulated activities <br/>
>>>>>>'AFODroplanding': to demonstrate and run drop landing model with AFO <br/>
>>>>>>'Walk_AFO' or 'Run_AFO': to demonstrate and run walk or running model with AFO <br/>

*Second parameter:* to determine whether demonstrating the MSK model or running the simulation:<br/>
>>>>>> 'model': to demonstrate the MSK model with AFO <br/>
>>>>>> 'simulation': to run drop landing, walk and running simulations <br/>

*Third parameter:* the folder for storing the drop landing simulation results <br/>

After the batch of simulation, the simulation results will store in:<br/>
*Drop landing:* .\Simulation_printAFO\Drop landing\DL simulation results <br/>
*Gait simulation:* .\Simulation_printAFO\Gait simulation\Model outputs\4_CMC <br/>
*Running simulation:* .\Simulation_printAFO_CAMG\Running simulation\Model outputs\4_CMC <br/>

***(Code 4): Collection of the drop landing simulation results and put them into an excel file:*** <br/>

This part of codes will collect the interested simulation results from the drop landing and put them into an excel file. <br/>
For drop landing, the interested simulation result parameters are: maximum subtalar angle, maximum ankle angle:
```
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']     # The specified parameter to extract
```
Similarly, the codes use a loop to collect the results from the simulation result of each AFO design, therefore, the parameters of range in the loop syntax should be changed to correspond to the loop syntax in the AFO design parameters (e.g. section (i))
```
or af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(2,3), range(8,9), range(1,2), range(3,4)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):
```
After running, the excel file will be stored in *.\Simulation_printAFO\Drop landing\DL simulation results * <br/>

***(Code 5): Collection of the walk simulation results and put them into an excel file:*** <br/>

This part of codes will collect the interested simulation results from the walk simulation, and put them into an excel file. <br/>
For walk, the interested simulation result parameters are: average differences of muscle forces/demand beween models with and without AFO across the whole cycle:

```
Results_parameter=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r', 'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r', 'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']              # The specified parameter to extract
```
This code provides the information about what results will collect from the simulation results, i.e. the instant time of the cycle, the name of each muslce in the MSK model. <br/>

Similarly, the codes use a loop to collect the results from the batch simulation of each AFO design, therefore, the parameters of range in the loop syntax should be correspond to the loop syntax in the AFO design parameters, which is determined using the ranges of design variables defined in ***Code 1***:
```
# For walk and run, sum the differences of muscle forces over the whole cycle
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product (*Var_range_FL_amplification):                # Design variable: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(*Var_rang_FL_shift):          # Design variable: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product (*Var_range_stripe_orientation):           # Deisgn variable: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product (*Var_range_bottom_location):  
                        # Design variable: bottom endpoint location (bottom_location)
```
When running the code, a dialog box will appear, asking to select the batch simulation results folder. Select the model outputs folder, (e.g. **./Simulation_printAFO/Gait simulation/Modeloutputs**), the excel file will be stored in the selected folder (e.g. **./Simulation_printAFO/Gait simulation/Modeloutputs**).

***(Code 6): Collection of the running simulation results and put them into an excel file:*** <br/>

This part of codes will collect the interested simulation results from the running simulation, and put them into an excel file. <br/>
For running, the interested simulation result parameters are: average differences of muscle forces/demand beween models with and without AFO across the whole cycle:
```
Results_parameter=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r', 'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r', 'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']                       # The specified parameter to extract
```
This code provides the information about what results will collect from the simulation results, i.e. the instant time, the name of each muslce in the MSK model. <br/>

Similarly, the codes use a loop to collect the results from the batch simulation of each AFO design, therefore, the parameters of range in the loop syntax should be correspond to the loop syntax in the AFO design parameters, which is determined using the ranges of design variables defined in ***Code 1***:
```
# For walk and run, sum the differences of muscle forces over the whole cycle
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product (*Var_range_FL_amplification):            # Design variable: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(*Var_rang_FL_shift):      # Design variable: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product (*Var_range_stripe_orientation):   # Deisgn variable: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product (*Var_range_bottom_location):     
                        # Design variable: bottom endpoint location (bottom_location)
```
When running the code, a dialog box will appear, asking to select the batch simulation results folder. Select the model outputs folder, (e.g. **./Simulation_printAFO/Running simulation/Modeloutputs**), the excel file will be stored in the selected folder (e.g. **./Simulation_printAFO/Running simulation/Modeloutputs**).

**Tips:** The seven parts of the codes are disabled using "" symbols before and after the codes, which should be removed to enable the code for running. The seven parts of codes can also be run one by one by removing the """ symbols before and after each part of the codes. 
