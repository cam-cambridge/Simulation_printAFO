#------------------------------------------------------------------------------------------------------------------------------------------
# The MBD simulation of drop landing for new AFO desig (cross design)
# DroplandingSimulation_AFO
#def Simulation(SimulationType, ModelOperation, DesignVariables, results_directory):
def Simulation(Parallel_simu_paralist):
    import os
    import numpy as np
    import SetupFileGeneration
    import AFO1_DesignParameter
    import AFO2_MBDModel
    # Parameter list for parallel simulation
    SimulationType=Parallel_simu_paralist[0]
    ModelOperation=Parallel_simu_paralist[1]
    DesignVariables=Parallel_simu_paralist[2]
    results_directory=Parallel_simu_paralist[3]
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Drop landing simulation if the drop landing related string is input
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if SimulationType=='AFODroplanding' or SimulationType=='AFOdroplanding' or SimulationType=='AFODROPLANDING' or SimulationType=='AFODrop landing':
        # For the drop landing activity, the Parallel_simu_paralist has 5 parameters, the 5th parameter is the plaform inclination
        Platform_inclination=Parallel_simu_paralist[4]
        results_directory_platform=results_directory+str(Platform_inclination[0])+str(Platform_inclination[1])+str(Platform_inclination[2])
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # The input parameters for the model development, including the folders and models
        foldername_droplanding='Simulation models\Drop landing'+str(results_directory)                         # The folders for drop landing model and simulation
        if Platform_inclination==[0, -45, -25]:
            msmodel_droplanding='Fullbodymodel_DL_platform45_AFO.osim'                                                   # The model for drop landing simulation
        else:
            msmodel_droplanding='Fullbodymodel_DL_platform0_AFO.osim'
        #folder_designparameters='AFO Design'                                                                                           # The folder include the design parameter .txt file
        #txtfile_designparameters='AFO input.txt'                                                                                         # The txt file includes the design parameters
        droplanding_forward_setup_file='default_Setup_ForwardTool.xml'                                               # The setup file for the drop landing forward dynamics
        # The Global coordinates for right tibial and calcn for drop landing model
        tibial_center = np.array([-0.07520, -0.46192, 0.0835])                                                                    # tibial center coordinates in drop landing MBD model (position 0) in global coordinate system
        calcn_center = np.array([-0.12397, -0.93387, 0.09142])                                                                  # calcn center coordinates in drop landing MBD model (position 0) in global coordinate system
        talus_center=[-0.0752, -0.8919, 0.0835]
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # The folder path of pthon script
        path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
        path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
        # The joining of the folders python simulation, drop landing and MBD model
        Model_AFO_droplanding=os.path.join(path_simulation, foldername_droplanding, msmodel_droplanding)
        # The AFO representation, AFO force magnitude, and platform inclination calculated from the design parameter file: AFO input.txt, using modue (AFO1_DesignParameter.AFODesignParameter)
        # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_length]
        # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
        [AFO_representation, AFO_material]=AFO1_DesignParameter.AFODesignParameter(DesignVariables, tibial_center, calcn_center, talus_center)
       # Generate the MBD drop landing model .osim file using module (AFO2_MBDModel.MBDmodel_Droplanding_AFO)
        AFO2_MBDModel.MBDmodel_Droplanding_AFO(Model_AFO_droplanding, Platform_inclination, AFO_representation, AFO_material, DesignVariables)
        # Display the MBD drop landing model with AFO
        os.chdir(os.path.join(path_simulation, foldername_droplanding))
        if ModelOperation=='model' or ModelOperation=='Model' or ModelOperation=='MODEL':
            os.system(msmodel_droplanding)
        elif ModelOperation=='simulation' or ModelOperation=='Simulation' or ModelOperation=='SIMULATION':
            ForwardDynamics_Droplanding(os.path.join(path_simulation, foldername_droplanding), msmodel_droplanding, droplanding_forward_setup_file, results_directory_platform, 0.25)
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Gait simulation if the gait related string is input
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif SimulationType=='Scaling_walk' or SimulationType=='scaling_walk' or SimulationType=='IK_walk' or SimulationType=='RRA_walk' or SimulationType=='rra_walk' or \
           SimulationType=='CMC_walk' or SimulationType=='cmc_walk' or SimulationType=='FD_walk' or SimulationType=='Forward dynamics_walk' or\
           SimulationType=='walk' or SimulationType=='Walk' or SimulationType=='Gait' or SimulationType=='gait' or SimulationType=='Walk_withoutAFO' or SimulationType=='walk_withoutAFO' or\
           SimulationType=='Gait_AFO' or SimulationType=='gait_AFO' or SimulationType=='Walk_AFO' or SimulationType=='walk_AFO':
           # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
           # The some input parameters for the model development, including the folders and models
           foldername_gait='Simulation models\Gait simulation'+str(results_directory)
           gait_setup_file_foldername=os.path.join(foldername_gait, 'Setup files')
           gait_model_output=os.path.join(foldername_gait, 'Model outputs')
           # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
           path_script = os.path.realpath(__file__)                                                                                              # The full document path of the python scrip
           path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder for the python script: python simulation
           path_setupfiles=os.path.join(path_simulation, gait_setup_file_foldername)                                      # The path of the simulation setup files
           SetupFileGeneration.dircreation(os.path.join(path_simulation, gait_model_output))
           os.chdir(path_setupfiles)                                                                                                                     # Set the current working directory: Gait simulation/Setup files
           if SimulationType=='Scaling_walk' or SimulationType=='scaling_walk' :
               Scaling(path_simulation, 'walk')
           elif SimulationType=='IK_walk' :
                #Scaling(path_simulation, 'walk')
                IK(path_simulation, 'walk')
           elif SimulationType=='RRA_walk' or SimulationType=='rra_walk' :
                #Scaling(path_simulation, 'walk')
                #IK(path_simulation, 'walk')
                RRA(path_simulation, 'walk')
                # The height_origin and height_scaled should be changed case by case
                MuscleScaling(path_simulation, 'walk', "Fullbodymodel_Walk_RRA_modification_final.osim", "Fullbodymodel_Walk_RRA_modification_final.osim", 1.70, 1.83, 15)
           elif SimulationType=='CMC_walk' or SimulationType=='cmc_walk':
                Scaling(path_simulation, 'walk')
                IK(path_simulation, 'walk')
                RRA(path_simulation, 'walk')
                # The height_origin and height_scaled should be changed case by case
                MuscleScaling(path_simulation, 'walk', "Fullbodymodel_Walk_RRA_modification_final.osim", "Fullbodymodel_Walk_RRA_modification_final.osim", 1.70, 1.83, 15)
                CMC(path_simulation, 'walk', 'SimulationOutput_Walk_0000000000000000')
           elif SimulationType=='FD_walk' or SimulationType=='Forward dynamics_walk' or SimulationType=='Walk' or SimulationType=='walk' or SimulationType=='Gait' or SimulationType=='gait':
                Scaling(path_simulation, 'walk')
                IK(path_simulation, 'walk')
                RRA(path_simulation, 'walk')
                # The height_origin and height_scaled should be changed case by case
                MuscleScaling(path_simulation, 'walk', "Fullbodymodel_Walk_RRA_modification_final.osim", "Fullbodymodel_Walk_RRA_modification_final.osim", 1.70, 1.83, 15)
                CMC(path_simulation, 'walk', '')
                FD(path_simulation, 'walk', '')
           elif SimulationType=='Gait_AFO' or SimulationType=='gait_AFO' or SimulationType=='Walk_AFO' or SimulationType=='walk_AFO' or SimulationType=='Walk_withoutAFO' or SimulationType=='walk_withoutAFO':
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # The some input parameters for the model development, including the folders and models
                foldername_gait='Simulation models\Gait simulation'+str(results_directory)
                gait_setup_file_foldername=os.path.join(foldername_gait, 'Setup files')
                gait_model_output=os.path.join(foldername_gait, 'Model outputs')
                model_AFO_origin_folder='3_RRA'
                model_AFO_origin_file='Fullbodymodel_Walk_RRA_adjusted.osim'
                model_AFO_final_file='Fullbodymodel_Walk_RRA_final_AFO.osim'
                # The Global coordinates for the right tibial, calcn and talus centers
                tibial_r_center=[-0.06850, 0.474615, 0.09158]
                calcn_r_center=[-0.13574, -0.05465, 0.10344]
                talus_r_center=[-0.07999, 0.015015, 0.091579]
                # The Global coordinates for the left tibial, calcn and talus centers
                tibial_l_center=[-0.06850, 0.474615, -0.09158]
                calcn_l_center=[-0.13574, -0.054654, -0.10344]
                talus_l_center=[-0.07999, 0.015015, -0.091579]
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                Model_AFO_origin=os.path.join(path_simulation, gait_model_output, model_AFO_origin_folder, model_AFO_origin_file)
                Model_AFO_final=os.path.join(path_simulation, gait_model_output, model_AFO_origin_folder, model_AFO_final_file)
                [AFO_representation, AFO_material]=AFO1_DesignParameter.AFODesignParameter(DesignVariables, tibial_r_center, calcn_r_center, talus_r_center)
                # Generate the MBD gait model .osim file using module (AFO2_MBDModel.MBDmodel_gait_AFO)
                AFO2_MBDModel.MBDmodel_Gait_AFO (Model_AFO_origin, Model_AFO_final, AFO_representation, AFO_material, DesignVariables)
                #AFO2_MBDModel.MBDmodel_Droplanding_AFO(Model_AFO_droplanding, AFO_representation, AFO_material)
                os.chdir(os.path.join(path_simulation, gait_model_output, model_AFO_origin_folder))
                if SimulationType=='Gait_AFO' or SimulationType=='gait_AFO' or SimulationType=='Walk_AFO' or SimulationType=='walk_AFO':
                    if ModelOperation=='model' or ModelOperation=='Model' or ModelOperation=='MODEL':
                        os.system(model_AFO_final_file)
                    elif ModelOperation=='simulation' or ModelOperation=='Simulation' or ModelOperation=='SIMULATION':
                        CMC(path_simulation, 'walk_AFO', results_directory)
                        #FD(path_simulation, 'walk_1stpart_AFO', results_directory)                                                                      # Previous code using kinematics as objective function
                        #FD(path_simulation, 'walk_2ndpart_AFO', results_directory)
                elif SimulationType=='Walk_withoutAFO' or SimulationType=='walk_withoutAFO':
                    if ModelOperation=='model' or ModelOperation=='Model' or ModelOperation=='MODEL':
                        os.system(model_AFO_origin_file)
                    elif ModelOperation=='simulation' or ModelOperation=='Simulation' or ModelOperation=='SIMULATION':
                        CMC(path_simulation, 'walk', 'SimulationOutput_Walk_0000000000000000')
                        #FD(path_simulation, 'walk_1stpart_withoutAFO', 'SimulationOutput_Walk_0000000000000000')          # Previous code using kinematics as objective function
                        #FD(path_simulation, 'walk_2ndpart_withoutAFO', 'SimulationOutput_Walk_0000000000000000')
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Running simulation if the gait related string is input
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    else:
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # The some input parameters for the model development, including the folders and models
        foldername_run='Simulation models\Running simulation'+str(results_directory)
        run_setup_file_foldername=os.path.join(foldername_run, 'Setup files')
        run_model_output=os.path.join(foldername_run, 'Model outputs')
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        path_script = os.path.realpath(__file__)                                                                                              # The full document path of the python scrip
        path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder for the python script: python simulation
        path_setupfiles=os.path.join(path_simulation, run_setup_file_foldername)                                      # The path of the simulation setup files
        SetupFileGeneration.dircreation(os.path.join(path_simulation, run_model_output))                        # Create the Model outputs folder, if the folder doesn't exit, then create it
        os.chdir(path_setupfiles)                                                                                                                     # Set the current working directory: Running simulation/Setup files
        if SimulationType=='Scaling_run' or SimulationType=='scaling_run' :
            Scaling(path_simulation, 'run')
        elif SimulationType=='IK_run':
            # Scaling(path_simulation, 'run')
            IK(path_simulation, 'run')
        elif SimulationType=='RRA_run' or SimulationType=='rra_run':
            # Scaling(path_simulation, 'run')
            # IK(path_simulation, 'run')
            RRA(path_simulation, 'run')
            MuscleScaling (path_simulation, 'run', "Fullbodymodel_Run_RRA_modification_final.osim", "Fullbodymodel_Run_RRA_modification_final.osim", 1.70, 1.78, 15)
        elif SimulationType=='CMC_run' or SimulationType=='cmc_run':
            Scaling(path_simulation, 'run')
            IK(path_simulation, 'run')
            RRA(path_simulation, 'run')
            MuscleScaling (path_simulation, 'run', "Fullbodymodel_Run_RRA_modification_final.osim", "Fullbodymodel_Run_RRA_modification_final.osim", 1.70, 1.78, 15)
            CMC(path_simulation, 'run', 'SimulationOutput_Run_0000000000000000')
        elif SimulationType=='FD_run' or SimulationType=='FD_RUN' or SimulationType=='Run' or SimulationType=='run':
            Scaling(path_simulation, 'run')
            IK(path_simulation, 'run')
            RRA(path_simulation, 'run')
            MuscleScaling (path_simulation, 'run', "Fullbodymodel_Run_RRA_modification_final.osim", "Fullbodymodel_Run_RRA_modification_final.osim", 1.70, 1.78, 15)
            CMC(path_simulation, 'run', '')
            FD(path_simulation, 'run_withoutAFO', 'SimulationOutput_Run_0000000000000000')
        elif SimulationType=='Run_AFO' or SimulationType=='run_AFO' or SimulationType=='Run_withoutAFO' or SimulationType=='run_withoutAFO':
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # The some input parameters for the model development, including the folders and models
            foldername_run='Simulation models\Running simulation'+str(results_directory)
            run_setup_file_foldername=os.path.join(foldername_run, 'Setup files')
            run_model_output=os.path.join(foldername_run, 'Model outputs')
            model_AFO_origin_folder='3_RRA'
            model_AFO_origin_file='Fullbodymodel_Run_RRA_adjusted.osim'
            model_AFO_final_file='Fullbodymodel_Run_RRA_final_AFO.osim'
            # The Global coordinates for the right tibial, calcn and talus centers
            tibial_r_center=[-0.05590, 0.41140, 0.08558]
            calcn_r_center=[-0.12120, -0.06647, 0.09444]
            talus_r_center=[-0.06667, -0.019561, 0.08558]
            # The Global coordinates for the left tibial, calcn and talus centers
            tibial_l_center=[-0.05590, 0.41140, -0.08558]
            calcn_l_center=[-0.12120, -0.06647, -0.09444]
            talus_l_center=[-0.06667, -0.019561, -0.08558]
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Model_AFO_origin=os.path.join(path_simulation, run_model_output, model_AFO_origin_folder, model_AFO_origin_file)
            Model_AFO_final=os.path.join(path_simulation, run_model_output, model_AFO_origin_folder, model_AFO_final_file)
            [AFO_representation, AFO_material]=AFO1_DesignParameter.AFODesignParameter(DesignVariables, tibial_r_center, calcn_r_center, talus_r_center)
            # Generate the MBD gait model .osim file using module (AFO2_MBDModel.MBDmodel_gait_AFO)
            AFO2_MBDModel.MBDmodel_Gait_AFO (Model_AFO_origin, Model_AFO_final, AFO_representation, AFO_material, DesignVariables)
            #AFO2_MBDModel.MBDmodel_Droplanding_AFO(Model_AFO_droplanding, AFO_representation, AFO_material)
            os.chdir(os.path.join(path_simulation, run_model_output, model_AFO_origin_folder))
            if SimulationType=='Run_AFO' or SimulationType=='run_AFO':
                if ModelOperation=='model' or ModelOperation=='Model' or ModelOperation=='MODEL':
                    os.system(model_AFO_final_file)
                elif ModelOperation=='simulation' or ModelOperation=='Simulation' or ModelOperation=='SIMULATION':
                    CMC(path_simulation, 'run_AFO', results_directory)
            elif SimulationType=='Run_withoutAFO' or SimulationType=='run_withoutAFO':
                if ModelOperation=='model' or ModelOperation=='Model' or ModelOperation=='MODEL':
                    os.system(model_AFO_origin_file)
                elif ModelOperation=='simulation' or ModelOperation=='Simulation' or ModelOperation=='SIMULATION':
                    CMC(path_simulation, 'run', 'SimulationOutput_Run_0000000000000000')
        else:
            print('Input error: invalid input, please try again! Try "Scaling", "IK", "RRA", "CMC", "FD", or "Walk" or "Gait_AFO".')
    #
