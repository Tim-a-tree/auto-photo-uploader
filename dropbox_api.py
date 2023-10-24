import dropbox
import pathlib
import dotenv
import os


def connect_to_dropbox(access_token): 
    try: 
        dbx = dropbox.Dropbox(access_token) 
        print('Connected to Dropbox successfully')
        return dbx
    except Exception as e: 
        print(str(e)) 
    
    return None

def list_files_in_folder(dbx): 
    # here dbx is an object which is obtained 
    # by connecting to dropbox via token 
    try: 
        folder_path = "/testing"
  
        # dbx object contains all functions that  
        # are required to perform actions with dropbox 
        files = dbx.files_list_folder(folder_path).entries 
        print("------------Listing Files in Folder------------ ") 


        for file in files: 
            # listing 
            print(file.name) 

    except Exception as e: 
        print(str(e)) 
  
def list_folder(dbx):
    try:
        folders = dbx.list_folder().entries
        print("------------ Listing Folders in Account -----------")

        for folder in folders:
            print(folder.name)

    except Exception as e: 
        print(str(e)) 

def upload(dbx, local_file_dir):
    dropbox_path = "" # TODO: Will be updated

    try:
        for local_file in local_file_list:
            if file.endswith(".arw") or file.endswith(".ARW"):
                local_file_path = pathlib.Path(local_file)

    
                with local_file_path.open("rb") as f:
                    dbx.files_upload(f.read(), dropbox_path)


    except Exception as e:
        print("Error on uploading file", local_file)


