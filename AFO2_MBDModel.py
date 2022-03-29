import numpy as np
import math
import opensim
import AFO9_MeshMechanics
import AFO10_OpenSimAPI
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Drop landing model - New AFO design with strap orientations in the musculoskeletal model for drop landing
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def MBDmodel_Droplanding_AFO (file_MBD, Platform_inclination, AFO_representation, AFO_material, DesignVariables):
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_strap_length]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_strap_length=AFO_representation[2]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_Fmagnitude=AFO_material[0]
    AFO_F_L=AFO_material[1]
    [AFO_bottom_location, AFO_top_location, theta_0_values, n_elements]=DesignVariables    # Design variables
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Read the MBD osim file and add the coordinate value of the AFO strip end points in the the model
    Platform_inclination1=[math.radians(Platform_inclination[0]), math.radians(Platform_inclination[1]), math.radians(Platform_inclination[2])]
    with open (file_MBD,"r",encoding="utf-8") as f:
        lines=f.readlines()
        with open(file_MBD,"w",encoding="utf-8") as f_w:
            index=0
            index_t=0
            for line in lines:
                index +=1
                if line.strip()=='<Coordinate name="platform_rx">':
                    f_w.write(line)
                    lines[index+1]='							<default_value>%f</default_value>' % (Platform_inclination1[0]) + '\n'
                elif line.strip()=='<Coordinate name="platform_ry">':
                    f_w.write(line)
                    lines[index+1]='							<default_value>%f</default_value>' % (Platform_inclination1[1]) + '\n'
                elif line.strip()=='<Coordinate name="platform_rz">':
                    f_w.write(line)
                    lines[index+1]='							<default_value>%f</default_value>' % (Platform_inclination1[2]) + '\n'
                elif line.strip()=='</CoordinateLimitForce>' and not lines[index].strip().startswith('<CoordinateLimitForce'):
                    index_t=index
                    f_w.write(line)
                elif index_t !=0 and line.strip()!='<groups>':
                    pass
                elif index_t!=0 and line.strip()=='<groups>':
                    index_t=0
                    for k1 in range (len(AFO_top_tibial)):
                        AFO_F_L_T=AFO_F_L[k1]
                        # AFO_F_L_T=AFO_F_L_T.reshape(2,-1)
                        f_w.writelines(['				<Ligament name="orthosis_',str(k1+1),'">',"\n"])
                        f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                        <appliesForce>true</appliesForce>
                        <!--the set of points defining the path of the ligament-->
                        <GeometryPath name="geometrypath">
                            <!--The set of points defining the path-->
                            <PathPointSet>
                                <objects>\n'''])
                        f_w.writelines(['								<PathPoint name="orthosis_',str(k1+1),'-P1">',"\n"])
                        f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                        <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                        <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                        AFO_top_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial[k1,0],AFO_top_tibial[k1,1],AFO_top_tibial[k1,2])
                        f_w.writelines(["									<location>",AFO_top_withoutbracket,"</location>\n","								</PathPoint>\n"])
                        f_w.writelines(['								<PathPoint name="orthosis_',str(k1+1),'-P2">',"\n"])
                        f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                        <socket_parent_frame>/bodyset/calcn_r</socket_parent_frame>
                                        <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                        AFO_bottom_withoutbracket='%.8f %.8f %.8f' %(AFO_bottom_calcn[k1,0],AFO_bottom_calcn[k1,1],AFO_bottom_calcn[k1,2])
                        f_w.writelines(["									<location>",AFO_bottom_withoutbracket,"</location>\n"])
                        f_w.writelines(['''								</PathPoint>
                                </objects>
                                <groups />
                            </PathPointSet>
                            <!--The wrap objects that are associated with this path-->
                            <PathWrapSet>
    							<objects>
    								<PathWrap name="pathwrap">
    									<!--A WrapObject that this PathWrap interacts with.-->
    									<wrap_object>foot_r_tibia</wrap_object>
    									<!--The wrapping method used to solve the path around the wrap object.-->
    									<method>hybrid</method>
    									<!--The range of indices to use to compute the path over the wrap object.-->
    									<range>-1 -1</range>
    								</PathWrap>
    							</objects>
    							<groups />
    						</PathWrapSet>
                            <!--Default appearance attributes for this GeometryPath-->
                            <Appearance>
                                <!--Flag indicating whether the associated Geometry is visible or hidden.-->
                                <visible>true</visible>
                                <!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
                                <color>0 1 0</color>
                            </Appearance>
                        </GeometryPath>
                        <!--resting length of the ligament-->\n'''])
                        AFO_strap_length_withoutbracket='%.8f' %(AFO_strap_length[k1])
                        f_w.writelines(["					<resting_length>",AFO_strap_length_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                        f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude),"</pcsa_force>\n"])
                        f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                        <SimmSpline name="force_length_curve">\n'''])
                        f_w.writelines(['''                    					<x>'''])
                        for j in range (len(AFO_F_L_T[0])):
                            f_w.write(str(AFO_F_L_T[0][j]))
                            f_w.write(' ')
                        f_w.writelines(['''</x>
                                            <y>'''])
                        for m in range (len(AFO_F_L_T[1])):
                            f_w.write(str(AFO_F_L_T[1][m]))
                            f_w.write(' ')
                        f_w.writelines(['''</y>
                        </SimmSpline>
                    </Ligament>\n'''])
                    f_w.writelines(['''			</objects>\n'''])
                    f_w.write(line)
                else:
                    f_w.write(line)
    # Set the resting lengths of the straps in the MSK model
    AFO10_OpenSimAPI.LigSetRestingLength(file_MBD)
    # Set the Force-length FL relationship in the MSK model
    AFO_FLrelationship=AFO9_MeshMechanics.MeshMechanics(file_MBD, theta_0_values, n_elements) # The force length relationship calculated from AFO9_MeshMechanics
    # Change the force-length relationship in the MSK model to the one obtained from the AFO9_MeshMechanics
    with open (file_MBD, "r+", encoding="utf-8") as f:
        lines=f.read()
        f.seek(0)
        for i in range (len(AFO_FLrelationship)):
            FL_x_str=' '.join(str(i) for i in AFO_FLrelationship[i][0])
            # Change the x and y values of force-length relationship from <x> 1 <x> to real number
            lines=lines.replace('<x> '+ str(i+1)+' </x>', '<x> '+str(FL_x_str)+' </x>')  # No space between <x> and str(i+1)
            lines=lines.replace('<x>'+ str(i+1)+' </x>', '<x>'+str(FL_x_str)+' </x>')  # No space between <x> and str(i+1) in left
            lines=lines.replace('<x> '+ str(i+1)+'</x>', '<x> '+str(FL_x_str)+'</x>')  # No space between <x> and str(i+1) in right
            lines=lines.replace('<x>'+ str(i+1)+'</x>', '<x>'+str(FL_x_str)+'</x>')  # No space between <x> and str(i+1) in both sides
            FL_y_str=' '.join(str(i) for i in AFO_FLrelationship[i][1])
            lines=lines.replace('<y> '+ str(i+1)+' </y>', '<y> '+str(FL_y_str)+' </y>')
            lines=lines.replace('<y>'+ str(i+1)+' </y>', '<y>'+str(FL_y_str)+' </y>')
            lines=lines.replace('<y> '+ str(i+1)+'</y>', '<y> '+str(FL_y_str)+'</y>')
            lines=lines.replace('<y>'+ str(i+1)+'</y>', '<y>'+str(FL_y_str)+'</y>')
        f.write(lines)
    #
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def MBDmodel_Gait_AFO (MBD_model, MBD_model_AFO, AFO_representation, AFO_material, DesignVariables):                  # MBD model file with AFO with default position: angular postion=[0]
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_length]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_strap_length=AFO_representation[2]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_Fmagnitude=AFO_material[0]
    AFO_F_L=AFO_material[1]
    [AFO_bottom_location, AFO_top_location, theta_0_values, n_elements]=DesignVariables    # Design variables
    # Read the MBD osim file and add the coordinate value of the AFO strip end points in the the model
    with open (MBD_model,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open(MBD_model_AFO,"w",encoding="utf-8") as f_w:
        index=0
        index_t=0
        for line in lines:
            index +=1
            if lines[index-7].strip().startswith('<mesh_file>r_fibula.vtp</mesh_file>') and line.strip()!='<WrapCylinder name="foot_r_tibia">':
                f_w.writelines(['''							<WrapCylinder name="foot_r_tibia">
								<!--Whether or not the WrapObject is considered active in computing paths-->
								<active>true</active>
								<!--Body-fixed Euler angle sequence for the orientation of the WrapObject-->
								<xyz_body_rotation>1.5707963 0 0</xyz_body_rotation>
								<!--Translation of the WrapObject.-->
								<translation>-0.00949 -0.38 0.006</translation>
								<!--The name of quadrant over which the wrap object is active. For example, '+x' or '-y' to set the sidedness of the wrapping.-->
								<quadrant>all</quadrant>
								<!--Default appearance for this Geometry-->
								<Appearance>
									<!--Flag indicating whether the associated Geometry is visible or hidden.-->
									<visible>true</visible>
									<!--The opacity used to display the geometry between 0:transparent, 1:opaque.-->
									<opacity>1</opacity>
									<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
									<color>0 1 1</color>
									<!--Visuals applied to surfaces associated with this Appearance.-->
									<SurfaceProperties>
										<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
										<representation>3</representation>
									</SurfaceProperties>
								</Appearance>
								<!--The radius of the cylinder.-->
								<radius>0.0365</radius>
								<!--The length of the cylinder.-->
								<length>0.18</length>
							</WrapCylinder>\n'''])
            if line.strip()=='</CoordinateActuator>' and not lines[index].strip().startswith('<CoordinateActuator') and not lines[index].strip().startswith('<PointActuator'):
                index_t=index
                f_w.write(line)
            elif index_t !=0 and line.strip()!='<groups>':
                pass
            elif index_t!=0 and line.strip()=='<groups>':
                index_t=0
                for k1 in range (len(AFO_top_tibial)):
                    AFO_F_L_T=AFO_F_L[k1]
                    #AFO_F_L_T=AFO_F_L_T.reshape(2,-1)
                    f_w.writelines(['				<Ligament name="orthosis_',str(k1+1),'">',"\n"])
                    f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                    <appliesForce>true</appliesForce>
                    <!--the set of points defining the path of the ligament-->
                    <GeometryPath name="geometrypath">
                        <!--The set of points defining the path-->
                        <PathPointSet>
                            <objects>\n'''])
                    f_w.writelines(['								<PathPoint name="orthosis_',str(k1+1),'-P1">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_top_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial[k1,0],AFO_top_tibial[k1,1],AFO_top_tibial[k1,2])
                    f_w.writelines(["									<location>",AFO_top_withoutbracket,"</location>\n","								</PathPoint>\n"])
                    f_w.writelines(['								<PathPoint name="orthosis_',str(k1+1),'-P2">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/calcn_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_bottom_withoutbracket='%.8f %.8f %.8f' %(AFO_bottom_calcn[k1,0],AFO_bottom_calcn[k1,1],AFO_bottom_calcn[k1,2])
                    f_w.writelines(["									<location>",AFO_bottom_withoutbracket,"</location>\n"])
                    f_w.writelines(['''								</PathPoint>
                            </objects>
                            <groups />
                        </PathPointSet>
                        <!--The wrap objects that are associated with this path-->
                        <PathWrapSet>
                            <objects>
                                <PathWrap name="pathwrap">
                                    <!--A WrapObject that this PathWrap interacts with.-->
                                    <wrap_object>foot_r_tibia</wrap_object>
                                    <!--The wrapping method used to solve the path around the wrap object.-->
                                    <method>hybrid</method>
                                    <!--The range of indices to use to compute the path over the wrap object.-->
                                    <range>-1 -1</range>
                                </PathWrap>
                            </objects>
                            <groups />
                        </PathWrapSet>
                        <!--Default appearance attributes for this GeometryPath-->
                        <Appearance>
                            <!--Flag indicating whether the associated Geometry is visible or hidden.-->
                            <visible>true</visible>
                            <!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
                            <color>0 1 0</color>
                        </Appearance>
                    </GeometryPath>
                    <!--resting length of the ligament-->\n'''])
                    AFO_length_withoutbracket='%.8f' %(AFO_strap_length[k1])
                    f_w.writelines(["					<resting_length>",AFO_length_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                    f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude),"</pcsa_force>\n"])
                    f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                    <SimmSpline name="force_length_curve">\n'''])
                    f_w.writelines(['''                    					<x>'''])
                    for j in range (len(AFO_F_L_T[0])):
                        f_w.write(str(AFO_F_L_T[0][j]))
                        f_w.write(' ')
                    f_w.writelines(['''</x>
                                        <y>'''])
                    for m in range (len(AFO_F_L_T[1])):
                        f_w.write(str(AFO_F_L_T[1][m]))
                        f_w.write(' ')
                    f_w.writelines(['''</y>
                    </SimmSpline>
                </Ligament>\n'''])
                f_w.writelines(['''			</objects>\n'''])
                f_w.write(line)
            else:
                f_w.write(line)
    # Set the resting lengths of the straps in the MSK model
    AFO10_OpenSimAPI.LigSetRestingLength(MBD_model_AFO)
    # Set the Force-length FL relationship in the MSK model
    AFO_FLrelationship=AFO9_MeshMechanics.MeshMechanics(MBD_model_AFO, theta_0_values, n_elements) # The force length relationship calculated from AFO9_MeshMechanics
    # Change the force-length relationship in the MSK model to the one obtained from the AFO9_MeshMechanics
    with open (MBD_model_AFO, "r+", encoding="utf-8") as f:
        lines=f.read()
        f.seek(0)
        for i in range (len(AFO_FLrelationship)):
            FL_x_str=' '.join(str(i) for i in AFO_FLrelationship[i][0])
            lines=lines.replace('<x> '+ str(i+1)+' </x>', '<x> '+str(FL_x_str)+' </x>')  # No space between <x> and str(i+1)
            lines=lines.replace('<x>'+ str(i+1)+' </x>', '<x>'+str(FL_x_str)+' </x>')  # No space between <x> and str(i+1) in left
            lines=lines.replace('<x> '+ str(i+1)+'</x>', '<x> '+str(FL_x_str)+'</x>')  # No space between <x> and str(i+1) in right
            lines=lines.replace('<x>'+ str(i+1)+'</x>', '<x>'+str(FL_x_str)+'</x>')  # No space between <x> and str(i+1) in both sides
            FL_y_str=' '.join(str(i) for i in AFO_FLrelationship[i][1])
            lines=lines.replace('<y> '+ str(i+1)+' </y>', '<y> '+str(FL_y_str)+' </y>')
            lines=lines.replace('<y>'+ str(i+1)+' </y>', '<y>'+str(FL_y_str)+' </y>')
            lines=lines.replace('<y> '+ str(i+1)+'</y>', '<y> '+str(FL_y_str)+'</y>')
            lines=lines.replace('<y>'+ str(i+1)+'</y>', '<y>'+str(FL_y_str)+'</y>')
        f.write(lines)
#
