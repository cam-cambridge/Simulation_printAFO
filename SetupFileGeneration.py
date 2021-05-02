import os
def dircreation(path):
    folder=os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("new required folder created")
    else:
        print("-- The required folder already exists --")

def rra_setup (loop_num):
    import os
    with open ("3_Walk_rra_setup_rra1.xml", "rt") as fin:
        with open("Walk_rra_setup_rra%d.xml" %(loop_num), "wt") as fout:
            for line in fin:
                fout.write(line.replace('rra_walk_1', 'rra_walk_%d' %(loop_num))
                .replace('../Model outputs/3_RRA/Fullbodymodel_Walk_RRA1.osim', '../Model outputs/3_RRA/Fullbodymodel_Walk_RRA%d.osim' %(loop_num))
                .replace('../Model outputs/1_Scale/Fullbodymodel_Walk_Scale.osim', '../Model outputs/3_RRA/Fullbodymodel_Walk_RRA%d_modification.osim' %(loop_num-1))
                .replace('../Model outputs/3_RRA/Results_rra_1', '../Model outputs/3_RRA/Results_rra_%d' %(loop_num))
                .replace('300_rra_tasks_walk_1', '300_rra_tasks_walk_2'))

def cmc_setup(loop_num):
    with open("4_Walk_cmc_setup_template.xml","rt") as fin:
        with open("Walk_cmc_setup.xml","wt") as fout:
            for line in fin:
                fout.write(line.replace('<model_file>..</model_file>', '<model_file>../Model outputs/3_RRA/Fullbodymodel_Walk_RRA_modification_final.osim</model_file>')
                                        .replace('<results_directory>Results</results_directory>', '<results_directory>../Model outputs/4_CMC</results_directory>')
                                        .replace('<desired_kinematics_file>..</desired_kinematics_file>', '<desired_kinematics_file>../Model outputs/3_RRA/Results_rra_%d/rra_walk_%d_Kinematics_q.sto</desired_kinematics_file>'
                                                        %(loop_num, loop_num)))
