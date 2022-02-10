def LigMechanics (osimModel, motSto_file):
    # Aims: to export the lengths and forces of the ligaments (i.e. AFO straps) during a specific motion
    # Inputs: osimModel: the opensim model with ligaments
    #             motSto_file: the motion file loaded to the model for length and forces exportion
    import opensim
    import numpy as np
    # Set and update the path to the local OpenSim geometry directory
    path='C:\OpenSim 4.1\Geometry'
    opensim.ModelVisualizer.addDirToGeometrySearchPaths(path)
    # Load the model
    #osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'   # File path for opensim model
    #motSto_file='D:\Drop landing\DL simulation results\\11.mot'           # File path for motion file
    myModel=opensim.Model(osimModel)           # Load the opensim model
    state=myModel.initSystem()                    # Initial state
    # Storage the simulation results of motion
    motSto=opensim.Storage(motSto_file)
    timestep_motSto=motSto.getSize()    # The number of time step
    coords=myModel.getCoordinateSet()
    num_coords=coords.getSize() # Get the number of coordinates in the model, including coordinates of forceset, such as BackBushing et al.
    # Update each model coordinate for each time frame
    vars=['knee_angle_r', 'ankle_angle_r', 'subtalar_angle_r']    # The coordinates that will be updated for calculate the ligament length
    motSto_num=12    # The number of time instances selected for ligament lengths and forces
    motSto_interval=int(timestep_motSto/motSto_num)   # The number of intervals for the time instances
    strap_lengths=[]
    strap_forces=[]
    for j in range (1,motSto_num):
        for i, var in enumerate (vars):
            coordvalue=opensim.ArrayDouble()
            #currentcoord=coords.get(i).getName()   # Get the name of coordinates in opensim model
            currentcoord_fullname='/jointset/'+var.replace('_angle_', '_')+'/'+var+'/value'
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
def Liginitstates(osimModel):
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
if __name__ == '__main__':
    osimModel='D:\Drop landing\Fullbodymodel_droplanding_AFO.osim'   # File path for opensim model
    motSto_file='D:\Drop landing\DL simulation results\\11.mot'           # File path for motion file
    [strap_lengths_init, strap_forces_init]=Liginitstates(osimModel)
    [strap_lengths, strap_forces]=LigMechanics(osimModel, motSto_file)
    print(strap_lengths_init)
    print(strap_forces_init)
