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

possible_sd_card_dir = ["D:", "E:", "F:", "G:", "H:", "I:", "J:", "K:", "L:", "M:", "N:", "O:", "P:", "Q:", "R:", "S:", "T:", "U:", "V:", "W:", "X:", "Y:", "Z:"]


# detects the sd card and returns the directory
def auto_detect_sd_card():
    for dir in possible_sd_card_dir:
        if os.path.isdir(dir):
            return dir



#create folder with directory on desktop 'C:\Users\user\Desktop\shutterpresso-{date}' and paste all .arw files
def create_shutterpresso_dir():
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    shutterpresso_dir = os.path.join(desktop_dir, "shutterpresso")
    date = datetime.now().strftime("%Y/%m/%d")
    date = date[2:10]
    shutterpresso_dir = os.path.join(shutterpresso_dir, date)

    # if the directory already exists, create a new one with a number at the end
    if os.path.exists(shutterpresso_dir):
        count = 1
        while os.path.exists(shutterpresso_dir + '-' + str(count)):
            count += 1
        os.mkdir(shutterpresso_dir + '-1')
        return shutterpresso_dir + '-1'
    

    # if the directory does not exist, create one
    os.mkdir(shutterpresso_dir)
    return shutterpresso_dir



# copy files to the shutterpresso folder
def copy_files_to_shutterpresso_dir(sd_card_dir, shutterpresso_dir):
    #copy all .arw files in DCIM folder
    DCIM_dir = os.path.join(sd_card_dir, "DCIM")

    files_in_DCIM = os.listdir(DCIM_dir)

    for file in files_in_DCIM:
        if file.endswith(".arw"):
            #copy file to desktop
            shutil.copy(os.path.join(DCIM_dir, file), shutterpresso_dir)
    
    #when the task is done, print 'Done'
    print("Done")


def main():

    # idle the program until sd card is inserted
    while auto_detect_sd_card() == None:
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"Cpu usage: {cpu_percent}%")
        time.sleep(1)

    sd_card_dir = auto_detect_sd_card()
    shutterpresso_dir = create_shutterpresso_dir()    

    copy_files_to_shutterpresso_dir(sd_card_dir, shutterpresso_dir)

    # go back to while loop
    main()

if __name__ == "__main__":
    main()
    


