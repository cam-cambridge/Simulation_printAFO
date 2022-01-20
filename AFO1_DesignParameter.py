import os
import math
import numpy as np
import AFO9_MeshMechanics
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Define the design parameters for the AFO, including the fixed parameters and design varaibels
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Fixed parameters
AFO_bottom_center=[0, 0, 0]
AFO_cylinder_radius=0.0365
AFO_height=0.1
Platform_inclination=[25, 0, 0]
AFO_Fmagnitude=1

def AFODesignParameter(DesignVariables, tibial_center, calcn_center, talus_center):
    # Input:        (1)  Input_directory: the folder that include the AFO input design parameter file - AFO input.txt
    #                  (2)  Input_file: the text file including the design parameters of AFO: AFO input.txt
    #                  (3,4,5) tibial_center, calcn_center, tabuls_center: The Global coordinates of the tibial, calcn and tabuls centers
    # Output:    (1)  AFO_representation: the local coordinates of the two endpoints for the AFO strips
    #                 (2)   AFO_material: the force magnitude and force-length relationship for the AFO material
    #                 (3)  Platform_inclination: the inclination of the platform
    # Get the full path of the directory and .txt file for the input parameters

    global Platform_inclination, AFO_Fmagnitude # Fixed parameters_global Variables
    [AFO_bottom_location, AFO_strap_orientations, theta_0_values, n_elements]=DesignVariables  # Design variables
    AFO_FLrelationship=AFO9_MeshMechanics.MeshMechanics(AFO_strap_orientations, theta_0_values, n_elements)
    AFO_material=[AFO_Fmagnitude, AFO_FLrelationship]
    AFO_representation=AFORepresentation(DesignVariables, tibial_center, calcn_center, talus_center)
    Platform_inclination=Platform_inclination
    return AFO_representation, AFO_material, Platform_inclination

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Create the endpoints matrixes for the AFO stripes in global and local coordinate systems (as input to develop AFO in the musculoskeletal model)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def AFORepresentation(DesignVariables, tibial_center, calcn_center, talus_center):
    # Input:       (1)   All the design parameters collected from the AFO input file - AFO design.txt
    # Output:    (2)   The coordinates values of endpoints of AFO strips in global and local coordinate systems:
    #                         (2.1)    AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    #                         (2.2)    AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
    #                         (2.3)    AFO_length=[AFO_length_side, AFO_length_front]
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    global AFO_bottom_center, AFO_height
    [AFO_bottom_location, AFO_strap_orientations, theta_0_values, n_elements]=DesignVariables    # Design variables

    # The locations of the centers of the AFO cross sections at top and bottom
    AFO_bottom_center_global=np.array(talus_center)+np.array(AFO_bottom_center)
    AFO_top_center_global=np.array(talus_center)+np.array(AFO_bottom_center)+np.array([0, AFO_height, 0])
    AFO_bottom=AFO_top=AFO_strap_length=[]
    for i in range (len(AFO_bottom_location)):
        # The coordinates of the endpoint at the AFO bottom in the global CS
        bottom_endpoint_angle=AFO_bottom_location[i]*math.pi/180
        x_bottom=AFO_bottom_center_global[0]+math.cos(bottom_endpoint_angle)*AFO_cylinder_radius
        y_bottom=AFO_bottom_center_global[1]
        z_bottom=AFO_bottom_center_global[2]+math.sin(bottom_endpoint_angle)*AFO_cylinder_radius
        AFO_bottom=np.append(AFO_bottom, np.array([x_bottom, y_bottom, z_bottom]))
        # The coordinates of the endpoint at the AFO top in the global CS
        top_endpoint_angle=bottom_endpoint_angle+AFO_height*math.tan(AFO_strap_orientations[i]/180*math.pi)/AFO_cylinder_radius
        x_top=AFO_top_center_global[0]+math.cos(top_endpoint_angle)*AFO_cylinder_radius
        y_top=AFO_top_center_global[1]
        z_top=AFO_top_center_global[2]+math.sin(top_endpoint_angle)*AFO_cylinder_radius
        AFO_top=np.append(AFO_top, np.array([x_top, y_top, z_top]))
        # The length of the AFO stripes
        AFO_strap_length_T=AFO_height/(math.cos(AFO_strap_orientations[i]*math.pi/180))
        AFO_strap_length=np.append(AFO_strap_length, AFO_strap_length_T)
    # Transfer the endpoints of the AFO into 3D matrixes
    AFO_top=AFO_top.reshape(-1,3)
    AFO_bottom=AFO_bottom.reshape(-1,3)
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Transfer the endpoints of AFO strips from global coordinate system to local coordinate systems
    # The Global coordinates of the tibial center and calcn center for the drop landing MBD model in position 0:
             # tibial_center = np.array([-0.07520, -0.46192, 0.0835])                                                                                      # tibial center coordinates in MBD model in global coordinate system
             # calcn_center = np.array([-0.12397, -0.93387, 0.09142])                                                                                    # calcn center coordinates in MBD model in global coordinate system
    #  The Global coordinates of the tibial center and calcn center for the gait MBD model in RRA model:
             # tibial_center = np.aray([-0.06850, 0.474615, 0.09158])                                                                        # The Global coordinates for the right tibial center
             # calcn_center = np.array([-0.13574, -0.05465, 0.10344])                                                                      # The Global coordinates for the right calcn center
    [AFO_top_local, AFO_bottom_local, AFO_strap_length]=MBDGlobalToLocal(AFO_top, AFO_bottom, AFO_strap_length, tibial_center, calcn_center)
    return AFO_top_local, AFO_bottom_local, AFO_strap_length

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Change the coordinate values of the endpoints from Global coordinate system to Locol coordinate system
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def MBDGlobalToLocal(AFO_top, AFO_bottom, AFO_length, tibial_center, calcn_center):
    #   Input:           (1 & 2)  AFO_top & AFO_bottom:           the matrix of endpoints on the top of the AFO in the Global coordinate system
    #                        (3)        AFO _length:                               the length of the AFO
    #                        (4 & 5)  tibial_center & calcn_center:    the coordinate values of the body centers for the tibial and calcn bone
    #  Output:         (1)         AFO_top_tibial:                         the matrix representing coordinate values of the points on the top of the AFO strips in tibial local coordinate system
    #                       (2)         AFO_bottom_calcn:                   the matrix representing coordinate values of the points at the bottom of the AFO strips in the calcn local coordinate system
    #                       (3)         AFO_length:                               the length of the AFO
    import numpy as np
    # The tibial local coordinate systems
    # tibial_center=np.array([-0.0752, -0.46192,0.0835])
    tibial_x=np.array([1,0,0])
    tibial_y=np.array([0,1,0])
    tibial_z=np.array([0,0,1])
    tibial_vector=np.array([tibial_x,tibial_y,tibial_z])

    # The calcn local coordinate systems
    # calcn_center=np.array([-0.12397,-0.93387,0.09142])
    calcn_x=np.array([1,0,0])
    calcn_y=np.array([0,1,0])
    calcn_z=np.array([0,0,1])
    calcn_vector=np.array([calcn_x,calcn_y,calcn_z])

    # The transformation from global coordinate system to the local coordiante systems
    AFO_top_tibial=np.array(transformation(AFO_top,tibial_center,tibial_vector))
    AFO_bottom_calcn=np.array(transformation(AFO_bottom,calcn_center,calcn_vector))
    return AFO_top_tibial, AFO_bottom_calcn, AFO_length

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Matrix operations: Dot，Cross and Normalization
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class MatrixOperation:
    # input arguments for Dot and Cross: two matrix, i.e. M1=[1.0,2.0,3.0],M2=[2.0,4.0,7.0]
    # input argument for Normalization: one matrix, i.e. M=[1,2,3]
    def Dot(M1,M2):
        return M1[0]*M2[0]+M1[1]*M2[1]+M1[2]*M2[2]
    def Cross(M1,M2):
        return [M1[1]*M2[2]-M1[2]*M2[1],-(M1[0]*M2[2]-M1[2]*M2[0]),M1[0]*M2[1]-M1[1]*M2[0]]
    def Norm(M):
        sqrt=pow((pow(M[0],2)+pow(M[1],2)+pow(M[2],2)),0.5)
        return sqrt
    def Sub(M1,M2):
        M=[]
        T=[]
        for i in range(len(M1)):
            for j in range(len(M1[0])):
                T.append(M1[i][j]-M2[i][j])
            M.append(T)
            T=[]
        return M

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Matrix transformation between two coordinate systems
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def transformation(M_origin,Coord_local_origin,Coord_local_vector):
    # input arguments: two matrix: M1(n*4 matrix): the original matrix,
                             # M2(1*3 matrix): the origin of the new (local) coordinate system
                             # M3(3*3 matrix): the x,y,z vectors of the new (local) coordinate system
        x_global=[1,0,0]
        y_global=[0,1,0]
        z_global=[0,0,1]
        x_local=Coord_local_vector[0]
        y_local=Coord_local_vector[1]
        z_local=Coord_local_vector[2]
        MO=MatrixOperation
        cos_x_local_x_global=MO.Dot(x_local,x_global)/(MO.Norm(x_local)*MO.Norm(x_global))
        cos_x_local_y_global=MO.Dot(x_local,y_global)/(MO.Norm(x_local)*MO.Norm(y_global))
        cos_x_local_z_global=MO.Dot(x_local,z_global)/(MO.Norm(x_local)*MO.Norm(z_global))

        cos_y_local_x_global=MO.Dot(y_local,x_global)/(MO.Norm(y_local)*MO.Norm(x_global))
        cos_y_local_y_global=MO.Dot(y_local,y_global)/(MO.Norm(y_local)*MO.Norm(y_global))
        cos_y_local_z_global=MO.Dot(y_local,z_global)/(MO.Norm(y_local)*MO.Norm(z_global))

        cos_z_local_x_global=MO.Dot(z_local,x_global)/(MO.Norm(z_local)*MO.Norm(x_global))
        cos_z_local_y_global=MO.Dot(z_local,y_global)/(MO.Norm(z_local)*MO.Norm(y_global))
        cos_z_local_z_global=MO.Dot(z_local,z_global)/(MO.Norm(z_local)*MO.Norm(z_global))
        M_new=[]
        T=[]
        M1=M_origin
        M2=Coord_local_origin
        for i in range(len(M1)):
            T=[(M1[i][0]-M2[0])*cos_x_local_x_global+(M1[i][1]-M2[1])*cos_x_local_y_global+(M1[i][2]-M2[2])*cos_x_local_z_global,
                (M1[i][0]-M2[0])*cos_y_local_x_global+(M1[i][1]-M2[1])*cos_y_local_y_global+(M1[i][2]-M2[2])*cos_y_local_z_global,
                (M1[i][0]-M2[0])*cos_z_local_x_global+(M1[i][1]-M2[1])*cos_z_local_y_global+(M1[i][2]-M2[2])*cos_z_local_z_global
                ]
            M_new.append(T)
            T=[]
        return M_new


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Previous old parameters
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def AFORepresentation_20210708(DesignParameter):                                                                                               # The old code before 20210708
    # Input:       (1)   All the design parameters collected from the AFO input file - AFO design.txt
    # Output:    (2)   The coordinates values of endpoints of AFO strips in global and local coordinate systems:
    #                         (2.1)    AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    #                         (2.2)    AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
    #                         (2.3)    AFO_length=[AFO_length_side, AFO_length_front]
    import math
    import numpy as np
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The design parameters for AFO in the MBD model, collected from the AFO input.txt file
    wrapCylinder_location=DesignParameter[0]
    wrapCylinder_radius=DesignParameter[1]
    wrapEllipsoid_location=DesignParameter[2]
    wrapEllipsoid_dim=DesignParameter[3]
    wrapEllipsoid_Orinentation=DesignParameter[4]
    AFO_side_top_iniPosAngle=DesignParameter[5]                                  # The initial position of the AFO strip in two sides of the foot, the position can be determined using ellipse angle
    AFO_side_top_rangeAngle=DesignParameter[6]
    AFO_side_bottom_iniPosAngle=DesignParameter[7]
    AFO_side_bottom_rangeAngle=DesignParameter[8]                                                       # The width of the AFO strip in two sides of the foot, is determined using ellipse angle
    AFO_front_top_iniPosAngle=DesignParameter[9]                                              # The initial position of the AFO strip in front sides of the foot, the position can be determined using ellipse angle
    AFO_front_top_rangeAngle=DesignParameter[10]
    AFO_front_bottom_iniPosAngle=DesignParameter[11]
    AFO_front_bottom_rangeAngle=DesignParameter[12]                                                      # The width of the AFO strip in front sides of the foot, is determined using ellipse angle
    AFO_height=DesignParameter[13]
    num_side=DesignParameter[14]                                                                               # The number of AFO strips in two sides of the foot
    num_front=DesignParameter[15]                                                                              # The number of AFO strips in front side of the foot
    # Transfer the AFO design parameters definition from angle to the radians
    [AFO_side_top_iniPosAngle, AFO_side_top_rangeAngle]=[AFO_side_top_iniPosAngle/180*math.pi, AFO_side_top_rangeAngle/180*math.pi]
    [AFO_side_bottom_iniPosAngle, AFO_side_bottom_rangeAngle]=[AFO_side_bottom_iniPosAngle/180*math.pi, AFO_side_bottom_rangeAngle/180*math.pi]
    [AFO_front_top_iniPosAngle, AFO_front_top_rangeAngle]=[AFO_front_top_iniPosAngle/180*math.pi, AFO_front_top_rangeAngle/180*math.pi]
    [AFO_front_bottom_iniPosAngle, AFO_front_bottom_rangeAngle]=[AFO_front_bottom_iniPosAngle/180*math.pi, AFO_front_bottom_rangeAngle/180*math.pi]

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The ellipsoid wrap surface in the calcn, the AFO at the bottom (ground coordinate system)
    # The AFO on the left and right sides of the foot_bottom
    theta_wrapEllipsoid=wrapEllipsoid_Orinentation                                                     # The rotation of the ellipsoid wrap surface about calcn coordinate system
    location_wrapEllipsoid=wrapEllipsoid_location                                                       # The location of the origin of the ellipsoid wrap surface on the ground coordinate system
    dim_wrapEllipsoid=wrapEllipsoid_dim                                                                   # The dimensions of the ellipsoid wrap surface
    AFO_bottomside_left=AFO_bottomside_right=[]
    for i in range (int(num_side)):
        # AFO strips in the left side of the foot_bottom
        x_left=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos(AFO_side_bottom_iniPosAngle+AFO_side_bottom_rangeAngle/num_side*i)
        y_left=location_wrapEllipsoid[1]
        z_left=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin(AFO_side_bottom_iniPosAngle+AFO_side_bottom_rangeAngle/num_side*i)
        AFO_bottomside_left=np.append(AFO_bottomside_left, np.array([x_left,y_left,z_left]))
        #AFO strips in the right side of the foot_bottom
        #x_right=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos((2*math.pi-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        x_right=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos((-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        y_right=location_wrapEllipsoid[1]
        #z_right=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin((2*math.pi-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        z_right=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin((-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        AFO_bottomside_right=np.append(AFO_bottomside_right, np.array([x_right,y_right,z_right]))
    AFO_bottomside_left=AFO_bottomside_left.reshape(-1,3)
    AFO_bottomside_right=AFO_bottomside_right.reshape(-1,3)

    # The AFO on the front sides of the foot_bottom
    AFO_bottomfront_left=AFO_bottomfront_right=[]
    for i in range (num_front):
        # AFO strips in the left front of the foot_bottom
        x_left=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos(AFO_front_bottom_iniPosAngle+AFO_front_bottom_rangeAngle/num_front*i)
        y_left=location_wrapEllipsoid[1]
        z_left=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin(AFO_front_bottom_iniPosAngle+AFO_front_bottom_rangeAngle/num_front*i)
        AFO_bottomfront_left=np.append(AFO_bottomfront_left, np.array([x_left,y_left,z_left]))
        #AFO strips in the right front of the foot_bottom
        x_right=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos((2*math.pi-AFO_front_bottom_iniPosAngle)-AFO_front_bottom_rangeAngle/num_front*i)
        y_right=location_wrapEllipsoid[1]
        z_right=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin((2*math.pi-AFO_front_bottom_iniPosAngle)-AFO_front_bottom_rangeAngle/num_front*i)
        AFO_bottomfront_right=np.append(AFO_bottomfront_right, np.array([x_right,y_right,z_right]))
    AFO_bottomfront_left=AFO_bottomfront_left.reshape(-1,3)
    AFO_bottomfront_right=AFO_bottomfront_right.reshape(-1,3)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The cylinder wrap surface in the tibia, the AFO at the top (ground coordinate system)
    #location_wrapCylinder=np.array([-0.0084,-0.4657,0.0067])                            # The center of the circle at the bottom of the wrap Cylinder (tibia coordinate system)
    location_wrapCylinder=wrapCylinder_location                                                  # The center of teh circle at the bottome in ground coordinate system
    radius=wrapCylinder_radius                                                                                # The radius of the circle for the wrap Cylinder
    AFO_height=AFO_height                                                                                     # The length of the AFO length
    # The AFO on the left and right sides of the foot_top
    AFO_topside_left=AFO_topside_right=[]
    for i in range (num_side):
        # AFO strips in the left side of the foot_top
        x_left=location_wrapCylinder[0]+radius*math.cos(AFO_side_top_iniPosAngle+AFO_side_top_rangeAngle/num_side*i)
        y_left=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_left=location_wrapCylinder[2]+radius*math.sin(AFO_side_top_iniPosAngle+AFO_side_top_rangeAngle/num_side*i)
        AFO_topside_left=np.append(AFO_topside_left, np.array([x_left,y_left,z_left]))
        # AFO strips in the right side of the foot_top
        x_right=location_wrapCylinder[0]+radius*math.cos((2*math.pi-AFO_side_top_iniPosAngle)-AFO_side_top_rangeAngle/num_side*i)
        y_right=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_right=location_wrapCylinder[2]+radius*math.sin((2*math.pi-AFO_side_top_iniPosAngle)-AFO_side_top_rangeAngle/num_side*i)
        AFO_topside_right=np.append(AFO_topside_right, np.array([x_right,y_right,z_right]))
    AFO_topside_left=AFO_topside_left.reshape(-1,3)
    AFO_topside_right=AFO_topside_right.reshape(-1,3)

    # The AFO on the front sides of the foot_top
    AFO_topfront_left=AFO_topfront_right=[]
    for i in range (num_front):
        # AFO strips in the left side of the foot_top
        x_left=location_wrapCylinder[0]+radius*math.cos(AFO_front_top_iniPosAngle+AFO_front_top_rangeAngle/num_front*i)
        y_right=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_left=location_wrapCylinder[2]+radius*math.sin(AFO_front_top_iniPosAngle+AFO_front_top_rangeAngle/num_front*i)
        AFO_topfront_left=np.append(AFO_topfront_left, np.array([x_left,y_left,z_left]))
        # AFO strips in the right side of the foot_top
        x_right=location_wrapCylinder[0]+radius*math.cos((2*math.pi-AFO_front_top_iniPosAngle)-AFO_front_top_rangeAngle/num_front*i)
        y_left=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_right=location_wrapCylinder[2]+radius*math.sin((2*math.pi-AFO_front_top_iniPosAngle)-AFO_front_top_rangeAngle/num_front*i)
        AFO_topfront_right=np.append(AFO_topfront_right, np.array([x_right,y_right,z_right]))
    AFO_topfront_left=AFO_topfront_left.reshape(-1,3)
    AFO_topfront_right=AFO_topfront_right.reshape(-1,3)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The length of the AFO strips in right, left and front sides
    # Top surface: AFO_topside_left, AFO_topside_right, AFO_topfront_left, AFO_topfront_right
    # Bottom surface: AFO_bottomside_left, AFO_bottomside_right, AFO_bottomfront_left, AFO_bottomfront_right
    # The length of strips in AFO sides
    AFO_side_left_length=AFO_side_right_length=[]
    for i in range (num_side):
        AFO_side_left_length_T=np.sqrt(np.sum(np.square(AFO_topside_left[i]-AFO_bottomside_left[i])))
        AFO_side_left_length=np.append(AFO_side_left_length, AFO_side_left_length_T)
        AFO_side_right_length_T=np.sqrt(np.sum(np.square(AFO_topside_right[i]-AFO_bottomside_right[i])))
        AFO_side_right_length=np.append(AFO_side_right_length,AFO_side_right_length_T)
    # The length of strips in AFO front
    AFO_front_left_length=AFO_front_right_length=[]
    for i in range (num_front):
        AFO_front_left_length_T=np.sqrt(np.sum(np.square(AFO_topfront_left[i]-AFO_bottomfront_right[i])))                      # The length of AFO strip in front, top left to bottom right (top left-bottom right)
        AFO_front_left_length=np.append(AFO_front_left_length, AFO_front_left_length_T)
        AFO_front_right_length_T=np.sqrt(np.sum(np.square(AFO_topfront_right[i]-AFO_bottomfront_left[i])))                    # The length of AFO strip in front, top right to bottom left (top right-bottom left)
        AFO_front_right_length=np.append(AFO_front_right_length, AFO_front_right_length_T)

    AFO_top_global_side=np.vstack((AFO_topside_left, AFO_topside_right))
    AFO_top_global_front=np.vstack((AFO_topfront_left, AFO_topfront_right))
    AFO_bottom_global_side=np.vstack((AFO_bottomside_left, AFO_bottomside_right))
    AFO_bottom_global_front=np.vstack((AFO_bottomfront_right, AFO_bottomfront_left))
    AFO_strip_length_side=np.append(AFO_side_left_length, AFO_side_right_length)
    AFO_strip_length_front= np.append(AFO_front_left_length, AFO_front_right_length)
    AFO_strip_length_side=AFO_strip_length_side
    AFO_strip_length_front=AFO_strip_length_front

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Transfer the endpoints of AFO strips from global coordinate system to local coordinate systems
    tibial_center = np.array([-0.0752, -0.4619, 0.0835])                                                                                              # tibial center coordinates in MBD model in global coordinate system
    calcn_center = np.array([-0.1240, -0.9339, 0.0914])                                                                                             # calcn center coordinates in MBD model in global coordinate system
    # The AFO strip in the AFO side
    [AFO_top_local_side, AFO_bottom_local_side, AFO_length_side]=MBDGlobalToLocal(AFO_top_global_side, AFO_bottom_global_side, AFO_strip_length_side, tibial_center, calcn_center)
    # The AFO strip in the AFO front
    [AFO_top_local_front, AFO_bottom_local_front, AFO_length_front]=MBDGlobalToLocal(AFO_top_global_front, AFO_bottom_global_front, AFO_strip_length_front, tibial_center, calcn_center)
    # Put the AFO strips in AFO side and front together
    AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
    AFO_length=[AFO_length_side, AFO_length_front]
    return AFO_top_local, AFO_bottom_local, AFO_length

