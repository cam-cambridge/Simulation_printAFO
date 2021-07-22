#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Drop landing model - New AFO design with stripe orientations in the musculoskeletal model for drop landing
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def MBDmodel_Droplanding_AFO (file_MBD, Platform_inclination, AFO_representation, AFO_material):
    import numpy as np
    import math
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_stripe_length]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_stripe_length=AFO_representation[2]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_Fmagnitude=AFO_material[0]
    AFO_F_L=AFO_material[1]
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
                        AFO_F_L_T=AFO_F_L_T.reshape(2,-1)
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
                        AFO_stripe_length_withoutbracket='%.8f' %(AFO_stripe_length[k1])
                        f_w.writelines(["					<resting_length>",AFO_stripe_length_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
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
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def MBDmodel_Gait_AFO (MBD_model, MBD_model_AFO, AFO_representation, AFO_material):                  # MBD model file with AFO with default position: angular postion=[0]
    import numpy as np
    import math
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_length]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_stripe_length=AFO_representation[2]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_Fmagnitude=AFO_material[0]
    AFO_F_L=AFO_material[1]

    """
    # AFO_material=[AFO_Fmagnitude_side, AFO_FLrelationship_side, AFO_Fmagnitude_front, AFO_FLrelationship_front]
    # AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_length=AFO_representation[2]
    # AFO_representation in AFO side
    AFO_top_tibial_side=AFO_top_tibial[0]
    AFO_bottom_calcn_side=AFO_bottom_calcn[0]
    AFO_length_side=AFO_length[0]
    # AFO_representation in AFO front
    AFO_top_tibial_front=AFO_top_tibial[1]
    AFO_bottom_calcn_front=AFO_bottom_calcn[1]
    AFO_length_front=AFO_length[1]
    # AFO_material=[AFO_Fmagnitude_side, AFO_FLrelationship_side, AFO_Fmagnitude_front, AFO_FLrelationship_front]
    AFO_Fmagnitude_side=AFO_material[0]
    AFO_F_L_side=AFO_material[1]
    AFO_Fmagnitude_front=AFO_material[2]
    AFO_F_L_front=AFO_material[3]
    """

    # Read the MBD osim file and add the coordinate value of the AFO strip end points in the the model
    with open (MBD_model,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open(MBD_model_AFO,"w",encoding="utf-8") as f_w:
        index=0
        index_t=0
        for line in lines:
            index +=1
            if line.strip()=='</CoordinateActuator>' and not lines[index].strip().startswith('<CoordinateActuator') and not lines[index].strip().startswith('<PointActuator'):
                index_t=index
                f_w.write(line)
            elif index_t !=0 and line.strip()!='<groups>':
                pass
            elif index_t!=0 and line.strip()=='<groups>':
                index_t=0
                for k1 in range (len(AFO_top_tibial)):
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
                    AFO_length_withoutbracket='%.8f' %(AFO_stripe_length[k1])
                    f_w.writelines(["					<resting_length>",AFO_length_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                    f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude),"</pcsa_force>\n"])
                    f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                    <SimmSpline name="force_length_curve">\n'''])
                    f_w.writelines(['''                    					<x>'''])
                    for j in range (len(AFO_F_L[0])):
                        f_w.write(str(AFO_F_L[0][j]))
                        f_w.write(' ')
                    f_w.writelines(['''</x>
                                        <y>'''])
                    for m in range (len(AFO_F_L[1])):
                        f_w.write(str(AFO_F_L[1][m]))
                        f_w.write(' ')
                    f_w.writelines(['''</y>
                    </SimmSpline>
                </Ligament>\n'''])
                f_w.writelines(['''			</objects>\n'''])
                f_w.write(line)
            else:
                f_w.write(line)


def MBDfile_Droplanding_orgin(MBD_model, MBD_model_droplanding, Platform_inclination):                             # Set the model in drop landing position, add the interface property between the model and platform
    import numpy as np
    import math
    import re
    with open (MBD_model,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open(MBD_model_droplanding,"w",encoding="utf-8") as f_w:
        index=0
        index_t=0
        for line in lines:
            index +=1
            if line.strip()=='<objects>' and lines[index-2].strip()=='<BodySet name="bodyset">':
                f_w.write(line)
                f_w.writelines(['''				<Body name="platform">
					<!--The geometry used to display the axes of this Frame.-->
					<FrameGeometry name="frame_geometry">
						<!--Path to a Component that satisfies the Socket 'frame' of type Frame.-->
						<socket_frame>..</socket_frame>
						<!--Scale factors in X, Y, Z directions respectively.-->
						<scale_factors>0.20000000000000001 0.20000000000000001 0.20000000000000001</scale_factors>
					</FrameGeometry>
					<!--List of geometry attached to this Frame. Note, the geometry are treated as fixed to the frame and they share the transform of the frame when visualized-->
					<attached_geometry />
					<!--Set of wrap objects fixed to this body that GeometryPaths can wrap over.This property used to be a member of Body but was moved up with the introduction of Frames.-->
					<WrapObjectSet name="wrapobjectset">
						<objects />
						<groups />
					</WrapObjectSet>
					<!--The mass of the body (kg)-->
					<mass>0.10000000000000001</mass>
					<!--The location (Vec3) of the mass center in the body frame.-->
					<mass_center>0 0 0</mass_center>
					<!--The elements of the inertia tensor (Vec6) as [Ixx Iyy Izz Ixy Ixz Iyz] measured about the mass_center and not the body origin.-->
					<inertia>0.001 0.001 0.001 0 0 0</inertia>
				</Body>\n'''])                                                             # Add the platform
            elif line.strip()=='<objects>' and lines[index-2].strip()=='<JointSet name="jointset">':
                f_w.write(line)
                f_w.writelines(['''				<CustomJoint name="ground_platform">
					<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The parent frame for the joint.).-->
					<socket_parent_frame>ground_offset</socket_parent_frame>
					<!--Path to a Component that satisfies the Socket 'child_frame' of type PhysicalFrame (description: The child frame for the joint.).-->
					<socket_child_frame>platform_offset</socket_child_frame>
					<!--List containing the generalized coordinates (q's) that parameterize this joint.-->
					<coordinates>
						<Coordinate name="platform_rx">
							<!--The value of this coordinate before any value has been set. Rotational coordinate value is in radians and Translational in meters.-->
							<default_value>0.523599</default_value>
							<!--The speed value of this coordinate before any value has been set. Rotational coordinate value is in rad/s and Translational in m/s.-->
							<default_speed_value>0</default_speed_value>
							<!--The minimum and maximum values that the coordinate can range between. Rotational coordinate range in radians and Translational in meters.-->
							<range>-3.1415999999999999 3.1415999999999999</range>
							<!--Flag indicating whether or not the values of the coordinates should be limited to the range, above.-->
							<clamped>true</clamped>
							<!--Flag indicating whether or not the values of the coordinates should be constrained to the current (e.g. default) value, above.-->
							<locked>true</locked>
							<!--If specified, the coordinate can be prescribed by a function of time. It can be any OpenSim Function with valid second order derivatives.-->
							<prescribed_function />
							<!--Flag indicating whether or not the values of the coordinates should be prescribed according to the function above. It is ignored if the no prescribed function is specified.-->
							<prescribed>false</prescribed>
						</Coordinate>
						<Coordinate name="platform_ry">
							<!--The value of this coordinate before any value has been set. Rotational coordinate value is in radians and Translational in meters.-->
							<default_value>0.000000</default_value>
							<!--The speed value of this coordinate before any value has been set. Rotational coordinate value is in rad/s and Translational in m/s.-->
							<default_speed_value>0</default_speed_value>
							<!--The minimum and maximum values that the coordinate can range between. Rotational coordinate range in radians and Translational in meters.-->
							<range>-3.1415999999999999 3.1415999999999999</range>
							<!--Flag indicating whether or not the values of the coordinates should be limited to the range, above.-->
							<clamped>true</clamped>
							<!--Flag indicating whether or not the values of the coordinates should be constrained to the current (e.g. default) value, above.-->
							<locked>true</locked>
							<!--If specified, the coordinate can be prescribed by a function of time. It can be any OpenSim Function with valid second order derivatives.-->
							<prescribed_function />
							<!--Flag indicating whether or not the values of the coordinates should be prescribed according to the function above. It is ignored if the no prescribed function is specified.-->
							<prescribed>false</prescribed>
						</Coordinate>
						<Coordinate name="platform_rz">
							<!--The value of this coordinate before any value has been set. Rotational coordinate value is in radians and Translational in meters.-->
							<default_value>0.000000</default_value>
							<!--The speed value of this coordinate before any value has been set. Rotational coordinate value is in rad/s and Translational in m/s.-->
							<default_speed_value>0</default_speed_value>
							<!--The minimum and maximum values that the coordinate can range between. Rotational coordinate range in radians and Translational in meters.-->
							<range>-3.1415999999999999 3.1415999999999999</range>
							<!--Flag indicating whether or not the values of the coordinates should be limited to the range, above.-->
							<clamped>true</clamped>
							<!--Flag indicating whether or not the values of the coordinates should be constrained to the current (e.g. default) value, above.-->
							<locked>true</locked>
							<!--If specified, the coordinate can be prescribed by a function of time. It can be any OpenSim Function with valid second order derivatives.-->
							<prescribed_function />
							<!--Flag indicating whether or not the values of the coordinates should be prescribed according to the function above. It is ignored if the no prescribed function is specified.-->
							<prescribed>false</prescribed>
						</Coordinate>
						<Coordinate name="platform_ty">
							<!--The value of this coordinate before any value has been set. Rotational coordinate value is in radians and Translational in meters.-->
							<default_value>-0.5</default_value>
							<!--The speed value of this coordinate before any value has been set. Rotational coordinate value is in rad/s and Translational in m/s.-->
							<default_speed_value>0</default_speed_value>
							<!--The minimum and maximum values that the coordinate can range between. Rotational coordinate range in radians and Translational in meters.-->
							<range>-5 1</range>
							<!--Flag indicating whether or not the values of the coordinates should be limited to the range, above.-->
							<clamped>true</clamped>
							<!--Flag indicating whether or not the values of the coordinates should be constrained to the current (e.g. default) value, above.-->
							<locked>true</locked>
							<!--If specified, the coordinate can be prescribed by a function of time. It can be any OpenSim Function with valid second order derivatives.-->
							<prescribed_function />
							<!--Flag indicating whether or not the values of the coordinates should be prescribed according to the function above. It is ignored if the no prescribed function is specified.-->
							<prescribed>false</prescribed>
						</Coordinate>
					</coordinates>
					<!--Physical offset frames owned by the Joint that are typically used to satisfy the owning Joint's parent and child frame connections (sockets). PhysicalOffsetFrames are often used to describe the fixed transformation from a Body's origin to another location of interest on the Body (e.g., the joint center). When the joint is deleted, so are the PhysicalOffsetFrame components in this list.-->
					<frames>
						<PhysicalOffsetFrame name="ground_offset">
							<!--The geometry used to display the axes of this Frame.-->
							<FrameGeometry name="frame_geometry">
								<!--Path to a Component that satisfies the Socket 'frame' of type Frame.-->
								<socket_frame>..</socket_frame>
								<!--Scale factors in X, Y, Z directions respectively.-->
								<scale_factors>0.20000000000000001 0.20000000000000001 0.20000000000000001</scale_factors>
							</FrameGeometry>
							<!--Path to a Component that satisfies the Socket 'parent' of type C (description: The parent frame to this frame.).-->
							<socket_parent>/ground</socket_parent>
							<!--Translational offset (in meters) of this frame's origin from the parent frame's origin, expressed in the parent frame.-->
							<translation>0 0 0</translation>
							<!--Orientation offset (in radians) of this frame in its parent frame, expressed as a frame-fixed x-y-z rotation sequence.-->
							<orientation>0 0 0</orientation>
						</PhysicalOffsetFrame>
						<PhysicalOffsetFrame name="platform_offset">
							<!--The geometry used to display the axes of this Frame.-->
							<FrameGeometry name="frame_geometry">
								<!--Path to a Component that satisfies the Socket 'frame' of type Frame.-->
								<socket_frame>..</socket_frame>
								<!--Scale factors in X, Y, Z directions respectively.-->
								<scale_factors>0.20000000000000001 0.20000000000000001 0.20000000000000001</scale_factors>
							</FrameGeometry>
							<!--Path to a Component that satisfies the Socket 'parent' of type C (description: The parent frame to this frame.).-->
							<socket_parent>/bodyset/platform</socket_parent>
							<!--Translational offset (in meters) of this frame's origin from the parent frame's origin, expressed in the parent frame.-->
							<translation>0 0 0</translation>
							<!--Orientation offset (in radians) of this frame in its parent frame, expressed as a frame-fixed x-y-z rotation sequence.-->
							<orientation>0 0 0</orientation>
						</PhysicalOffsetFrame>
					</frames>
					<!--Defines how the child body moves with respect to the parent as a function of the generalized coordinates.-->
					<SpatialTransform>
						<!--3 Axes for rotations are listed first.-->
						<TransformAxis name="rotation1">
							<!--Names of the coordinates that serve as the independent variables         of the transform function.-->
							<coordinates>platform_rx</coordinates>
							<!--Rotation or translation axis for the transform.-->
							<axis>1 0 0</axis>
							<!--Transform function of the generalized coordinates used to        represent the amount of displacement along a specified axis.-->
							<LinearFunction name="function">
								<coefficients> 1 0</coefficients>
							</LinearFunction>
						</TransformAxis>
						<TransformAxis name="rotation2">
							<!--Names of the coordinates that serve as the independent variables         of the transform function.-->
							<coordinates>platform_ry</coordinates>
							<!--Rotation or translation axis for the transform.-->
							<axis>0 1 0</axis>
							<!--Transform function of the generalized coordinates used to        represent the amount of displacement along a specified axis.-->
							<LinearFunction name="function">
								<coefficients> 1 0</coefficients>
							</LinearFunction>
						</TransformAxis>
						<TransformAxis name="rotation3">
							<!--Names of the coordinates that serve as the independent variables         of the transform function.-->
							<coordinates>platform_rz</coordinates>
							<!--Rotation or translation axis for the transform.-->
							<axis>0 0 1</axis>
							<!--Transform function of the generalized coordinates used to        represent the amount of displacement along a specified axis.-->
							<LinearFunction name="function">
								<coefficients> 1 0</coefficients>
							</LinearFunction>
						</TransformAxis>
						<!--3 Axes for translations are listed next.-->
						<TransformAxis name="translation1">
							<!--Names of the coordinates that serve as the independent variables         of the transform function.-->
							<coordinates></coordinates>
							<!--Rotation or translation axis for the transform.-->
							<axis>1 0 0</axis>
							<!--Transform function of the generalized coordinates used to        represent the amount of displacement along a specified axis.-->
							<Constant name="function">
								<value>0</value>
							</Constant>
						</TransformAxis>
						<TransformAxis name="translation2">
							<!--Names of the coordinates that serve as the independent variables         of the transform function.-->
							<coordinates>platform_ty</coordinates>
							<!--Rotation or translation axis for the transform.-->
							<axis>0 1 0</axis>
							<!--Transform function of the generalized coordinates used to        represent the amount of displacement along a specified axis.-->
							<LinearFunction name="function">
								<coefficients> 1 0</coefficients>
							</LinearFunction>
						</TransformAxis>
						<TransformAxis name="translation3">
							<!--Names of the coordinates that serve as the independent variables         of the transform function.-->
							<coordinates></coordinates>
							<!--Rotation or translation axis for the transform.-->
							<axis>0 0 -1</axis>
							<!--Transform function of the generalized coordinates used to        represent the amount of displacement along a specified axis.-->
							<Constant name="function">
								<value>0</value>
							</Constant>
						</TransformAxis>
					</SpatialTransform>
				</CustomJoint>\n'''])                                                           # Add the joint for the platform
            elif line.strip()=='<objects />' and lines[index-2].strip()=='<ContactGeometrySet name="contactgeometryset">':
                f_w.writelines(['''			<objects>
				<ContactHalfSpace name="platform">
					<!--Path to a Component that satisfies the Socket 'frame' of type PhysicalFrame (description: The frame to which this geometry is attached.).-->
					<socket_frame>/bodyset/platform</socket_frame>
					<!--Location of geometry center in the PhysicalFrame.-->
					<location>0 0 0</location>
					<!--Orientation of geometry in the PhysicalFrame (body-fixed XYZ Euler angles).-->
					<orientation>0 0 -1.5707963300000001</orientation>
					<!--Default appearance for this Geometry-->
					<Appearance>
						<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
						<color>0 1 1</color>
						<!--Visuals applied to surfaces associated with this Appearance.-->
						<SurfaceProperties>
							<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
							<representation>3</representation>
						</SurfaceProperties>
					</Appearance>
				</ContactHalfSpace>
				<ContactSphere name="heel_r">
					<!--Path to a Component that satisfies the Socket 'frame' of type PhysicalFrame (description: The frame to which this geometry is attached.).-->
					<socket_frame>/bodyset/calcn_r</socket_frame>
					<!--Location of geometry center in the PhysicalFrame.-->
					<location>0.01 0.01 -0.0050000000000000001</location>
					<!--Orientation of geometry in the PhysicalFrame (body-fixed XYZ Euler angles).-->
					<orientation>0 0 0</orientation>
					<!--Default appearance for this Geometry-->
					<Appearance>
						<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
						<color>0 1 1</color>
						<!--Visuals applied to surfaces associated with this Appearance.-->
						<SurfaceProperties>
							<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
							<representation>3</representation>
						</SurfaceProperties>
					</Appearance>
					<!--Radius of the sphere (default: 0).-->
					<radius>0.029999999999999999</radius>
				</ContactSphere>
				<ContactSphere name="ball_big_toe_r">
					<!--Path to a Component that satisfies the Socket 'frame' of type PhysicalFrame (description: The frame to which this geometry is attached.).-->
					<socket_frame>/bodyset/toes_r</socket_frame>
					<!--Location of geometry center in the PhysicalFrame.-->
					<location>-0.0050000000000000001 0.0050000000000000001 -0.029999999999999999</location>
					<!--Orientation of geometry in the PhysicalFrame (body-fixed XYZ Euler angles).-->
					<orientation>0 0 0</orientation>
					<!--Default appearance for this Geometry-->
					<Appearance>
						<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
						<color>0 1 1</color>
						<!--Visuals applied to surfaces associated with this Appearance.-->
						<SurfaceProperties>
							<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
							<representation>3</representation>
						</SurfaceProperties>
					</Appearance>
					<!--Radius of the sphere (default: 0).-->
					<radius>0.02</radius>
				</ContactSphere>
				<ContactSphere name="small_toe_r">
					<!--Path to a Component that satisfies the Socket 'frame' of type PhysicalFrame (description: The frame to which this geometry is attached.).-->
					<socket_frame>/bodyset/toes_r</socket_frame>
					<!--Location of geometry center in the PhysicalFrame.-->
					<location>-0.040000000000000001 0.0050000000000000001 0.040000000000000001</location>
					<!--Orientation of geometry in the PhysicalFrame (body-fixed XYZ Euler angles).-->
					<orientation>0 0 0</orientation>
					<!--Default appearance for this Geometry-->
					<Appearance>
						<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
						<color>0 1 1</color>
						<!--Visuals applied to surfaces associated with this Appearance.-->
						<SurfaceProperties>
							<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
							<representation>3</representation>
						</SurfaceProperties>
					</Appearance>
					<!--Radius of the sphere (default: 0).-->
					<radius>0.014999999999999999</radius>
				</ContactSphere>
				<ContactSphere name="heel_l">
					<!--Path to a Component that satisfies the Socket 'frame' of type PhysicalFrame (description: The frame to which this geometry is attached.).-->
					<socket_frame>/bodyset/calcn_l</socket_frame>
					<!--Location of geometry center in the PhysicalFrame.-->
					<location>0.01 0.01 0.0050000000000000001</location>
					<!--Orientation of geometry in the PhysicalFrame (body-fixed XYZ Euler angles).-->
					<orientation>0 0 0</orientation>
					<!--Default appearance for this Geometry-->
					<Appearance>
						<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
						<color>0 1 1</color>
						<!--Visuals applied to surfaces associated with this Appearance.-->
						<SurfaceProperties>
							<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
							<representation>3</representation>
						</SurfaceProperties>
					</Appearance>
					<!--Radius of the sphere (default: 0).-->
					<radius>0.029999999999999999</radius>
				</ContactSphere>
				<ContactSphere name="ball_big_toe_l">
					<!--Path to a Component that satisfies the Socket 'frame' of type PhysicalFrame (description: The frame to which this geometry is attached.).-->
					<socket_frame>/bodyset/toes_l</socket_frame>
					<!--Location of geometry center in the PhysicalFrame.-->
					<location>-0.0050000000000000001 0.0050000000000000001 0.029999999999999999</location>
					<!--Orientation of geometry in the PhysicalFrame (body-fixed XYZ Euler angles).-->
					<orientation>0 0 0</orientation>
					<!--Default appearance for this Geometry-->
					<Appearance>
						<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
						<color>0 1 1</color>
						<!--Visuals applied to surfaces associated with this Appearance.-->
						<SurfaceProperties>
							<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
							<representation>3</representation>
						</SurfaceProperties>
					</Appearance>
					<!--Radius of the sphere (default: 0).-->
					<radius>0.02</radius>
				</ContactSphere>
				<ContactSphere name="small_toe_l">
					<!--Path to a Component that satisfies the Socket 'frame' of type PhysicalFrame (description: The frame to which this geometry is attached.).-->
					<socket_frame>/bodyset/toes_l</socket_frame>
					<!--Location of geometry center in the PhysicalFrame.-->
					<location>-0.040000000000000001 0.0050000000000000001 -0.040000000000000001</location>
					<!--Orientation of geometry in the PhysicalFrame (body-fixed XYZ Euler angles).-->
					<orientation>0 0 0</orientation>
					<!--Default appearance for this Geometry-->
					<Appearance>
						<!--The color, (red, green, blue), [0, 1], used to display the geometry. -->
						<color>0 1 1</color>
						<!--Visuals applied to surfaces associated with this Appearance.-->
						<SurfaceProperties>
							<!--The representation (1:Points, 2:Wire, 3:Shaded) used to display the object.-->
							<representation>3</representation>
						</SurfaceProperties>
					</Appearance>
					<!--Radius of the sphere (default: 0).-->
					<radius>0.014999999999999999</radius>
				</ContactSphere>
            </objects>\n'''])                 # Define the relationship between the platform and foots
            else:
                f_w.write(line)

    Platform_inclination_radian=[math.radians(Platform_inclination[0]), math.radians(Platform_inclination[1]), math.radians(Platform_inclination[2])]                      # Change the Platform_inclination angles  from degree to radians
    # -------------------------------------------------------------------------------------------------------------------------------------------------
    # The matrix for the default poses of the MBD model for drop landing simulation
    poses_coord=['platform_ty=-0.5', 'pelvis_tilt=-12', 'pelvis_list=0', 'pelvis_rotation=0', 'pelvis_tx=0.05', 'pelvis_ty=0.92', 'pelvis_tz=0', 'hip_flexion_r=20', 'hip_adduction_r=-1', 'hip_rotation_r=5', 'knee_angle_r=20',
                                   'ankle_angle_r=11.5', 'subtalar_angle_r=-0.03', 'mtp_angle_r=0', 'hip_flexion_l=-20', 'hip_adduction_l=10', 'hip_rotation_l=5', 'knee_angle_l=120',  'ankle_angle_l=11.5', 'subtalar_angle_l=-0.03', 'mtp_angle_l=0',
                                   'lumbar_extension=0', 'lumbar_bending=0', 'lumbar_rotation=0']
    poses_coord_value=[]
    pattern=re.compile('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?')
    for i in range (len(poses_coord)):
        poses_coord_tem=pattern.findall(poses_coord[i])
        poses_coord_tem=float(list(map(float, poses_coord_tem))[0])
        if poses_coord[i]!='platform_ty=-0.5' and  poses_coord[i]!='pelvis_tx=0.05' and poses_coord[i]!='pelvis_ty=0.92' and poses_coord[i]!='pelvis_tz=0':
            poses_coord_tem=math.radians(poses_coord_tem)
        poses_coord_value.append(poses_coord_tem)

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Define the variation parameters of the model, including platform inclination, poses parameters of the body
    with open (MBD_model_droplanding,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open(MBD_model_droplanding,"w",encoding="utf-8") as f_w:
        index=0
        for line in lines:
            index +=1
            #-----------------------------------------------------------------------------------------------------------------------------------------------
            # Define the inclination angles of platform
            if line.strip()=='<Coordinate name="platform_rx">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (Platform_inclination_radian[0]) + '\n'
            elif line.strip()=='<Coordinate name="platform_ry">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (Platform_inclination_radian[1]) + '\n'
            elif line.strip()=='<Coordinate name="platform_rz">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (Platform_inclination_radian[2]) + '\n'
            # ---------------------------------------------------------------------------------------------------------------------------------------
            # Define poses coordinate values
            elif line.strip()=='<Coordinate name="platform_ty">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[0]) + '\n'
            elif line.strip()=='<Coordinate name="pelvis_tilt">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[1]) + '\n'
            elif line.strip()=='<Coordinate name="pelvis_list">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[2]) + '\n'
            elif line.strip()=='<Coordinate name="pelvis_rotation">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[3]) + '\n'
            elif line.strip()=='<Coordinate name="pelvis_tx">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[4]) + '\n'
            elif line.strip()=='<Coordinate name="pelvis_ty">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[5]) + '\n'
            elif line.strip()=='<Coordinate name="pelvis_tz">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[6]) + '\n'
            elif line.strip()=='<Coordinate name="hip_flexion_r">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[7]) + '\n'
            elif line.strip()=='<Coordinate name="hip_adduction_r">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[8]) + '\n'
            elif line.strip()=='<Coordinate name="hip_rotation_r">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[9]) + '\n'
            elif line.strip()=='<Coordinate name="knee_angle_r">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[10]) + '\n'
                lines[index+5]='							<range>-0.17453293, 2.0943950999999998 </range>' + '\n'
            elif line.strip()=='<Coordinate name="ankle_angle_r">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[11]) + '\n'
            elif line.strip()=='<Coordinate name="subtalar_angle_r">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[12]) + '\n'
            elif line.strip()=='<Coordinate name="mtp_angle_r">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[13]) + '\n'
            elif line.strip()=='<Coordinate name="hip_flexion_l">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[14]) + '\n'
            elif line.strip()=='<Coordinate name="hip_adduction_l">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[15]) + '\n'
            elif line.strip()=='<Coordinate name="hip_rotation_l">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[16]) + '\n'
            elif line.strip()=='<Coordinate name="knee_angle_l">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[17]) + '\n'
                lines[index+5]='							<range>-2.0943950999999998, 2.0943950999999998 </range>' + '\n'
            elif line.strip()=='<Coordinate name="ankle_angle_l">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[18]) + '\n'
            elif line.strip()=='<Coordinate name="subtalar_angle_l">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[19]) + '\n'
            elif line.strip()=='<Coordinate name="mtp_angle_l">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[20]) + '\n'
            elif line.strip()=='<Coordinate name="lumbar_extension">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[21]) + '\n'
            elif line.strip()=='<Coordinate name="lumbar_bending">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[22]) + '\n'
            elif line.strip()=='<Coordinate name="lumbar_rotation">':
                f_w.write(line)
                lines[index+1]='							<default_value>%f</default_value>' % (poses_coord_value[23]) + '\n'
            else:
                f_w.write(line)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Old previouse scripts
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# The drop landing mode with AFO developed originally_20210130
# The AFO strips in side and front have the same material properties
def MBDmodel_Droplanding_AFO_20210130 (file_MBD, Platform_inclination, AFO_representation, AFO_material):
    import numpy as np
    import math
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_length]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_length=AFO_representation[2]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_Fmagnitude=AFO_material[0]
    AFO_F_L=AFO_material[1]
    #AFO_F_L=np.array([[-1,-0.5,-0.25,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.6,0.7,0.8,0.9,1],[0,0,0,0,0,0,0.01,0.015,0.02,0.03,0.07,0.2,0.32,0.45,0.62,0.75,0.86,0.94,1]])
    #AFO_Fmagnitude=AFO_material[0]
    #AFO_F_L=AFO_material[1]

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
                    for k in range (len(AFO_top_tibial)):
                        f_w.writelines(['				<Ligament name="orthosis_',str(k+1),'_r">',"\n"])
                        f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                        <appliesForce>true</appliesForce>
                        <!--the set of points defining the path of the ligament-->
                        <GeometryPath name="geometrypath">
                            <!--The set of points defining the path-->
                            <PathPointSet>
                                <objects>\n'''])
                        f_w.writelines(['								<PathPoint name="orthosis_',str(k+1),'_r-P1">',"\n"])
                        f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                        <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                        <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                        AFO_top_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial[k,0],AFO_top_tibial[k,1],AFO_top_tibial[k,2])
                        f_w.writelines(["									<location>",AFO_top_withoutbracket,"</location>\n","								</PathPoint>\n"])
                        f_w.writelines(['								<PathPoint name="orthosis_',str(k+1),'_r-P2">',"\n"])
                        f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                        <socket_parent_frame>/bodyset/calcn_r</socket_parent_frame>
                                        <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                        AFO_bottom_withoutbracket='%.8f %.8f %.8f' %(AFO_bottom_calcn[k,0],AFO_bottom_calcn[k,1],AFO_bottom_calcn[k,2])
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
                        			<PathWrap name="pathwrap_0">
                        				<!--A WrapObject that this PathWrap interacts with.-->
                        				<wrap_object>foot_r_calcn</wrap_object>
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
                        AFO_length_withoutbracket='%.8f' %(AFO_length[k])
                        f_w.writelines(["					<resting_length>",AFO_length_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                        f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude),"</pcsa_force>\n"])
                        f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                        <SimmSpline name="force_length_curve">\n'''])
                        f_w.writelines(['''                    					<x>'''])
                        for j in range (len(AFO_F_L[0])):
                            f_w.write(str(AFO_F_L[0][j]))
                            f_w.write(' ')
                        f_w.writelines(['''</x>
                                            <y>'''])
                        for m in range (len(AFO_F_L[1])):
                            f_w.write(str(AFO_F_L[1][m]))
                            f_w.write(' ')
                        f_w.writelines(['''</y>
                        </SimmSpline>
                    </Ligament>\n'''])
                    f_w.writelines(['''			</objects>\n'''])
                    f_w.write(line)
                else:
                    f_w.write(line)

def AFO_MBDfile_20210307(MBD_model, MBD_model_AFO, AFO_representation, AFO_material):                  # MBD model file with AFO with default position: angular postion=[0]
    import numpy as np
    import math
    # AFO_representation=[AFO_top_tibial, AFO_bottom_calcn, AFO_length]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_length=AFO_representation[2]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_Fmagnitude=AFO_material[0]
    AFO_F_L=AFO_material[1]

    # Read the MBD osim file and add the coordinate value of the AFO strip end points in the the model
    with open (MBD_model,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open(MBD_model_AFO,"w",encoding="utf-8") as f_w:
        index=0
        index_t=0
        for line in lines:
            index +=1
            if line.strip()=='</CoordinateActuator>' and not lines[index].strip().startswith('<CoordinateActuator') and not lines[index].strip().startswith('<PointActuator'):
                index_t=index
                f_w.write(line)
            elif index_t !=0 and line.strip()!='<groups>':
                pass
            elif index_t!=0 and line.strip()=='<groups>':
                index_t=0
                for k in range (len(AFO_top_tibial)):
                    f_w.writelines(['				<Ligament name="orthosis_',str(k+1),'_r">',"\n"])
                    f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                    <appliesForce>true</appliesForce>
                    <!--the set of points defining the path of the ligament-->
                    <GeometryPath name="geometrypath">
                        <!--The set of points defining the path-->
                        <PathPointSet>
                            <objects>\n'''])
                    f_w.writelines(['								<PathPoint name="orthosis_',str(k+1),'_r-P1">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_top_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial[k,0],AFO_top_tibial[k,1],AFO_top_tibial[k,2])
                    f_w.writelines(["									<location>",AFO_top_withoutbracket,"</location>\n","								</PathPoint>\n"])
                    f_w.writelines(['								<PathPoint name="orthosis_',str(k+1),'_r-P2">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/calcn_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_bottom_withoutbracket='%.8f %.8f %.8f' %(AFO_bottom_calcn[k,0],AFO_bottom_calcn[k,1],AFO_bottom_calcn[k,2])
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
                                <PathWrap name="pathwrap_0">
                                    <!--A WrapObject that this PathWrap interacts with.-->
                                    <wrap_object>foot_r_calcn</wrap_object>
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
                    AFO_length_withoutbracket='%.8f' %(AFO_length[k])
                    f_w.writelines(["					<resting_length>",AFO_length_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                    f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude),"</pcsa_force>\n"])
                    f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                    <SimmSpline name="force_length_curve">\n'''])
                    f_w.writelines(['''                    					<x>'''])
                    for j in range (len(AFO_F_L[0])):
                        f_w.write(str(AFO_F_L[0][j]))
                        f_w.write(' ')
                    f_w.writelines(['''</x>
                                        <y>'''])
                    for m in range (len(AFO_F_L[1])):
                        f_w.write(str(AFO_F_L[1][m]))
                        f_w.write(' ')
                    f_w.writelines(['''</y>
                    </SimmSpline>
                </Ligament>\n'''])
                f_w.writelines(['''			</objects>\n'''])
                f_w.write(line)
            else:
                f_w.write(line)

#
def MBDmodel_Droplanding_AFO_20210716 (file_MBD, Platform_inclination, AFO_representation, AFO_material):
    import numpy as np
    import math
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_stripe_length]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_stripe_length=AFO_representation[2]
    # AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_Fmagnitude=AFO_material[0]
    AFO_F_L=AFO_material[1]

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
                        AFO_F_L_T=AFO_F_L_T.reshape(2,-1)
                        f_w.writelines(['				<Ligament name="orthosis_',str(k1+1),'_r">',"\n"])
                        f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                        <appliesForce>true</appliesForce>
                        <!--the set of points defining the path of the ligament-->
                        <GeometryPath name="geometrypath">
                            <!--The set of points defining the path-->
                            <PathPointSet>
                                <objects>\n'''])
                        f_w.writelines(['								<PathPoint name="orthosis_',str(k1+1),'_r-P1">',"\n"])
                        f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                        <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                        <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                        AFO_top_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial[k1,0],AFO_top_tibial[k1,1],AFO_top_tibial[k1,2])
                        f_w.writelines(["									<location>",AFO_top_withoutbracket,"</location>\n","								</PathPoint>\n"])
                        f_w.writelines(['								<PathPoint name="orthosis_',str(k1+1),'_r-P2">',"\n"])
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
    								<PathWrap name="pathwrap_0">
    									<!--A WrapObject that this PathWrap interacts with.-->
    									<wrap_object>foot_r_calcn</wrap_object>
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
                        AFO_stripe_length_withoutbracket='%.8f' %(AFO_stripe_length[k1])
                        f_w.writelines(["					<resting_length>",AFO_stripe_length_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
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
                    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    # Previous model with side and front AFO
                    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    """
                    for k2 in range (len(AFO_top_tibial_front)):
                        f_w.writelines(['				<Ligament name="orthosis_front_',str(k2+1),'_r">',"\n"])
                        f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                        <appliesForce>true</appliesForce>
                        <!--the set of points defining the path of the ligament-->
                        <GeometryPath name="geometrypath">
                            <!--The set of points defining the path-->
                            <PathPointSet>
                                <objects>\n'''])
                        f_w.writelines(['								<PathPoint name="orthosis_front_',str(k2+1),'_r-P1">',"\n"])
                        f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                        <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                        <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                        AFO_top_front_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial_front[k2,0],AFO_top_tibial_front[k2,1],AFO_top_tibial_front[k2,2])
                        f_w.writelines(["									<location>",AFO_top_front_withoutbracket,"</location>\n","								</PathPoint>\n"])
                        f_w.writelines(['								<PathPoint name="orthosis_front_',str(k2+1),'_r-P2">',"\n"])
                        f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                        <socket_parent_frame>/bodyset/calcn_r</socket_parent_frame>
                                        <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                        AFO_bottom_front_withoutbracket='%.8f %.8f %.8f' %(AFO_bottom_calcn_front[k2,0],AFO_bottom_calcn_front[k2,1],AFO_bottom_calcn_front[k2,2])
                        f_w.writelines(["									<location>",AFO_bottom_front_withoutbracket,"</location>\n"])
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
    								<PathWrap name="pathwrap_0">
    									<!--A WrapObject that this PathWrap interacts with.-->
    									<wrap_object>foot_r_calcn</wrap_object>
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
                        AFO_length_front_withoutbracket='%.8f' %(AFO_length_front[k2])
                        f_w.writelines(["					<resting_length>",AFO_length_front_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                        f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude_front),"</pcsa_force>\n"])
                        f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                        <SimmSpline name="force_length_curve">\n'''])
                        f_w.writelines(['''                    					<x>'''])
                        for j in range (len(AFO_F_L_front[0])):
                            f_w.write(str(AFO_F_L_front[0][j]))
                            f_w.write(' ')
                        f_w.writelines(['''</x>
                                            <y>'''])
                        for m in range (len(AFO_F_L_front[1])):
                            f_w.write(str(AFO_F_L_front[1][m]))
                            f_w.write(' ')
                        f_w.writelines(['''</y>
                        </SimmSpline>
                    </Ligament>\n'''])
                    """
                    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    f_w.writelines(['''			</objects>\n'''])
                    f_w.write(line)
                else:
                    f_w.write(line)
#
# Change def AFO_MBDfile to MBDmodel_Gait_AFO
def AFO_MBDfile_20210721 (MBD_model, MBD_model_AFO, AFO_representation, AFO_material):                  # MBD model file with AFO with default position: angular postion=[0]
    import numpy as np
    import math
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_length]
                                          # AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
                                          # AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
                                          # AFO_length=[AFO_length_side, AFO_length_front]
    # AFO_material=[AFO_Fmagnitude_side, AFO_FLrelationship_side, AFO_Fmagnitude_front, AFO_FLrelationship_front]
    # AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    AFO_top_tibial=AFO_representation[0]
    AFO_bottom_calcn=AFO_representation[1]
    AFO_length=AFO_representation[2]
    # AFO_representation in AFO side
    AFO_top_tibial_side=AFO_top_tibial[0]
    AFO_bottom_calcn_side=AFO_bottom_calcn[0]
    AFO_length_side=AFO_length[0]
    # AFO_representation in AFO front
    AFO_top_tibial_front=AFO_top_tibial[1]
    AFO_bottom_calcn_front=AFO_bottom_calcn[1]
    AFO_length_front=AFO_length[1]

    # AFO_material=[AFO_Fmagnitude_side, AFO_FLrelationship_side, AFO_Fmagnitude_front, AFO_FLrelationship_front]
    AFO_Fmagnitude_side=AFO_material[0]
    AFO_F_L_side=AFO_material[1]
    AFO_Fmagnitude_front=AFO_material[2]
    AFO_F_L_front=AFO_material[3]

    # Read the MBD osim file and add the coordinate value of the AFO strip end points in the the model
    with open (MBD_model,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open(MBD_model_AFO,"w",encoding="utf-8") as f_w:
        index=0
        index_t=0
        for line in lines:
            index +=1
            if line.strip()=='</CoordinateActuator>' and not lines[index].strip().startswith('<CoordinateActuator') and not lines[index].strip().startswith('<PointActuator'):
                index_t=index
                f_w.write(line)
            elif index_t !=0 and line.strip()!='<groups>':
                pass
            elif index_t!=0 and line.strip()=='<groups>':
                index_t=0
                for k1 in range (len(AFO_top_tibial_side)):
                    f_w.writelines(['				<Ligament name="orthosis_side_',str(k1+1),'_r">',"\n"])
                    f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                    <appliesForce>true</appliesForce>
                    <!--the set of points defining the path of the ligament-->
                    <GeometryPath name="geometrypath">
                        <!--The set of points defining the path-->
                        <PathPointSet>
                            <objects>\n'''])
                    f_w.writelines(['								<PathPoint name="orthosis_side_',str(k1+1),'_r-P1">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_top_side_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial_side[k1,0],AFO_top_tibial_side[k1,1],AFO_top_tibial_side[k1,2])
                    f_w.writelines(["									<location>",AFO_top_side_withoutbracket,"</location>\n","								</PathPoint>\n"])
                    f_w.writelines(['								<PathPoint name="orthosis_side_',str(k1+1),'_r-P2">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/calcn_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_bottom_side_withoutbracket='%.8f %.8f %.8f' %(AFO_bottom_calcn_side[k1,0],AFO_bottom_calcn_side[k1,1],AFO_bottom_calcn_side[k1,2])
                    f_w.writelines(["									<location>",AFO_bottom_side_withoutbracket,"</location>\n"])
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
                                <PathWrap name="pathwrap_0">
                                    <!--A WrapObject that this PathWrap interacts with.-->
                                    <wrap_object>foot_r_calcn</wrap_object>
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
                    AFO_length_side_withoutbracket='%.8f' %(AFO_length_side[k1])
                    f_w.writelines(["					<resting_length>",AFO_length_side_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                    f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude_side),"</pcsa_force>\n"])
                    f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                    <SimmSpline name="force_length_curve">\n'''])
                    f_w.writelines(['''                    					<x>'''])
                    for j in range (len(AFO_F_L_side[0])):
                        f_w.write(str(AFO_F_L_side[0][j]))
                        f_w.write(' ')
                    f_w.writelines(['''</x>
                                        <y>'''])
                    for m in range (len(AFO_F_L_side[1])):
                        f_w.write(str(AFO_F_L_side[1][m]))
                        f_w.write(' ')
                    f_w.writelines(['''</y>
                    </SimmSpline>
                </Ligament>\n'''])
                for k2 in range (len(AFO_top_tibial_front)):
                    f_w.writelines(['				<Ligament name="orthosis_front_',str(k2+1),'_r">',"\n"])
                    f_w.writelines(['''					<!--Flag indicating whether the force is applied or not. If true the forceis applied to the MultibodySystem otherwise the force is not applied.NOTE: Prior to OpenSim 4.0, this behavior was controlled by the 'isDisabled' property, where 'true' meant that force was not being applied. Thus, if 'isDisabled' is true, then 'appliesForce` is false.-->
                    <appliesForce>true</appliesForce>
                    <!--the set of points defining the path of the ligament-->
                    <GeometryPath name="geometrypath">
                        <!--The set of points defining the path-->
                        <PathPointSet>
                            <objects>\n'''])
                    f_w.writelines(['								<PathPoint name="orthosis_front_',str(k2+1),'_r-P1">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/tibia_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_top_front_withoutbracket='%.8f %.8f %.8f' %(AFO_top_tibial_front[k2,0],AFO_top_tibial_front[k2,1],AFO_top_tibial_front[k2,2])
                    f_w.writelines(["									<location>",AFO_top_front_withoutbracket,"</location>\n","								</PathPoint>\n"])
                    f_w.writelines(['								<PathPoint name="orthosis_front_',str(k2+1),'_r-P2">',"\n"])
                    f_w.writelines(['''									<!--Path to a Component that satisfies the Socket 'parent_frame' of type PhysicalFrame (description: The frame in which this path point is defined.).-->
                                    <socket_parent_frame>/bodyset/calcn_r</socket_parent_frame>
                                    <!--The fixed location of the path point expressed in its parent frame.-->\n'''])
                    AFO_bottom_front_withoutbracket='%.8f %.8f %.8f' %(AFO_bottom_calcn_front[k2,0],AFO_bottom_calcn_front[k2,1],AFO_bottom_calcn_front[k2,2])
                    f_w.writelines(["									<location>",AFO_bottom_front_withoutbracket,"</location>\n"])
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
                                <PathWrap name="pathwrap_0">
                                    <!--A WrapObject that this PathWrap interacts with.-->
                                    <wrap_object>foot_r_calcn</wrap_object>
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
                    AFO_length_front_withoutbracket='%.8f' %(AFO_length_front[k2])
                    f_w.writelines(["					<resting_length>",AFO_length_front_withoutbracket,"</resting_length>\n","					<!--force magnitude that scales the force-length curve-->\n"])
                    f_w.writelines(["					<pcsa_force>",str(AFO_Fmagnitude_front),"</pcsa_force>\n"])
                    f_w.writelines(['''					<!--Function representing the force-length behavior of the ligament-->
                                    <SimmSpline name="force_length_curve">\n'''])
                    f_w.writelines(['''                    					<x>'''])
                    for j in range (len(AFO_F_L_front[0])):
                        f_w.write(str(AFO_F_L_front[0][j]))
                        f_w.write(' ')
                    f_w.writelines(['''</x>
                                        <y>'''])
                    for m in range (len(AFO_F_L_front[1])):
                        f_w.write(str(AFO_F_L_front[1][m]))
                        f_w.write(' ')
                    f_w.writelines(['''</y>
                    </SimmSpline>
                </Ligament>\n'''])
                f_w.writelines(['''			</objects>\n'''])
                f_w.write(line)
            else:
                f_w.write(line)
#