def Scaling(path_simulation, SimulationType):
    import os
    import SetupFileGeneration
    #---------------------------------------------------------------------------------
    # Model scalling
    if SimulationType=='walk':
        scale_setup='1_Walk_Scale_Setup.xml'                                                                                                                     # Setup file for the model scaling
        SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '1_Scale'))         # Create new folder for the results of model scaling
        cmd="opensim-cmd run-tool %s" %(scale_setup)                                                                                                     # Command line execution
        os.system(cmd)                                                                                                                                                           # Run model scalling using command line
    elif SimulationType=='run':
        scale_setup='1_Run_Scale_Setup.xml'                                                                                                                     # Setup file for the model scaling
        SetupFileGeneration.dircreation(os.path.join(path_simulation,'Running simulation', 'Model outputs', '1_Scale'))   # Create new folder for the results of model scaling
        cmd="opensim-cmd run-tool %s" %(scale_setup)                                                                                                     # Command line execution
        os.system(cmd)                                                                                                                                                           # Run model scalling using command line
    #
def IK(path_simulation, SimulationType):
    import os
    import SetupFileGeneration
    #---------------------------------------------------------------------------------
    # IK (inverse kinematics)
    if SimulationType=='walk':
        IK_setup='2_Walk_IK_Setup.xml'                                                                                                                            # Setup file for the IK (Inverse Kinematics)
        SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '2_IK'))             # Create new folder for the results of IK
        cmd="opensim-cmd run-tool %s" %(IK_setup)
        os.system(cmd)                                                                                                                                                          # Run IK using command line
    elif SimulationType=='run':
        IK_setup='2_Run_IK_Setup.xml'                                                                                                                            # Setup file for the IK (Inverse Kinematics)
        SetupFileGeneration.dircreation(os.path.join(path_simulation,'Running simulation', 'Model outputs', '2_IK'))    # Create new folder for the results of IK
        cmd="opensim-cmd run-tool %s" %(IK_setup)
        os.system(cmd)                                                                                                                                                          # Run IK using command line
    #
