# Requirements:
#     1. Auto detect SD card
#     2. copy all .arw files in DCIM folder
#     3. create folder with directory on desktop 'C:\Users\user\Desktop\shutterpresso-{date}' and paste all .arw files
#     4. when the task is done, print 'Done'

# Additional Requirements:
#     1. convert .arw file to .jpg
#     2. multi-threading of the program according to the number of .arw files


import os
import shutil
from datetime import datetime
import psutil
import time
from sys import platform

# default directory for mac
default_directory_mac = ["Macintosh HD"]


def get_current_status():
    print("Getting current directory: ")
    if platform == "darwin":
        current_directory = os.listdir("/Volumes/")
    elif platform == "win32":
        # get all the drives in windows system(ex. C:, D:, E:)
        drives = []
        for partition in psutil.disk_partitions():
            drives.append(partition.device)
        print("Detected drives: ", drives) # DEBUG
        return drives



    print("Default detected directory: ", current_directory)  # DEBUG

# detects the sd card and returns the directory
def auto_detect_sd_card():
    if platform == "darwin":
        arr = os.listdir("/Volumes/")
        result = [x for x in arr if x not in default_directory_mac]
        return "/Volumes/" + result[0]
    elif platform == "win32":
        for partition in psutil.disk_partitions():
            if "removable" in partition.opts:
                print("DEBUG : detected sd card : ", partition.device) # DEBUG
                return partition.device
            
    return

    


# create folder with directory on desktop 'C:\Users\user\Desktop\shutterpresso-{date}' and paste all .arw files
# TODO : create the folder with the identificatin of each photographer

def create_shutterpresso_dir():
    print("Start creating directory for shutterpresso")  # DEBUG

    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    shutterpresso_dir = os.path.join(desktop_dir, "shutterpresso")
    date = datetime.now().strftime("%Y-%m-%d")
    date = date[2:10]

    shutterpresso_dir = shutterpresso_dir + "_" + str(date)

    # if the directory already exists, create a new one with a number at the end
    if os.path.exists(shutterpresso_dir):
        count = 1
        while os.path.exists(shutterpresso_dir + "_" + str(count)):
            count += 1
        os.mkdir(shutterpresso_dir + "_" + str(count))
        return shutterpresso_dir + "_" + str(count)
    else:
        os.mkdir(shutterpresso_dir)

    # if the directory does not exist, create one
    print("DEBUG : the directory has been created : ", shutterpresso_dir)  # DEBUG
    return shutterpresso_dir


# copy files to the shutterpresso folder
def copy_files_to_shutterpresso_dir(sd_card_dir, shutterpresso_dir):
    # copy all .arw files in DCIM folder
    DCIM_dir = os.path.join(str(sd_card_dir), "DCIM")
    print("DEBUG : DCIM_dir : ", DCIM_dir)
    if not os.path.exists(DCIM_dir):
        print("ERROR : DCIM_dir does not exist")
        return

    print("DEBUG : DCIM directory detected ", DCIM_dir)  # DEBUG

    files_in_DCIM = os.listdir(DCIM_dir)

    for file in files_in_DCIM:
        if file.endswith(".arw"):
            # copy file to desktop
            print("DEBUG : copying file : ", file, "to ", shutterpresso_dir)  # DEBUG
            shutil.copy(os.path.join(DCIM_dir, file), shutterpresso_dir)

    # when the task is done, print 'Done'
    print("Done")


def main():
    get_current_status()
    # idle the program until sd card is inserted
    sd_card_dir = ""
    print("Start auto detecting sd card")  # DEBUG
    while True:
        sd_card_dir = auto_detect_sd_card()
        if sd_card_dir != None:
            print("Detected directory is ", sd_card_dir) # DEBUG
            break
        
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"Cpu usage: {cpu_percent}%")
        time.sleep(1)

    # sd_card_dir = auto_detect_sd_card()
    shutterpresso_dir = create_shutterpresso_dir()

    copy_files_to_shutterpresso_dir(sd_card_dir, shutterpresso_dir)

    # go back to while loop
    # main()


if __name__ == "__main__":
    main()
