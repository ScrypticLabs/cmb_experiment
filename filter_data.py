import os
import shutil

def check_for(filepath, keyword):
    with open(filepath) as f:
        for line in f.readlines():
            if keyword in line.split(" ") or keyword+"\n" in line.split(" "):
                return True
    return False

def move_file(origin, destination):
    shutil.move(origin, destination)
            
def move_data(root, id):
    for file in os.listdir(root):
        if check_for(root+"/"+file, "calibration"):
            move_file(root+"/"+file, os.getcwd()+"/datasets/data_week_1/calibration/"+id+"/"+file)
        elif check_for(root+"/"+file, "pizza"):
            move_file(root+"/"+file, os.getcwd()+"/datasets/data_week_1/sky_dip_pizza/"+id+"/"+file)
        else:
            move_file(root+"/"+file, os.getcwd()+"/datasets/data_week_1/sky_dip/"+id+"/"+file)
    
if __name__ == "__main__":
    # move_data(root=os.getcwd()+"/datasets/spring2020_week_2_trial_1", id="1")
    # move_data(root=os.getcwd()+"/datasets/spring2020_week_2_trial_2", id="2")
    move_data(root=os.getcwd()+"/datasets/spring2020_1", id="1")
    move_data(root=os.getcwd()+"/datasets/spring2020_2", id="2")
    move_data(root=os.getcwd()+"/datasets/spring2020_3", id="3")