def RRA(path_simulation, SimulationType):
    import os
    import RRA_evaluation
    import opensim as open
    import RRAModelMassModification
    import SetupFileGeneration
    #---------------------------------------------------------------------------------
    #RRA (Residual Reduction Algorithm)
    if SimulationType=='walk':
        loop_num=1                                                                                                                                                                    # The number of the times of the RRA analysis
        Residual=pErr=[100, 100, 100, 100]                                                                                                                              # The initial values set for the residual results, including Max and RMS residual force, residual moment, transportational and angular position error
        while Residual[0]>10 or Residual[1]>5 or Residual[2]>20 or Residual[3]>20 or pErr[0]>2 or pErr[1]>2 or pErr[2]>2 or pErr[3]>2:              # The criterion for the RRA analysis loop
            os.chdir(os.path.join(path_simulation, 'Gait simulation\Setup files'))                                                                                                               # Set the current working directory: Gait simulation/Setup files, this is required in the second RRA loop because it will change during the loop
            if loop_num==1:
                RRA_setup='3_Walk_rra_setup_rra1.xml'
            else:
                SetupFileGeneration.rra_setup(loop_num, SimulationType)                                                                                                              # From the second loop of RRA, a new setup file will be generated based on the RRA results
                RRA_setup='Walk_rra_setup_rra%d.xml' %(loop_num)
            SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '3_RRA'))                   # Create new folder for the results of RRA
            cmd="opensim-cmd run-tool %s" %(RRA_setup)
            os.system(cmd)                                                                                                                                                            # Simulation of RRA using command line
            RRA_massoutput='out.log'                                                                                                                                          # Read the RRA output log and get the recommended total mass change from RRA
            Totalmasschange=RRAModelMassModification.getRRAmassoutput(RRA_massoutput)                                        # Read the total mass change according to RRA from the out log
            path_RRAOutput=os.path.join(path_simulation,'Gait simulation', 'Model outputs','3_RRA')
            os.chdir(path_RRAOutput)                                                                                                                                          # Set the current working directory: Model outputs/3_RRA
            osimModel=open.Model("Fullbodymodel_Walk_RRA%d.osim" %(loop_num))                                                      # Assign model to osimModel
            osimModel_rrachanges=RRAModelMassModification.setBodyMassUsingRRAMassChange(osimModel,Totalmasschange)            # Adjust the mass of the body segment according to the RRA recommendation
            osimModel_rrachanges.printToXML("Fullbodymodel_Walk_RRA%d_modification.osim" %(loop_num))                                        # Save the adjusted model to osimModel_rrachanges
            [Residual, pErr]=RRA_evaluation.rra_evaluation(path=os.path.join(path_simulation, 'Gait simulation\Model outputs\\3_RRA'), RRA_directory='Results_rra_%d' %(loop_num),               # RRA evaluation
                                                                                            RRA_Residuals='rra_walk_%d_avgResiduals.txt' %(loop_num),
                                                                                            RRA_pErr_file='rra_walk_%d_pErr.sto' %(loop_num))
            loop_num=loop_num+1
            if loop_num>10:
                print('The RRA evaluation criterion is not achieved')
                break
        osimModel_rrachanges.printToXML('Fullbodymodel_Walk_RRA_modification_final.osim')
        return loop_num
    if SimulationType=='run':
        loop_num=1                                                                                                                                                                    # The number of the times of the RRA analysis
        Residual=pErr=[100, 100, 100, 100]                                                                                                                              # The initial values set for the residual results, including Max and RMS residual force, residual moment, transportational and angular position error
        while Residual[0]>10 or Residual[1]>5 or Residual[2]>20 or Residual[3]>20 or pErr[0]>2 or pErr[1]>2 or pErr[2]>2 or pErr[3]>2:              # The criterion for the RRA analysis loop
            os.chdir(os.path.join(path_simulation, 'Running simulation\Setup files'))                                                                                                               # Set the current working directory: Gait simulation/Setup files, this is required in the second RRA loop because it will change during the loop
            if loop_num==1:
                RRA_setup='3_Run_rra_setup_rra1.xml'
            else:
                SetupFileGeneration.rra_setup(loop_num, SimulationType)                                                                                                              # From the second loop of RRA, a new setup file will be generated based on the RRA results
                RRA_setup='Run_rra_setup_rra%d.xml' %(loop_num)
            SetupFileGeneration.dircreation(os.path.join(path_simulation,'Running simulation', 'Model outputs', '3_RRA'))                   # Create new folder for the results of RRA
            cmd="opensim-cmd run-tool %s" %(RRA_setup)
            os.system(cmd)                                                                                                                                                            # Simulation of RRA using command line
            RRA_massoutput='out.log'                                                                                                                                          # Read the RRA output log and get the recommended total mass change from RRA
            Totalmasschange=RRAModelMassModification.getRRAmassoutput(RRA_massoutput)                                        # Read the total mass change according to RRA from the out log
            path_RRAOutput=os.path.join(path_simulation,'Running simulation', 'Model outputs','3_RRA')
            os.chdir(path_RRAOutput)                                                                                                                                          # Set the current working directory: Model outputs/3_RRA
            osimModel=open.Model("Fullbodymodel_Run_RRA%d.osim" %(loop_num))                                                      # Assign model to osimModel
            osimModel_rrachanges=RRAModelMassModification.setBodyMassUsingRRAMassChange(osimModel,Totalmasschange)            # Adjust the mass of the body segment according to the RRA recommendation
            osimModel_rrachanges.printToXML("Fullbodymodel_Run_RRA%d_modification.osim" %(loop_num))                                        # Save the adjusted model to osimModel_rrachanges
            [Residual, pErr]=RRA_evaluation.rra_evaluation(path=os.path.join(path_simulation, 'Running simulation\Model outputs\\3_RRA'), RRA_directory='Results_rra_%d' %(loop_num),               # RRA evaluation
                                                                                            RRA_Residuals='rra_run_%d_avgResiduals.txt' %(loop_num),
                                                                                            RRA_pErr_file='rra_run_%d_pErr.sto' %(loop_num))
            loop_num=loop_num+1
            if loop_num>3:
                print('The RRA evaluation criterion is not achieved')
                break
        osimModel_rrachanges.printToXML('Fullbodymodel_Run_RRA_modification_final.osim')
        return loop_num
    #
