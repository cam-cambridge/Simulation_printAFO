#------------------------------------------------------------------------------------------------------------------------------------------
# The MBD simulation of drop landing for new AFO desig (cross design)
# DroplandingSimulation_AFO
def Simulation(SimulationType, ModelOperation, results_directory):
    import os
    import SetupFileGeneration
    import AFO1_DesignParameter
    import AFO2_MBDModel
    #---------------------------------------------------------------------------------------------------------------------------
    # Drop landing simulation if the drop landing related string is input
    if SimulationType=='AFODroplanding' or SimulationType=='AFOdroplanding' or SimulationType=='AFODROPLANDING' or SimulationType=='AFODrop landing':
        # The folder path of pthon script
        path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
        path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
        # The joining of the folders python simulation, drop landing and MBD model
        Model_AFO_droplanding=os.path.join(path_simulation, 'Drop landing', 'Fullbodymodel_droplanding_AFO.osim')
        # The AFO representation, AFO force magnitude, and platform inclination calculated from the design parameter file: AFO input.txt, using modue (AFO1_DesignParameter.AFODesignParameter)
        # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_length]
        # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
        [AFO_representation, AFO_material, Platform_inclination]=AFO1_DesignParameter.AFODesignParameter('AFO Design', 'AFO input.txt')
       # Generate the MBD drop landing model .osim file using module (AFO2_MBDModel.MBDmodel_Droplanding_AFO)
        AFO2_MBDModel.MBDmodel_Droplanding_AFO(Model_AFO_droplanding, Platform_inclination, AFO_representation, AFO_material)
        # Display the MBD drop landing model with AFO
        os.chdir(os.path.join(path_simulation, 'Drop landing'))
        if ModelOperation=='model' or ModelOperation=='Model' or ModelOperation=='MODEL':
            os.system('Fullbodymodel_droplanding_AFO.osim')
        elif ModelOperation=='simulation' or ModelOperation=='Simulation' or ModelOperation=='SIMULATION':
            ForwardDynamics_Droplanding(os.path.join(path_simulation, 'Drop landing'), 'Fullbodymodel_droplanding_AFO.osim', 'default_Setup_ForwardTool.xml', results_directory, 0.45)
    # Gait simulation if the gait related string is input
    else:
        path_script = os.path.realpath(__file__)                                                                                              # The full document path of the python scrip
        path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder for the python script: python simulation
        path_setupfiles=os.path.join(path_simulation, 'Gait simulation data\Setup files')                                            # The path of the simulation setup files
        SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation data', 'Model outputs'))
        os.chdir(path_setupfiles)                                                                                                                     # Set the current working directory: Gait simulation data/Setup files
        if SimulationType=='Scaling' or SimulationType=='scaling' or SimulationType=='model scaling' or SimulationType=='Model scaling':
            Scaling(path_simulation)
        elif SimulationType=='IK' or SimulationType=='inverse kinematics' or SimulationType=='Invese Kinematics' or SimulationType=='Inverse kinematics':
            Scaling(path_simulation)
            IK(path_simulation)
        elif SimulationType=='RRA' or SimulationType=='rra' or SimulationType=='Residual reduced algorithm':
            Scaling(path_simulation)
            IK(path_simulation)
            RRA(path_simulation)
        elif SimulationType=='CMC' or SimulationType=='cmc' or SimulationType=='Computed Muscle Control' or SimulationType=='computed muscle control':
            Scaling(path_simulation)
            IK(path_simulation)
            loop_num=RRA(path_simulation)
            CMC(path_simulation, loop_num)
        elif SimulationType=='FD' or SimulationType=='Forward dynamics' or SimulationType=='Walk' or SimulationType=='walk' or SimulationType=='WALK' or SimulationType=='Gait' or SimulationType=='gati':
            Scaling(path_simulation)
            IK(path_simulation)
            loop_num=RRA(path_simulation)
            CMC(path_simulation, loop_num)
            FD(path_simulation)
        elif SimulationType=='Gait_AFO' or SimulationType=='gait_AFO' or SimulationType=='GAIT_AFO':
            Model_AFO_origin=os.path.join(path_simulation, 'Gait simulation data/Model outputs//3_RRA', 'Fullbodymodel_Walk_RRA_modification_final.osim')
            Model_AFO_final=os.path.join(path_simulation, 'Gait simulation data/Model outputs//3_RRA', 'Fullbodymodel_Walk_RRA_modification_AFO.osim')
            # AFO_representation, AFO_material, Platform_inclination=AFO1_DesignParameter.AFODesignParameter('AFO Design', 'AFO input1.txt')
            [AFO_representation, AFO_material, Platform_inclination]=AFO1_DesignParameter.AFODesignParameter('AFO Design', 'AFO input.txt')
            # Generate the MBD drop landing model .osim file using module (AFO2_MBDModel.MBDmodel_Droplanding_AFO)
            AFO2_MBDModel.AFO_MBDfile(Model_AFO_origin, Model_AFO_final, AFO_representation, AFO_material)            
             #AFO2_MBDModel.MBDmodel_Droplanding_AFO(Model_AFO_droplanding, Platform_inclination, AFO_representation, AFO_material)

            os.chdir(os.path.join(path_simulation, 'Gait simulation data/Model outputs/3_RRA'))
            os.system('Fullbodymodel_Walk_RRA_modification_AFO.osim')




            #FD_AFO(path_simulation)
        else:
            print('Input error: invalid input, please try again! Try "Scaling", "IK", "RRA", "CMC", "FD", or "Walk" or "Gait_AFO".')

