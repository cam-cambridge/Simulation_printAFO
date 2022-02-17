import opensim
import numpy as np
def LigMechanicsMax (Sim_output_folder, Sim_results, osimModel):
    # Aims: to export the maximum lengths and forces of the ligaments (i.e. AFO straps) during a specific motion
    # Inputs: osimModel: the opensim model with ligaments
    #             motSto_file: the motion file loaded to the model for length and forces exportion
    import os
    import opensim
    import numpy as np
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
    strap_lengths_max=np.max(np.array(strap_lengths).T, axis=1)
    strap_forces_max=np.max(np.array(strap_forces).T, axis=1)
    return strap_lengths_max, strap_forces_max
    #
def LigSetRestingLength(osimModel):
    # Set the resting length for the ligament (strap)
    import opensim
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
def Liginitstates(osimModel):
    # Aims: to export the lengths and forces of the ligaments (i.e. AFO straps) at the initial state of model
    # Inputs: osimModel: the opensim model with ligaments
    # Set and update the path to the local OpenSim geometry directory
    import opensim
    import numpy as np
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
    import opensim
    import numpy as np
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
if __name__ == '__main__':
    import pandas as pd
    osimModel='D:\Trial\\3_RRA\Fullbodymodel_Walk_RRA_final_AFO.osim'
    DL_results_output_folder='D:\Trial\\4_CMC\\1'
    DL_results='cmc_states.sto'
    [strap_length_max, strap_forces_max]=LigMechanicsMax(DL_results_output_folder, DL_results, osimModel)
    print(strap_forces_max)
    # Save results to an excel files
    exe_file='D:\Trial\Results_20220210.xlsx'
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
# The API of getting the length and force in GUI
myModel=getCurrentModel()
fset=myModel.getForceSet()
strap=modeling.Ligament.safeDownCast(fset.get("orthosis_4"))
state=myModel.initSystem()
length=strap.getLength(state)
myModel.computeStateVariableDerivatives(state)
strap_force=strap.getTension(state)
"""