def MuscleScaling (path_simulation, SimulationType, osimModel_origin, osimModel_scaled, height_origin, height_scaled, maxContractionVelocity):
    import RRAModelMassModification
    import opensim
    osimModel_origin=opensim.Model(osimModel_origin)
    osimModel_scaled=opensim.Model(osimModel_scaled)
    osimModel_adjusted=RRAModelMassModification.ScaleOptimalForceSubjectSpecific(osimModel_origin, osimModel_scaled, height_origin, height_scaled)
    osimModel_adjusted=RRAModelMassModification.setMaxContractionVelocityAllMuscles(osimModel_adjusted, maxContractionVelocity)
    if SimulationType=='walk':
        osimModel_adjusted.printToXML("Fullbodymodel_Walk_RRA_adjusted.osim")
    elif SimulationType=='run':
        osimModel_adjusted.printToXML("Fullbodymodel_Run_RRA_adjusted.osim")
    #
def CMC(path_simulation, SimulationType, results_directory):
    import os
    #--------------------------------------------------------------------------------
    #CMC (Computed Muscle Control)
    if SimulationType=='walk' or SimulationType=='walk_AFO':
        os.chdir(os.path.join(path_simulation, 'Simulation models\Gait simulation'+str(results_directory)+'\Setup files'))
        if SimulationType=='walk':
            CMC_setup='4_Walk_cmc_setup_withoutAFO.xml'
        if SimulationType=='walk_AFO':
            CMC_setup='4_Walk_cmc_setup_AFO.xml'
        results_directory='Model outputs/4_CMC//'+results_directory
        Setupfile_resultsdir(CMC_setup, results_directory)
        cmd="opensim-cmd run-tool %s" %(CMC_setup)
        os.system(cmd)
    if SimulationType=='run' or SimulationType=='run_AFO':
        os.chdir(os.path.join(path_simulation, 'Simulation models\Running simulation'+str(results_directory)+'\Setup files'))
        if SimulationType=='run':
            CMC_setup='4_Run_cmc_setup_withoutAFO.xml'
        if SimulationType=='run_AFO':
            CMC_setup='4_Run_cmc_setup_AFO.xml'
        results_directory='Model outputs/4_CMC//'+results_directory
        Setupfile_resultsdir(CMC_setup, results_directory)
        cmd="opensim-cmd run-tool %s" %(CMC_setup)
        os.system(cmd)
    #