def AFORepresentation_20210714(DesignParameter):                                                                                               # The old code before 20210714
    # Input:       (1)   All the design parameters collected from the AFO input file - AFO design.txt
    # Output:    (2)   The coordinates values of endpoints of AFO strips in global and local coordinate systems:
    #                         (2.1)    AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    #                         (2.2)    AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
    #                         (2.3)    AFO_length=[AFO_length_side, AFO_length_front]
    import math
    import numpy as np
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The design parameters for AFO in the MBD model, collected from the AFO input.txt file

    tabus_GlobalCS_origin=DesignParameter[0]
    AFO_bottom_location=DesignParameter[1]
    AFO_cylinder_radius=DesignParameter[2]
    AFO_length=DesignParameter[3]
    AFO_side_num=DesignParameter[4]
    AFO_front_num=DesignParameter[5]
    AFO_lateralside_top_iniPosAngle=DesignParameter[6]
    AFO_lateralside_top_rangeAngle=DesignParameter[7]
    AFO_lateralside_orientations=DesignParameter[8]
    AFO_medialside_top_iniPosAngle=DesignParameter[9]
    AFO_medialside_top_rangeAngle=DesignParameter[10]
    AFO_medialside_orientations=DesignParameter[11]
    AFO_lateralfront_top_iniPosAngle=DesignParameter[12]
    AFO_lateralfront_top_rangeAngle=DesignParameter[13]
    AFO_lateralfront_orientations=DesignParameter[14]
    AFO_medialfront_top_iniPosAngle=DesignParameter[15]
    AFO_medialfront_top_rangeAngle=DesignParameter[16]
    AFO_medialfront_orientations=DesignParameter[17]

    AFO_top_center=np.array(tabus_GlobalCS_origin)+np.array(AFO_bottom_location)+np.array([0, AFO_length, 0])
    AFO_bottom_center=np.array(tabus_GlobalCS_origin)+np.array(AFO_bottom_location)
    def AFOendpoints (AFO_side_num, iniPosAngle, rangeAngle, AFO_stripe_orientations):
        AFO_top=AFO_bottom=AFO_stripe_length=[]
        for i in range (int(AFO_side_num)):
            # The endpoints for the top of the AFO
            top_endpoint_angle=(iniPosAngle+i*rangeAngle/(AFO_side_num-1))/180*math.pi
            x_top=AFO_top_center[0]+math.cos(top_endpoint_angle)*AFO_cylinder_radius
            y_top=AFO_top_center[1]
            z_top=AFO_top_center[2]+math.sin(top_endpoint_angle)*AFO_cylinder_radius
            AFO_top=np.append(AFO_top, np.array([x_top, y_top, z_top]))
            # The endpoints for the bottom of the AFO
            bottom_endpoint_angle=top_endpoint_angle+AFO_length*math.tan(AFO_stripe_orientations[i]/180*math.pi)/AFO_cylinder_radius
            x_bottom=AFO_bottom_center[0]+math.cos(bottom_endpoint_angle)*AFO_cylinder_radius
            y_bottom=AFO_bottom_center[1]
            z_bottom=AFO_bottom_center[2]+math.sin(bottom_endpoint_angle)*AFO_cylinder_radius
            AFO_bottom=np.append(AFO_bottom, np.array([x_bottom, y_bottom, z_bottom]))
            # The lengths of the AFO AFO_strip
            AFO_stripe_length_T=np.sqrt(np.sum(np.square(np.array([x_top, y_top, z_top])-np.array([x_bottom, y_bottom, z_bottom]))))
            AFO_stripe_length=np.append(AFO_stripe_length, AFO_stripe_length_T)
        AFO_top=AFO_top.reshape(-1,3)
        AFO_bottom=AFO_bottom.reshape(-1,3)
        return AFO_top, AFO_bottom, AFO_stripe_length
    [AFO_top_lateralside, AFO_bottom_lateralside, AFO_lateralside_length]=AFOendpoints(AFO_side_num, AFO_lateralside_top_iniPosAngle, AFO_lateralside_top_rangeAngle, AFO_lateralside_orientations)
    [AFO_top_medialside, AFO_bottom_medialside, AFO_medialside_length]=AFOendpoints(AFO_side_num, AFO_medialside_top_iniPosAngle, AFO_medialside_top_rangeAngle, AFO_medialside_orientations)
    [AFO_top_lateralfront, AFO_bottom_lateralfront, AFO_lateralfront_length]=AFOendpoints(AFO_front_num, AFO_lateralfront_top_iniPosAngle, AFO_lateralfront_top_rangeAngle, AFO_lateralfront_orientations)
    [AFO_top_medialfront, AFO_bottom_medialfront, AFO_medialfront_length]=AFOendpoints(AFO_front_num, AFO_medialfront_top_iniPosAngle,AFO_medialfront_top_rangeAngle, AFO_medialfront_orientations)
    # Put the lateral side and medial side of AFO stripes together, using np.vstack function
    AFO_top_global_side=np.vstack((AFO_top_lateralside, AFO_top_medialside))
    AFO_top_global_front=np.vstack((AFO_top_lateralfront, AFO_top_medialfront))
    AFO_bottom_global_side=np.vstack((AFO_bottom_lateralside, AFO_bottom_medialside))
    AFO_bottom_global_front=np.vstack((AFO_bottom_lateralfront, AFO_bottom_medialfront))
    AFO_side_length=np.append(AFO_lateralside_length, AFO_medialside_length)
    AFO_front_length=np.append(AFO_lateralfront_length, AFO_medialfront_length)
    AFO_side_length=AFO_side_length
    AFO_front_length=AFO_front_length
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Transfer the endpoints of AFO strips from global coordinate system to local coordinate systems
    tibial_center = np.array([-0.0752, -0.4619, 0.0835])                                                                                              # tibial center coordinates in MBD model in global coordinate system
    calcn_center = np.array([-0.1240, -0.9339, 0.0914])                                                                                             # calcn center coordinates in MBD model in global coordinate system
    # The AFO strip in the AFO side
    [AFO_top_local_side, AFO_bottom_local_side, AFO_length_side]=MBDGlobalToLocal(AFO_top_global_side, AFO_bottom_global_side, AFO_side_length, tibial_center, calcn_center)
    # The AFO strip in the AFO front
    [AFO_top_local_front, AFO_bottom_local_front, AFO_length_front]=MBDGlobalToLocal(AFO_top_global_front, AFO_bottom_global_front, AFO_front_length, tibial_center, calcn_center)
    # Put the AFO strips in AFO side and front together
    AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
    AFO_length=[AFO_length_side, AFO_length_front]
    return AFO_top_local, AFO_bottom_local, AFO_length
#
