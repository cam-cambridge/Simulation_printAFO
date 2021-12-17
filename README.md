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
This part of codes is a normal simulation process for the walk and running activities, which will perform model scaling, inverse kinematics (IK), residual reduction algorithm (RRA), computed muscle control (CMC) and forward dynamics. The results of the model scaling, IK and RRA will be used in the following codes. The simulation results will be stored in the Simulation_printAFO\Gait simulation\Model outputs folder.<br/>

***(Code 1) The determination of ranges of the design variables and step size for each variable for optimization:*** <br/>
This part of codes is to provide the values or the ranges of the design variables for the AFO representation in the model and simulation, using the following equations:
```
# The ranges for design variables
Var_range_FL_amplification=itertools.product(range(1,2), range(1,2), range(1,2), range(1,2))     # Range of design variables: force-length amplification (fl_am)
Var_rang_FL_shift=itertools.product(range(0,1), range(0,1), range(0,1), range(0,1))              # Range of design variables: force-length shift (fl_shift)
Var_range_stripe_orientation=itertools.product(range(0,1), range(0,1), range(0,1), range(0,1))   # Range of design variables: stripe orientation (strip_ori)
Var_range_bottom_location=itertools.product(range(0,1), range(0,1), range (0,1), range(0,1))     # Range of design variables: bottom endpoint location (bottom_location)
```
This part of code is also to provide the step sizes for the design variables for batch simulation and optimization:
```
# The step size for each design variable during optimization
FL_amplification_stepsize=60                      # The step size for the design parameter: force-length amplification, can be changed to any number
FL_shift_stepsize=0.2                             # The step size for the design parameter: force-length shift, can be changed to any number
strip_orientation_stepsize=5                      # The step size for the design parameter: strap orientation, can be changed to any number
bottom_location_stepsize=5                        # The step size for the design parameter: bottom endpoint location, can be changed to any number
```




***(1) Batch simulation for the DL, walk and run:*** <br/>

This part of codes will change the design parameters of the AFO in the model and run the model automatically, the processes are: (1) the code will change the design parameters in the AFO design.txt file in the AFO Design folders; (2) an AFO representation model will be created in the musculoskeletal model; (3) the code will run the simulation of drop landing, walking and running. The code use a loop to achieve these: <br/>

***(i) The change of design parameters in the AFO design.txt file in the AFO Design folder:***<br/>

```
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product(range(2,4), range(8,9), range(1,2), range(3,4)):        # Design parameter: force-length amplification (fl_am)
```
This code will determine the amplification parameters of the AFO materials (force-length relationship) for the four stripes. The amplification is defined as the scaling factors of the force generated by the AFO strape with the same extension, and is determined using the following equation:
```
# The amplification (scaling) of the force-length relationship
FL_amplification_1=fl_am_1*FL_amplification_stepsize
FL_amplification_2=fl_am_2*FL_amplification_stepsize
FL_amplification_3=fl_am_3*FL_amplification_stepsize
FL_amplification_4=fl_am_4*FL_amplification_stepsize
```
where the FL_amplification_stepsize can be defined using the first line of the following (can be changed during the optimization).
```
FL_amplification_stepsize=20                                     # The step size for the design parameter: force-length amplification, can be changed to any number
FL_shift_stepsize=0.2                                            # The step size for the design parameter: force-length shift, can be changed to any number
strip_orientation_stepsize=5                                     # The step size for the design parameter: strap orientation, can be changed to any number
bottom_location_stepsize=5                                       # The step size for the design parameter: bottom endpoint location, can be changed to any number
```
The amplification of the force-length relationship for the AFO materials can be then determined using the desigan varialbes (fl_am_) and the step size selected (FL_amplification_stepsize). e.g., in the current case, the amplification parameters of the four stripes are 40, 160, 20 and 60, respectively.

```
for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)): # Design parameter: force-length shift (fl_shift)
```
This code will determine the shift parameters of the AFO materials for the four stripes. The shift parameters can be determined using the following equation:
```
FL_shift_1=fl_shift_1*FL_shift_stepsize-0.2
FL_shift_2=fl_shift_2*FL_shift_stepsize-0.2
FL_shift_3=fl_shift_3*FL_shift_stepsize-0.2
FL_shift_4=fl_shift_4*FL_shift_stepsize-0.2
```
where the FL_shift_stepsize will be defined using the second line of the following equations (can be changed during optimization, depending on the step size selected):
```
FL_amplification_stepsize=20                                     # The step size for the design parameter: force-length amplification, can be changed to any number
FL_shift_stepsize=0.2                                            # The step size for the design parameter: force-length shift, can be changed to any number
strip_orientation_stepsize=5                                     # The step size for the design parameter: strap orientation, can be changed to any number
bottom_location_stepsize=5                                       # The step size for the design parameter: bottom endpoint location, can be changed to any number
```
E.g., in the current case, the shift parameters for the four stripes are 0 (1x0.2-0.2), -0.2 (0x0.2-0.2), 0.2 (2x0.2-0.2) and 0.2 (2x0.2-0.2), respectively. The shift parameters are defined as the translation of the force-length curve of the AFO materials, i.e, FL_shift_2=-0.2 means the force-length curve will move 0.2 unit to the left.