def FD(path_simulation, SimulationType, results_directory):
    import os
    #--------------------------------------------------------------------------------
    #Forward Dynamics (FD)
    if SimulationType=='walk':
        os.chdir(os.path.join(path_simulation, 'Gait simulation\Setup files'))
        # SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '5_ForwardDynamics'))                   # Create new folder for the results of IK
        FD_setup='5_Walk_Forward_setup_withoutAFO.xml'
        #results_directory='Model outputs/5_ForwardDynamics/'+results_directory
        # To check whether the results directory exists or not, if no, create one
        """
        if not os.path.isdir(results_directory):
            os.makedirs(results_directory)
        Setupfile_resultsdir(FD_setup, results_directory)
        """
        cmd="opensim-cmd run-tool %s" %(FD_setup)
        os.system(cmd)
    if SimulationType=='walk_1stpart_withoutAFO' or SimulationType=='walk_1stpart_AFO' :
        os.chdir(os.path.join(path_simulation, 'Gait simulation\Setup files'))
        # SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '5_ForwardDynamics'))                   # Create new folder for the results of IK
        if SimulationType=='walk_1stpart_withoutAFO':
            FD_setup='5_Walk_Forward_setup_withoutAFO_1st.xml'
        elif SimulationType=='walk_1stpart_AFO':
            FD_setup='5_Walk_Forward_setup_AFO_1st.xml'
        results_directory='Model outputs/5_ForwardDynamics_1st/'+results_directory
        Setupfile_resultsdir(FD_setup, results_directory)
        cmd="opensim-cmd run-tool %s" %(FD_setup)
        os.system(cmd)
    if SimulationType=='walk_2ndpart_withoutAFO' or SimulationType=='walk_2ndpart_AFO':
        os.chdir(os.path.join(path_simulation, 'Gait simulation\Setup files'))
        # SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '5_ForwardDynamics'))                   # Create new folder for the results of IK
        if SimulationType=='walk_2ndpart_withoutAFO':
            FD_setup='5_Walk_Forward_setup_withoutAFO_2nd.xml'
        elif SimulationType=='walk_2ndpart_AFO':
            FD_setup='5_Walk_Forward_setup_AFO_2nd.xml'
        results_directory='Model outputs/5_ForwardDynamics_2nd/'+results_directory
        Setupfile_resultsdir(FD_setup, results_directory)
        cmd="opensim-cmd run-tool %s" %(FD_setup)
        os.system(cmd)
    if SimulationType=='run_withoutAFO' or SimulationType=='run_AFO':
        os.chdir(os.path.join(path_simulation, 'Running simulation\Setup files'))
        # SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '5_ForwardDynamics'))                   # Create new folder for the results of IK
        if SimulationType=='run_withoutAFO':
            FD_setup='5_Run_Forward_setup_withoutAFO.xml'
        elif SimulationType=='run_AFO':
            FD_setup='5_Run_Forward_setup_AFO.xml'
        results_directory='Model outputs/5_ForwardDynamics/'+results_directory
        Setupfile_resultsdir(FD_setup, results_directory)
        cmd="opensim-cmd run-tool %s" %(FD_setup)
        os.system(cmd)
        print(FD_setup)
    #
