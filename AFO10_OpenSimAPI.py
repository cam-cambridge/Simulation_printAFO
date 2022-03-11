import os
import opensim
import numpy as np
def LigMechanicsMax (Sim_output_folder, Sim_results, osimModel):
    # Aims: to export the maximum lengths and forces of the ligaments (i.e. AFO straps) during a specific motion
    # Inputs: osimModel: the opensim model with ligaments
    #             motSto_file: the motion file loaded to the model for length and forces exportion
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: Simulation_printAFO
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script:Simulation_printAFO_CAMG
    # Set and update the path to the local OpenSim geometry directory
    path='C:\OpenSim 4.1\Geometry'
    opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
    # Load the MSK model
    osimModel=os.path.join(path_simulation, osimModel)
    myModel=opensim.Model(osimModel)           # Load the opensim model
    state=myModel.initSystem()                    # Initial state
    # Load the motion file
    motSto_file=os.path.join(path_simulation, Sim_output_folder, Sim_results)
    motSto_file_type='states' in motSto_file        # Determine whether the file name includes 'states' or not, will be used in the below syntax
    # Storage the simulation results of motion
    motSto=opensim.Storage(motSto_file)
    timestep_motSto=motSto.getSize()    # The number of time step
    coords=myModel.getCoordinateSet()
    num_coords=coords.getSize() # Get the number of coordinates in the model, including coordinates of forceset, such as BackBushing et al.
    # Update each model coordinate for each time frame
    vars=['ankle_angle_r', 'subtalar_angle_r']    # The coordinates that will be updated for calculate the ligament length
    motSto_num=timestep_motSto    # The number of time instances selected for ligament lengths and forces
    motSto_interval=int(timestep_motSto/motSto_num)   # The number of intervals for the time instances
    strap_lengths=[]
    strap_forces=[]
    for j in range (0,motSto_num):
        for i, var in enumerate (vars):
            coordvalue=opensim.ArrayDouble()
            #currentcoord=coords.get(i).getName()   # Get the name of coordinates in opensim model
            if motSto_file_type==True:
                currentcoord_fullname='/jointset/'+var.replace('_angle_', '_')+'/'+var+'/value'
            else:
                currentcoord_fullname=var
            motSto.getDataColumn(currentcoord_fullname, coordvalue)
            q=coordvalue.getitem(j*motSto_interval)
            myModel.updCoordinateSet().get(var).setValue(state, np.radians(q), False)
        myModel.assemble(state)
        myModel.realizePosition(state)
        # Access ligament in models forceset & get ligament length after safedoncast
        fset=myModel.getForceSet()
        strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
        strap2=opensim.Ligament.safeDownCast(fset.get("orthosis_2"))
        strap3=opensim.Ligament.safeDownCast(fset.get("orthosis_3"))
        strap4=opensim.Ligament.safeDownCast(fset.get("orthosis_4"))
        strap_lengths.append([strap1.getLength(state), strap2.getLength(state), strap3.getLength(state), strap4.getLength(state)])
        myModel.computeStateVariableDerivatives(state)
        strap_forces.append([strap1.getTension(state), strap2.getTension(state), strap3.getTension(state), strap4.getTension(state)])
    strap_lengths_realtime=np.array(strap_lengths).T
    strap_forces_realtime=np.array(strap_forces).T
    strap_lengths_max=np.max(np.array(strap_lengths).T, axis=1)
    strap_forces_max=np.max(np.array(strap_forces).T, axis=1)
    return strap_lengths_realtime, strap_forces_realtime, strap_lengths_max, strap_forces_max
    #
