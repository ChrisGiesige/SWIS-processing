import numpy as np
import os
import shutil
import cv2 as cv
import glob
import sys
import json

data = "D:/calfire_2020/Sorted_Fires/"

###########################################################################
# Walk through each folder in the directory using os.walk, grab the name...
# ...of the fire and the flight and match them.
# Put them into a list and save the list as a json file
# So Eric you can skip this section
#------------------------------------------------------------------------- 
organized = {}
fireflights = {}
fires_list = []

for root, folders, files in os.walk(r'D:\calfire_2020\Sorted_Fires'):
    splitter = root.split(os.sep)
    
    if len(splitter) < 6:
        continue
    
    zone = splitter[3]
    fire = splitter[4]
    flight = splitter[5]
    
    if fire not in organized:
        organized[fire] = {}
        
    organized[fire][flight] = {
        "zone": zone
    }
    
    if fire not in fireflights:
        fireflights[fire] = set()
    
    # fireflights[fire].add(flight)
    
    if [fire, flight] not in fires_list:
        fires_list.append([fire, flight])

json_list = json.dumps(fires_list, indent=4)    
with open("calfire_fire_list.json", "w") as outfile:
    outfile.write(json_list)


############################################################################
# Open the json file that contains a list of each flight matched with the...
# ...fire it belongs to.
# Link to the organized directory where the organized data will be stored
# If a directory containing the fire name has not yet been created in...
# ...the organized directory create one.
# Walk through the unorganized database, check if the last index of the...
# ...root matches a flight in the list of flights from the json file...
# ...and if it does match grab the name of the fire associated with that...
# ...flight and copy that folder into the directory of the fire in the...
# ...organized database.
#--------------------------------------------------------------------------


j_file = open('calfire_fire_list.json')    
calfire_list = json.load(j_file)
organized_path = "/mdata/calfire_2020_organized"

sorted_fire_list = []

for firename in calfire_list:
    path = os.path.join(organized_path, firename[0])
    if not os.path.exists(path):
        os.makedirs(path)
    
for root, folders, files in os.walk(r'/mdata/calfire_2020'):
    splitter = root.split(os.sep)
    last_index = splitter[-1]

    for i in calfire_list:
        if last_index == i[1]:
            sorted_fire_list.append([i[0], last_index])
            path = os.path.join(organized_path, i[0])
            new_path = os.path.join(path, i[1])
            
            if not os.path.exists(new_path):
                copy_dir = shutil.copytree(root, new_path)
        