def FD_AFO(path_simulation, SimulationType):
    import os
    #--------------------------------------------------------------------------------
    #Forward Dynamics (FD)
    if SimulationType=='walk':
        os.chdir(os.path.join(path_simulation, 'Gait simulation\Setup files'))
        # SetupFileGeneration.dircreation(os.path.join(path_simulation,'Gait simulation', 'Model outputs', '5_ForwardDynamics'))                   # Create new folder for the results of IK
        FD_setup='5_Walk_Forward_setup_AFO.xml'
        cmd="opensim-cmd run-tool %s" %(FD_setup)
        os.system(cmd)
    #
#------------------------------------------------------------------------------------------------------------------------------------------
# Generate the set up file for the drop landing forward dynamics simulations, and run the FD simulation using the set up file
def ForwardDynamics_Droplanding(path, file_MBD, SetFile_forward, results_directory, run_finaltime):
    import numpy as np
    import os
    import opensim
    # Set the current working directory
    os.chdir(path)
    OsModel_full=os.path.join(path, file_MBD)

    # To generate forward setup file (.xml), first check, if no, to create one
    results_directory='DL simulation results/'+results_directory
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
    # Set and update the path to the local OpenSim geometry directory
    path='C:\OpenSim 4.1\Geometry'
    opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
    # To run the simulation
    cmd="opensim-cmd -L \"C:\OpenSim 4.1\\bin\osimExampleComponents.dll\"  run-tool %s" %(SetFile_forward)
    os.system(cmd)
    #
#------------------------------------------------------------------------------------------------------------------------------------------
# Change the results directory in the setup file based on the defined parameters
def Setupfile_resultsdir (SetupFile, results_directory):
    import os
    # To put the results directory in the Setup file
    with open (SetupFile,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open (SetupFile,"w",encoding="utf-8") as f_w:
        for line in lines:
            if line.strip().startswith('<results_directory>'):
                f_w.writelines(['		<results_directory>../',results_directory,'</results_directory>',"\n"])
            else:
                f_w.write(line)
    #