def LigSetRestingLength(osimModel):
    # Set the resting length for the ligament (strap)
    # Set and update the path to the local OpenSim geometry directory
    path='C:\OpenSim 4.1\Geometry'
    opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
    # Load the model
    myModel=opensim.Model(osimModel)           # Load the opensim model
    state=myModel.initSystem()                    # Initial state
    fset=myModel.getForceSet()
    strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
    strap2=opensim.Ligament.safeDownCast(fset.get("orthosis_2"))
    strap3=opensim.Ligament.safeDownCast(fset.get("orthosis_3"))
    strap4=opensim.Ligament.safeDownCast(fset.get("orthosis_4"))
    # Get the lengths of the straps in the MSK model
    strap1_length=strap1.getLength(state)
    strap2_length=strap2.getLength(state)
    strap3_length=strap3.getLength(state)
    strap4_length=strap4.getLength(state)
    # Set the resting lengths for the straps using the extracted lengths
    strap1.set_resting_length(strap1_length)
    strap2.set_resting_length(strap2_length)
    strap3.set_resting_length(strap3_length)
    strap4.set_resting_length(strap4_length)
    myModel.printToXML(osimModel)
    #
def Liginitstates(osimModel):    # Define the raltive path of opensim model, e.g. relative to the python code
    # Aims: to export the lengths and forces of the ligaments (i.e. AFO straps) at the initial state of model
    # Inputs: osimModel: the opensim model with ligaments
    # Set and update the path to the local OpenSim geometry directory
    # Set and update the path to the local OpenSim geometry directory
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: Simulation_printAFO
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script:Simulation_printAFO_CAMG
    # Set and update the path to the local OpenSim geometry directory
    path='C:\OpenSim 4.1\Geometry'
    opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
    # Load the MSK model
    osimModel=os.path.join(path_simulation, osimModel)
    # Load the model
    myModel=opensim.Model(osimModel)           # Load the opensim model
    state=myModel.initSystem()                    # Initial state
    fset=myModel.getForceSet()
    strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
    strap2=opensim.Ligament.safeDownCast(fset.get("orthosis_2"))
    strap3=opensim.Ligament.safeDownCast(fset.get("orthosis_3"))
    strap4=opensim.Ligament.safeDownCast(fset.get("orthosis_4"))
    strap_lengths=[strap1.getLength(state), strap2.getLength(state), strap3.getLength(state), strap4.getLength(state)]
    myModel.computeStateVariableDerivatives(state)
    strap_forces=[strap1.getTension(state), strap2.getTension(state), strap3.getTension(state), strap4.getTension(state)]
    return strap_lengths, strap_forces
    #
def LigMechanicsRealtime (osimModel, motSto_file):
    # Aims: to export the real time lengths and forces of the ligaments (i.e. AFO straps) during a specific motion
    # Inputs: osimModel: the opensim model with ligaments
    #             motSto_file: the motion file loaded to the model for length and forces exportion
    # Set and update the path to the local OpenSim geometry directory
    path='C:\OpenSim 4.1\Geometry'
    opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
    # Load the model
    #osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'   # File path for opensim model
    #motSto_file='D:\Drop landing\DL simulation results\\11.mot'           # File path for motion file
    myModel=opensim.Model(osimModel)           # Load the opensim model
    state=myModel.initSystem()                    # Initial state
    motSto_file_type='states' in motSto_file        # Determine whether the file name includes 'states' or not, will be used in the below syntax
    # Storage the simulation results of motion
    motSto=opensim.Storage(motSto_file)
    timestep_motSto=motSto.getSize()    # The number of time step
    coords=myModel.getCoordinateSet()
    num_coords=coords.getSize() # Get the number of coordinates in the model, including coordinates of forceset, such as BackBushing et al.
    # Update each model coordinate for each time frame
    vars=['ankle_angle_r', 'subtalar_angle_r']    # The coordinates that will be updated for calculate the ligament length
    motSto_num=timestep_motSto    # The number of time instances selected for ligament lengths and forces
    motSto_interval=int(timestep_motSto/motSto_num)   # The number of intervals for the time instances
    strap_lengths=[]
    strap_forces=[]
    for j in range (1,motSto_num):
        for i, var in enumerate (vars):
            coordvalue=opensim.ArrayDouble()
            #currentcoord=coords.get(i).getName()   # Get the name of coordinates in opensim model
            if motSto_file_type==True:
                currentcoord_fullname='/jointset/'+var.replace('_angle_', '_')+'/'+var+'/value'
            else:
                currentcoord_fullname=var
            motSto.getDataColumn(currentcoord_fullname, coordvalue)
            q=coordvalue.getitem(j*motSto_interval)
            myModel.updCoordinateSet().get(var).setValue(state, np.radians(q), False)
        myModel.assemble(state)
        myModel.realizePosition(state)
        # Access ligament in models forceset & get ligament length after safedoncast
        fset=myModel.getForceSet()
        strap1=opensim.Ligament.safeDownCast(fset.get("orthosis_1"))
        strap2=opensim.Ligament.safeDownCast(fset.get("orthosis_2"))
        strap3=opensim.Ligament.safeDownCast(fset.get("orthosis_3"))
        strap4=opensim.Ligament.safeDownCast(fset.get("orthosis_4"))
        strap_lengths.append([strap1.getLength(state), strap2.getLength(state), strap3.getLength(state), strap4.getLength(state)])
        myModel.computeStateVariableDerivatives(state)
        strap_forces.append([strap1.getTension(state), strap2.getTension(state), strap3.getTension(state), strap4.getTension(state)])
    strap_lengths=np.array(strap_lengths).T
    strap_forces=np.array(strap_forces).T
    return strap_lengths, strap_forces
    #
