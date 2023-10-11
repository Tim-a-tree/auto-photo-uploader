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
    drives = []
    if platform == "darwin":
        for a in os.listdir("/Volumes/"):
            drives.append(a)
    elif platform == "win32":
        # get all the drives in windows system(ex. C:, D:, E:)
        for partition in psutil.disk_partitions():
            drives.append(partition.device)
    print("Detected drives: ", drives) # DEBUG
    return drives


# detects the sd card and returns the directory
def auto_detect_sd_card(drives):
    while True:
         #DEBUG
        cpu_percent = psutil.cpu_percent(interval=6)
        print(f"Cpu usage: {cpu_percent}%")
        time.sleep(6)

        if platform == "darwin":
            arr = os.listdir("/Volumes/")
            if len(arr) > len(drives):
                result = [x for x in arr if x not in drives]
                return "/Volumes/" + result[0]
            else:
                drives = arr
        elif platform == "win32":
            arr = [partition.device for partition in psutil.disk_partitions()]
            print("DEBUG : arr : ", arr) # DEBUG
            if len(arr) > len(drives):
                result = [x for x in arr if x not in drives]
                print("detected sd card : ", result[0])
                return result[0]
            else:
                drives = arr
            # for partition in psutil.disk_partitions():
            #     if "removable" in partition.opts and partition.fstype != "":
            #         print("DEBUG : detected sd card : ", partition.device) # DEBUG
            #         return partition.device

    return

    


# create folder with directory on desktop 'C:\Users\user\Desktop\shutterpresso-{date}' and paste all .arw files
# TODO : create the folder with the identificatin of each photographer
# FIX: case when DCIM folder does not exists, the program still makes the copy folder 
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
    print("DCIM_dir : ", DCIM_dir)
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

    print("Done")

def main():
    drives = get_current_status()

    # idle the program until sd card is inserted
    sd_card_dir = ""
    print("Start auto detecting sd card")  # DEBUG
    sd_card_dir = auto_detect_sd_card(drives)


    shutterpresso_dir = create_shutterpresso_dir()

    copy_files_to_shutterpresso_dir(sd_card_dir, shutterpresso_dir)

    # go back to while loop
    main()


if __name__ == "__main__":
    main()
