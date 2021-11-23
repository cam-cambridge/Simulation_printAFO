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




