# Requirements:
#     1. Auto detect SD card
#     2. copy all .arw files in DCIM folder
#     3. create folder with directory on desktop 'C:\Users\user\Desktop\shutterpresso-{date}' and paste all .arw files
#     4. when the task is done, print 'Done'

# Additional Requirements:
#     1. convert .arw file to .jpg
#     2. multi-threading of the program according to the number of .arw files

from dotenv import load_dotenv
import os
import shutil
from datetime import datetime
import psutil
import time
from sys import platform
import user
import dropbox_api as dba


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
    print("Detected drives: ", drives)  # DEBUG
    return drives


# detects the sd card and returns the directory
def auto_detect_sd_card(drives):
    while True:
        # DEBUG
        cpu_percent = psutil.cpu_percent(interval=2)
        print(f"Cpu usage: {cpu_percent}%")
        time.sleep(2)

        if platform == "darwin":
            arr = os.listdir("/Volumes/")
            if len(arr) > len(drives):
                result = [x for x in arr if x not in drives]
                return "/Volumes/" + result[0]
            else:
                if len(arr) < len(drives):
                    print("Updating connected devices: ", arr)  # DEBUG
                drives = arr
        elif platform == "win32":
            arr = [partition.device for partition in psutil.disk_partitions()]
            if len(arr) > len(drives):
                result = [x for x in arr if x not in drives]
                print("detected sd card : ", result[0])
                return result[0]
            else:
                drives = arr

    return


# create folder with directory on desktop 'C:\Users\user\Desktop\shutterpresso-{date}' and paste all .arw files
# FIX: case when DCIM folder does not exists, the program still makes the copy folder
def create_shutterpresso_dir(id):
    print("Start creating directory for shutterpresso")  # DEBUG

    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    shutterpresso_dir = os.path.join(desktop_dir, "shutterpresso")
    date = datetime.now().strftime("%Y-%m-%d")
    date = date[2:10]

    shutterpresso_dir = shutterpresso_dir + "_" + str(date) + "_" + str(id)

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
    print("Directory created : ", shutterpresso_dir)
    return shutterpresso_dir


# WARNING: detects the id only using first file in the list
def find_id(user_list, file):
    # detecting filename matches with the dictionary
    print("Received", user_list, file)
    for user in user_list.keys():
        print("Checking ", user)  # DEBUG
        values = user_list.get(user)
        for value in values:
            if value.lower() in file.lower():
                print("Matching: ", value.lower(), user, file.lower())  # DEBUG
                id = str(user)
                print("The SD card belongs to ", id)
                return id


# copy files to the shutterpresso folder
def copy_files_to_shutterpresso_dir(sd_card_dir, user_list):
    # copy all .arw files in DCIM folder
    DCIM_dir = os.path.join(str(sd_card_dir), "DCIM")
    print("DCIM_dir : ", DCIM_dir)
    if not os.path.exists(DCIM_dir):
        print("ERROR : DCIM_dir does not exist")
        return

    print("Start copying files to shutterpresso directory")
    files_in_DCIM = os.listdir(DCIM_dir)

    id = find_id(user_list, files_in_DCIM[0])
    shutterpresso_dir = create_shutterpresso_dir(id)
    for file in files_in_DCIM:
        if file.endswith(".arw") or file.endswith(".ARW"):
            # copy file to desktop
            print("copying file : ", file)
            shutil.copy(os.path.join(DCIM_dir, file), shutterpresso_dir)

    return shutterpresso_dir


def main():
    load_dotenv()

    drives = get_current_status()
    user_list = user.read_users()

    # idle the program until sd card is inserted
    sd_card_dir = ""
    print("Start auto detecting sd card......")
    sd_card_dir = auto_detect_sd_card(drives)

    # shutterpresso_dir = create_shutterpresso_dir()

    shutterpresso_dir = copy_files_to_shutterpresso_dir(sd_card_dir, user_list)

    # Dropbox authentication
    access_token = os.environ["ACCESS_TOKEN"]
    dbx = dba.connect_to_dropbox(access_token)

    # create a folder in dropbox
    # try:
    #     dbx.files_create_folder_v2(dbx, shutterpresso_dir)
    #     print("Folder created on Dropbox with name: ", shutterpresso_dir)

    # except dropbox.exceptions.ApiError as e:
    #     print("Error creating folder: ", e)

    # uploading to dropbox
    dba.upload_files(dbx, shutterpresso_dir)
    # go back to while loop
    main()


if __name__ == "__main__":
    main()