def Scaling(path_simulation):
    import os
    import SetupFileGeneration
    #---------------------------------------------------------------------------------
    # Model scalling
    scale_setup='1_Walk_Scale_Setup.xml'                                                                                                                     # Setup file for the model scaling
    SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation data', 'Model outputs', '1_Scale'))                # Create new folder for the results of model scaling
    cmd="opensim-cmd run-tool %s" %(scale_setup)                                                                                                     # Command line execution
    os.system(cmd)                                                                                                                                                           # Run model scalling using command line

def IK(path_simulation):
    import os
    import SetupFileGeneration
    #---------------------------------------------------------------------------------
    # IK (inverse kinematics)
    IK_setup='2_Walk_IK_Setup.xml'                                                                                                                            # Setup file for the IK (Inverse Kinematics)
    SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation data', 'Model outputs', '2_IK'))                   # Create new folder for the results of IK
    cmd="opensim-cmd run-tool %s" %(IK_setup)
    os.system(cmd)                                                                                                                                                          # Run IK using command line

def RRA(path_simulation):
    import os
    import RRA_evaluation
    import opensim as open
    import RRAModelMassModification
    import SetupFileGeneration
    #---------------------------------------------------------------------------------
    #RRA (Residual Reduction Algorithm)
    loop_num=1                                                                                                                                                                    # The number of the times of the RRA analysis
    Residual=pErr=[100, 100, 100, 100]                                                                                                                              # The initial values set for the residual results, including Max and RMS residual force, residual moment, transportational and angular position error
    while Residual[0]>10 or Residual[1]>5 or Residual[2]>20 or Residual[3]>20 or pErr[0]>2 or pErr[1]>2 or pErr[2]>2 or pErr[3]>2:             # The criterion for the RRA analysis loop
        os.chdir(os.path.join(path_simulation, 'Gait simulation data\Setup files'))                                                                                                                                            # Set the current working directory: Gait simulation data/Setup files, this is required in the second RRA loop because it will change during the loop
        if loop_num==1:
            RRA_setup='3_Walk_rra_setup_rra1.xml'
        else:
            SetupFileGeneration.rra_setup(loop_num)                                                                                                              # From the second loop of RRA, a new setup file will be generated based on the RRA results
            RRA_setup='Walk_rra_setup_rra%d.xml' %(loop_num)
        SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation data', 'Model outputs', '3_RRA'))                   # Create new folder for the results of RRA
        cmd="opensim-cmd run-tool %s" %(RRA_setup)
        os.system(cmd)                                                                                                                                                            # Simulation of RRA using command line
        RRA_massoutput='out.log'                                                                                                                                          # Read the RRA output log and get the recommended total mass change from RRA
        Totalmasschange=RRAModelMassModification.getRRAmassoutput(RRA_massoutput)                                        # Read the total mass change according to RRA from the out log
        path_RRAOutput=os.path.join(path_simulation,'Gait simulation data', 'Model outputs','3_RRA')
        os.chdir(path_RRAOutput)                                                                                                                                          # Set the current working directory: Model outputs/3_RRA
        osimModel=open.Model("Fullbodymodel_Walk_RRA%d.osim" %(loop_num))                                                      # Assign model to osimModel
        osimModel_rrachanges=RRAModelMassModification.setBodyMassUsingRRAMassChange(osimModel,Totalmasschange)            # Adjust the mass of the body segment according to the RRA recommendation
        osimModel_rrachanges.printToXML("Fullbodymodel_Walk_RRA%d_modification.osim" %(loop_num))                                        # Save the adjusted model to osimModel_rrachanges
        [Residual, pErr]=RRA_evaluation.rra_evaluation(path=os.path.join(path_simulation, 'Gait simulation data\Model outputs\\3_RRA'), RRA_directory='Results_rra_%d' %(loop_num),               # RRA evaluation
                                                                                        RRA_Residuals='rra_walk_%d_avgResiduals.txt' %(loop_num),
                                                                                        RRA_pErr_file='rra_walk_%d_pErr.sto' %(loop_num))
        loop_num=loop_num+1
        if loop_num>10:
            print('The RRA evaluation criterion is not achieved')
            break
    osimModel_rrachanges.printToXML('Fullbodymodel_Walk_RRA_modification_final.osim')
    return loop_num