def LigPeneMonitor(strap_lengths_realtime, strap_length_ini, threshold):
    strap_lengths_grad=[]
    strap_pene_monitor=[]
    for strap_num in range (len(strap_lengths_realtime)):
        strap_lengths_grad_temp=[]
        strap_pene_monitor_temp='No Penetration'
        strap_length_index=0
        for i,j in zip(strap_lengths_realtime[strap_num], strap_lengths_realtime[strap_num][1:]):
            strap_length_index+=1
            strap_lengths_grad_temp.append(j-i)
            if abs(j-i)>threshold:
                print(j-i)
                if strap_lengths_realtime[strap_num][strap_length_index] - strap_length_ini[strap_num] > 0:
                    strap_pene_monitor_temp='Penetration stretch'
                else:
                    strap_pene_monitor_temp='Penetration slack'
        strap_lengths_grad.append(strap_lengths_grad_temp)
        strap_pene_monitor.append(strap_pene_monitor_temp)
    return strap_lengths_grad, strap_pene_monitor
    #
if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt
    output_folder_DL_platform0='D:\Trial\Gait simulation0\Model outputs\\4_CMC\\0'
    osimModel_platform0='D:\Trial\Gait simulation0\Model outputs\\3_RRA\Fullbodymodel_Walk_RRA_final_AFO.osim'
    [strap_lengths, strap_forces, strap_lengths_max, strap_forces_max]=LigMechanicsMax(output_folder_DL_platform0, 'cmc_Kinematics_q.sto', osimModel_platform0)
    #[strap_length_grad, strap_pene_monitor]=LigPeneMonitor(strap_lengths, 0.004)
    [strap_length_ini, strap_forces_ini]=Liginitstates(osimModel_platform0)
    #strap_length_ini_reshape=np.array(strap_length_ini).reshape(-1,1)
    #strap_length_rate=strap_lengths/strap_length_ini_reshape
    [strap_length_grad, strap_pene_monitor]=LigPeneMonitor(strap_lengths, strap_length_ini, 0.003)

    strap_length_grad_grad=[]
    a=1
    for num in range(len(strap_length_grad)):
        strap_length_grad_grad_temp=[]
        for i,j in zip (strap_length_grad[num], strap_length_grad[num][1:]):
            strap_length_grad_grad_temp.append(j/i)
        strap_length_grad_grad.append(strap_length_grad_grad_temp)
    strap_length_grad=strap_length_grad_grad
    #strap_length_grad=strap_lengths

    [nrow,ncolumn]=np.array(strap_length_grad).shape
    strap_length_grad_index=list(range(ncolumn))
    print(strap_pene_monitor)

    """
    osimModel='D:\Trial\Drop landing0\Fullbodymodel_DL_platform0_AFO.osim'
    Results_file='D:\Trial\Drop landing0\DL simulation results\\02500\default_states_degrees1.mot'
    [strap_length_ini, strap_force_ini]=Liginitstates(osimModel)
    [strap_lengths, strap_forces]=LigMechanicsRealtime(osimModel, Results_file)
    #strap_length_ini_reshape=np.array(strap_length_ini).reshape(-1,1)
    #strap_length_rate=strap_lengths/strap_length_ini_reshape
    #[nrow, ncolumn]=strap_lengths.shape
    #strap_length_index=list(range(ncolumn))
    strap_length_grad=[]
    for strap_num in range (len(strap_lengths)):
        strap_length_grad_temp=[]
        for i,j in zip(strap_lengths[strap_num], strap_lengths[strap_num][1:]):
            strap_length_grad_temp.append(j-i)
        strap_length_grad.append(strap_length_grad_temp)
    [nrow,ncolumn]=np.array(strap_length_grad).shape
    strap_length_grad_index=list(range(ncolumn))
    """

    plt.figure()
    plt.subplot(2,2,1)
    #plt.plot(strap_length_index, strap_lengths[0], marker='o', label='Strap lengths for strap 1')
    #plt.plot(strap_length_index, strap_length_rate[0], marker='o', label='Strap lengths for strap 1')
    plt.plot(strap_length_grad_index, strap_length_grad[0], marker='o', label='Strap lengths for strap 1')
    #plt.xlim((0,800))
    #plt.ylim((-0.02, 0.002))
    plt.subplot(2,2,2)
    #plt.plot(strap_length_index, strap_lengths[1], marker='o', label='Strap lengths for strap 2')
    #plt.plot(strap_length_index, strap_length_rate[1], marker='o', label='Strap lengths for strap 2')
    plt.plot(strap_length_grad_index, strap_length_grad[1], marker='o', label='Strap lengths for strap 2')
    #plt.xlim((0,800))
    #plt.ylim((-0.02, 0.002))
    plt.subplot(2,2,3)
    #plt.plot(strap_length_index, strap_lengths[2], marker='o', label='Strap lengths for strap 3')
    #plt.plot(strap_length_index, strap_length_rate[2], marker='o', label='Strap lengths for strap 3')
    plt.plot(strap_length_grad_index, strap_length_grad[2], marker='o', label='Strap lengths for strap 3')
    #plt.xlim((0,800))
    #plt.ylim((-0.02, 0.002))
    plt.subplot(2,2,4)
    #plt.plot(strap_length_index, strap_lengths[3], marker='o', label='Strap lengths for strap 4')
    #plt.plot(strap_length_index, strap_length_rate[3], marker='o', label='Strap lengths for strap 4')
    plt.plot(strap_length_grad_index, strap_length_grad[3], marker='o', label='Strap lengths for strap 4')
    #plt.xlim((0,800))
    #plt.ylim((-0.02, 0.002))
    plt.show()

    """
    # The plot of the force-length relationship in one figure
    plt.figure()
    plt.plot(strap_lengths[0], strap_forces[0], marker='o', label='Strap FL for strap 1')
    plt.plot(strap_lengths[1], strap_forces[1], marker='o', label='Strap FL for strap 2')
    plt.plot(strap_lengths[2], strap_forces[2], marker='o', label='Strap FL for strap 3')
    plt.plot(strap_lengths[3], strap_forces[3], marker='o', label='Strap FL for strap 4')
    plt.show()
    """

    """
    # Save results to an excel files
    exe_file='D:\Trial\Strap forces and lengths.xlsx'
    sheet_name='Sheet1'
    strap_length_forces=np.vstack((strap_lengths, strap_forces)).T
    data_pd=pd.DataFrame(strap_length_forces)
    data_pd.columns=['strap_1_length', 'strap_2_length', 'strap_3_length', 'strap_4_length', 'strap_1_force', 'strap_2_force', 'strap_3_force', 'strap_4_force']
    data_writer=pd.ExcelWriter(exe_file)
    data_pd.to_excel(data_writer, sheet_name)
    data_writer.save()
    data_writer.close()
    #
    """

"""
# The API of getting the length and force in GUI
myModel=getCurrentModel()
fset=myModel.getForceSet()
strap=modeling.Ligament.safeDownCast(fset.get("orthosis_4"))
state=myModel.initSystem()
length=strap.getLength(state)
myModel.computeStateVariableDerivatives(state)
strap_force=strap.getTension(state)
"""