```
for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):     # Deisgn parameters of stripe orientation
```
This code will determine the orientations of the stripes of the AFO for the four stripes, which can be determined using the following equation:
```
Strip_orientation=np.array([strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4])*strip_orientation_stepsize
```
where the strip_orientation_stepsize can be defined using the third line of the following equations (can be changed during the optimization, dependening on the step size selected):
```
FL_amplification_stepsize=20                                     # The step size for the design parameter: force-length amplification, can be changed to any number
FL_shift_stepsize=0.2                                            # The step size for the design parameter: force-length shift, can be changed to any number
strip_orientation_stepsize=5                                     # The step size for the design parameter: strap orientation, can be changed to any number
bottom_location_stepsize=5                                       # The step size for the design parameter: bottom endpoint location, can be changed to any number
```

```
for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product(range(0,1), range(0,1), range (0,1), range(0,1)): # Design parameter: bottom endpoint location (bottom_location)
```
This code will determine the locations of the endpoints of the AFO representations at the bottom size (e.g. the location of the AFO representation relative to the leg segment). The locations can be determined using the following equation:
```
bottom_location_angle=np.array([bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4])*bottom_location_stepsize
```
where the bottom_location_stepsize can be defined using the fourth line of the following equations (can be changed based on the step sizes selected):
```
FL_amplification_stepsize=20                                     # The step size for the design parameter: force-length amplification, can be changed to any number
FL_shift_stepsize=0.2                                            # The step size for the design parameter: force-length shift, can be changed to any number
strip_orientation_stepsize=5                                     # The step size for the design parameter: strap orientation, can be changed to any number
bottom_location_stepsize=5                                       # The step size for the design parameter: bottom endpoint location, can be changed to any number
```
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

*Second parameter:* 'model': to demonstrate the musculoskeletal model with AFO <br/>
>>>>>> 'simulation': to run drop landing, walk and running simulations <br/>

*Third parameter:* the folder for storing the drop landing simulation results <br/>

After the batch of simulation, the simulation results will store in:<br/>
*Drop landing:* ./Drop landing/DL simulation results <br/>
*Gait simulation:* ./Gait simulation/Model outputs/5_ForwardDynamics_1st *and* ./Gait simulation/Model outputs/5_ForwardDynamics_1st
*Running simulation:* ./Running simulation/Model outputs/5_ForwardDynamics

***(2) Collection of the drop landing simulation results and put them into an excel file:*** <br/>

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
After running, the excel file will be stored in *./Drop landing/DL simulation results* <br/>

***(3) Collection of the walk simulation results and put them into an excel file:*** <br/>

This part of codes will collect the interested simulation results from the walk simulation, and put them into an excel file. <br/>
For walk, the interested simulation result parameters are: average differences of subtalar angles and ankle angles between models with and without AFO across the gait:
```
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']   # The specified parameter to extract
```
This code provides the information about what results will collect from the simulation results, i.e. the instant time, the subtalar angle and the ankle angle. <br/>

Similarly, the codes use a loop to collect the results from the batch simulation of each AFO design, therefore, the parameters of range in the loop syntax should be changed to correspond to the loop syntax in the AFO design parameters (e.g. section **3**/***(1)***/***(i)***)
```
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(2,3), range(8,9), range(1,2), range(3,4)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):
```
When running the code, a dialog box will appear, asking to select the batch simulation results folder. Select the model outputs folder, (e.g. **./Gait simulation/Modeloutputs**), the excel file will be stored in the selected folder (e.g. **./Gait simulation/Modeloutputs**).

***(4) Collection of the running simulation results and put them into an excel file:*** <br/>

This part of codes will collect the interested simulation results from the running simulation, and put them into an excel file. <br/>
For running, the interested simulation result parameters are: average differences of subtalar angles and ankle angles between models with and without AFO across the whole cycle:
```
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']   # The specified parameter to extract
```
This code provides the information about what results will collect from the simulation results, i.e. the instant time, the subtalar angle and the ankle angle. <br/>

Similarly, the codes use a loop to collect the results from the batch simulation of each AFO design, therefore, the parameters of range in the loop syntax should be changed to correspond to the loop syntax in the AFO design parameters (e.g. section **3**/***(1)***/***(i)***)
```
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(2,3), range(8,9), range(1,2), range(3,4)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):
```
When running the code, a dialog box will appear, asking to select the batch simulation results folder. Select the model outputs folder, (e.g. **./Running simulation/Modeloutputs**), the excel file will be stored in the selected folder (e.g. **./Running simulation/Modeloutputs**).

**Tips:** The four parts of codes are disabled, which can be enabled by remove the """ symbols before and after the codes. The four parts of codes can also be run one by one by removing the """ symbols before and after each part of the codes. 