def CMC(path_simulation, loop_num):
    import os
    import SetupFileGeneration
    #--------------------------------------------------------------------------------
    #CMC (Computed Muscle Control)
    os.chdir(os.path.join(path_simulation, 'Gait simulation data\Setup files'))
    SetupFileGeneration.cmc_setup(loop_num-1)                                                                                                      # Generate new setup file for the CMC, which will include the model and results from the last RRA simulation
    CMC_setup='Walk_cmc_setup.xml'
    cmd="opensim-cmd run-tool %s" %(CMC_setup)
    os.system(cmd)

def FD(path_simulation):
    import os
    #--------------------------------------------------------------------------------
    #Forward Dynamics (FD)
    os.chdir(os.path.join(path_simulation, 'Gait simulation data\Setup files'))
    # SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation data', 'Model outputs', '5_ForwardDynamics'))                   # Create new folder for the results of IK
    FD_setup='5_Walk_Forward_setup.xml'
    cmd="opensim-cmd run-tool %s" %(FD_setup)
    os.system(cmd)

def FD_AFO(path_simulation):
    import os
    #--------------------------------------------------------------------------------
    #Forward Dynamics (FD)
    os.chdir(os.path.join(path_simulation, 'Gait simulation data\Setup files'))
    # SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation data', 'Model outputs', '5_ForwardDynamics'))                   # Create new folder for the results of IK
    FD_setup='5_Walk_Forward_setup_AFO.xml'
    cmd="opensim-cmd run-tool %s" %(FD_setup)
    os.system(cmd)

