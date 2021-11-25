# Simulation_printAFO
This repository mainly includes the python codes, OpenSim musculoskeletal models and associated files for the musculoskeletal simulation of the 3D printed AFO.

## **1. Python installation** <br/>
(1) It should be noted that starting with 4.0, OpenSim is distributed as 64-bit only, so you must use 64-bit Python. If you are using 4.0, you need Python 2.7.x. If you are using 4.1 or 4.2, you need Python 3.7.x. <br/>
(2) After installing the python 3.7.x, install modules "numpy","pandas", "mpl_toolkits", "xlwt", "xlrd", xlutils", "openpyxl".

## **2. Architecture of the files and folders** <br/>
![image](https://user-images.githubusercontent.com/14294455/143143898-af1cb7da-dccf-4e96-b800-2dfbe2634f57.png)

The batch simulation pipeline is stricted to the architecture of the files and foler, as shown in the figure above: <br/>
***Simulation_printeAFO:*** the folder for all the simulation pipeline files. The folder include AFO Design folder, Drop landing folder, Gait simulation folder, Running simulation folder, Batch simulation code folder. <br/>
***AFO Design:*** the design parameters for the AFO in .txt format. It includes two files: AFO input_default: the original design parameters; AFO input: the desgin paraeters for the AFO models in the musculoskeletal models. The AFO Design folder can be downloaded directly from the repo. <br/>
***Drop landing:*** the drop landing model and associated files. The Drop landing folder can be downloaded directly from the repo. <br/>
***Gait simulation:*** the musculoskeletal models and files required for the gait simulation. Due to the large size of the files, the files were separated into two folders, one is "Gait Simulation.rar", which should be decompressed after downloaded, the second one is "4_CMC.rar", which should be decrompressed and then putted into the "Gait simulation" folder. <br/>
***Running simulation:*** the musculoskeletal models (same with the model for gait simulation) and files required for the running simulation. It should be decompressed after downloaded. <br/>
***Batch simulation code:*** the code for the batch simulation. Apart from the above folders, all the codes should be downloaded and put in the "Batch simulation code" folder.

## **3. Batch simulation code** <br/>
The batch simulation code will change the design parameters, develop the AFO representation in the model and run the simulations automatically. It includes simulations of drop landing, walk and running, collection of drop landing simulation results (maximum subtalar angle and ankle angle), and collection of simulation results of gait and running (differences of subtalar angle and ankle angle for models with and without AFO):<br/>
***(1) Batch simulation for the DL, walk and run:*** <br/>
This part of codes will change the design parameters of the AFO in the model and run the model automatically, the processes are: (1) the code will change the design parameters in the AFO design.txt file in the AFO Design folders; (2) a representation model of AFO will be created in the musculoskeletal model; (3) the code will run the simulation of drop landing, walking and running. The code use a loop to achieve these: <br/>

***(i) The change of design parameters in the AFO design.txt file in the AFO Design folder:***<br/>
```
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(2,3), range(8,9), range(1,2), range(3,4)):  # Design parameters of force-length amplification
```
This code will determine the amplification parameters of the AFO materials (force-length relationship) for the four stripes. The amplification is defined as the scaling factors of the force generated by the AFO strape with the same extension, and is determined using the following equation:
```
FL_amplification_1=af_am_1*20
FL_amplification_2=af_am_2*20
FL_amplification_3=af_am_3*20
FL_amplification_4=af_am_4*20
```
where the number 20 can change to any number, depending on the sizes of the step seleted, i.e. in this case, the amplification parameters of the four stripes are 40, 160, 20 and 60, respectively. The ranges of the amplification parameters for the four stripes can be changed during the batch simulation.

```
  for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):  # Design parameters of force-length shift
```
This code will determine the shift parameters of the AFO materials for the four stripes. The shift parameters can be determined using the following equation:
```
FL_shift_1=af_shift_1*0.2-0.2
FL_shift_2=af_shift_2*0.2-0.2
FL_shift_3=af_shift_3*0.2-0.2
FL_shift_4=af_shift_4*0.2-0.2
```
where the equation can be changed, depending the range of the shift parameters and the sizes of the step. I.e. in this case, the shift parameters for the four stripes are 0 (1x0.2-0.2), -0.2 (0x0.2-0.2), 0.2 (2x0.2-0.2) and 0.2 (2x0.2-0.2), respectively. The shift parameters are defined as the translation of the force-length curve of the AFO materials, i.e, FL_shift_2=-0.2 means the force-length curve will move 0.2 unit to the left.

```
for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):# Deisgn parameters of stripe orientation
```
This code will determine the orientation of the stripes of the AFO directly, i.e. strip_ori_1=5 means the orientation of the first stripe is 5 degree.<br/>

The definations of the design parameters in the AFO can be found in the Guidelines in the repo.<br/>

***(ii) The development of AFO in the musculoskeletal model and run the simulation:***<br/>
After the design parameters in the AFO design'txt file were changed, the main code will call the module "AFO0_Simulation" module to create AFO representation in the musculoskeletal model and run the simulation: <br/>
```
AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory_DL)
```
This code will call the module "AFO0_Simulation" module to demonstrate the musculoskeletal model with AFO representation and run the simulation of activities. There are three parameters in the module: <br/>
*First parameter:* to determine the simulated activities <br/>
>>>>>>'AFODroplanding': to demonstrate and run drop landing model with AFO <br/>
>>>>>>'Walk_AFO' or 'Run_AFO': to demonstrate and run walk or running model with AFO <br/>
*Second parameter:* use 'model' to demonstrate the musculoskeletal model with AFO <br/>
>>>>>> use 'simulation' to run drop landing, walk and running simulations <br/>
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

***(3) Collection of the walk and running simulation results and put them into an excel file:*** <br/>
This part of codes will collect the interested simulation results from the walk and running, and put them into an excel file. <br/>
For walk and running, the interested simulation result parameters are: average differences of subtalar angles and ankle angles between models with and without AFO across the gait:
```
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']   # The specified parameter to extract
```
This code provide the information about what results will collect from the simulation results, i.e. the instant time, the subtalar angle and the ankle angle. <br/>

Similarly, the codes use a loop to collect the results from the simulation result of each AFO design, therefore, the parameters of range in the loop syntax should be changed to correspond to the loop syntax in the AFO design parameters (e.g. section **3**/***(1)***/***(i)***)
```
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(2,3), range(8,9), range(1,2), range(3,4)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):
```