#------------------------------------------------------------------------------------------------------------------------------------------
# Generate the set up file for the drop landing forward dynamics simulations, and run the FD simulation using the set up file
def ForwardDynamics_Droplanding(path, file_MBD, SetFile_forward, results_directory, run_finaltime):
    import numpy as np
    import os
    # Set the current working directory
    os.chdir(path)
    OsModel_full=os.path.join(path, file_MBD)

    # To generate forward setup file (.xml), first check, if no, to create one
    if not os.path.isdir(results_directory):
        os.makedirs(results_directory)
    if not os.path.exists(SetFile_forward):
        os.system("opensim-cmd print-xml forward")

    # To revise the default forward setup file (.xml)
    with open (SetFile_forward,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open (SetFile_forward,"w",encoding="utf-8") as f_w:
        for line in lines:
            if line.strip().startswith('<model_file'):
                f_w.writelines(['		<model_file>',OsModel_full,'</model_file>',"\n"])
            elif line.strip().startswith('<results_directory>'):
                f_w.writelines(['		<results_directory>./',results_directory,'</results_directory>',"\n"])
            elif line.strip().startswith('<final_time>'):
                f_w.writelines(["		<final_time>",str(run_finaltime),"</final_time>","\n"])
            elif line.strip().startswith('<solve_for_equilibrium_for_auxiliary_states>'):
                f_w.writelines(['		<solve_for_equilibrium_for_auxiliary_states>true</solve_for_equilibrium_for_auxiliary_states>',"\n"])
            else:
                f_w.write(line)
    # To run the simulation
    cmd="opensim-cmd -L \"C:\OpenSim 4.1\\bin\osimExampleComponents.dll\"  run-tool %s" %(SetFile_forward)
    os.system(cmd)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Old previouse scripts
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#---------------------------------------------------------------------------------------------------------------------------------------------------
def DroplandingSimulation(str):
    import os
    import AFO2_MBDModel
    if str=='Droplanding' or str=='droplanding' or str=='DROPLANDING' or str=='Drop landing':
        path_script = os.path.realpath(__file__)                                                                                              # The full document path of the python scrip
        path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder for the python script: python simulation
        Model_AFO_droplanding_origin=os.path.join(path_simulation, 'Gait simulation data/Model outputs//3_RRA', 'Fullbodymodel_Walk_RRA_modification_AFO.osim')
        Model_AFO_droplanding_final=os.path.join(path_simulation, 'Drop landing', 'Fullbodymodel_Droplanding_AFO.osim')
        AFO2_MBDModel.MBDfile_Droplanding(Model_AFO_droplanding_origin, Model_AFO_droplanding_final, Platform_inclination=[30,0,0])
        os.chdir(os.path.join(path_simulation, 'Drop landing'))
        os.system('Fullbodymodel_Droplanding_AFO.osim')
    else:
        print('Input error: invalid input, please try again! Try "Droplanding".')

def GaitSimulation (str):
    import os
    import SetupFileGeneration
    import AFO1_DesignParameter
    import AFO2_MBDModel
    #---------------------------------------------------------------------------------
    # Get the document path of the simulation
    path_script = os.path.realpath(__file__)                                                                                              # The full document path of the python scrip
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder for the python script: python simulation
    path_setupfiles=os.path.join(path_simulation, 'Gait simulation data\Setup files')                                            # The path of the simulation setup files
    SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation data', 'Model outputs'))
    os.chdir(path_setupfiles)                                                                                                                     # Set the current working directory: Gait simulation data/Setup files
    if str=='Scaling' or str=='scaling' or str=='model scaling' or str=='Model scaling':
        Scaling(path_simulation)
    elif str=='IK' or str=='inverse kinematics' or str=='Invese Kinematics' or str=='Inverse kinematics':
        Scaling(path_simulation)
        IK(path_simulation)
    elif str=='RRA' or str=='rra' or str=='Residual reduced algorithm':
        Scaling(path_simulation)
        IK(path_simulation)
        RRA(path_simulation)
    elif str=='CMC' or str=='cmc' or str=='Computed Muscle Control' or str=='computed muscle control':
        Scaling(path_simulation)
        IK(path_simulation)
        loop_num=RRA(path_simulation)
        CMC(path_simulation, loop_num)
    elif str=='FD' or str=='Forward dynamics' or str=='Walk' or str=='walk' or str=='WALK':
        Scaling(path_simulation)
        IK(path_simulation)
        loop_num=RRA(path_simulation)
        CMC(path_simulation, loop_num)
        FD(path_simulation)
    elif str=='Gait_AFO' or str=='gait_AFO' or str=='GAIT_AFO':
        Model_AFO_origin=os.path.join(path_simulation, 'Gait simulation data/Model outputs//3_RRA', 'Fullbodymodel_Walk_RRA_modification_final.osim')
        Model_AFO_final=os.path.join(path_simulation, 'Gait simulation data/Model outputs//3_RRA', 'Fullbodymodel_Walk_RRA_modification_AFO.osim')
        AFO_representation, AFO_material, Platform_inclination=AFO1_DesignParameter.AFODesignParameter('AFO Design', 'AFO input1.txt')
        AFO2_MBDModel.AFO_MBDfile(Model_AFO_origin, Model_AFO_final, AFO_representation, AFO_material)
        os.chdir(os.path.join(path_simulation, 'Gait simulation data/Model outputs/3_RRA'))
        os.system('Fullbodymodel_Walk_RRA_modification_AFO.osim')
        #FD_AFO(path_simulation)
    else:
        print('Input error: invalid input, please try again! Try "Scaling", "IK", "RRA", "CMC", "FD", or "Walk" or "Gait_AFO".')
