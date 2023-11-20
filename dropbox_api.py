import dropbox
import contextlib
import os
import time


def connect_to_dropbox(access_token):
    try:
        dbx = dropbox.Dropbox(access_token)
        print("Connected to Dropbox successfully")
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


def upload_files(dbx, local_path):
    dropbox_path = "/testing/"  # TODO: Will be updated

    file_list = os.listdir(local_path)

    for file in file_list:
        if file.endswith(".arw") or file.endswith(".ARW") and not file.startswith("."):
            fullname = os.path.join(local_path, file)
            print("DEBUG - found file ", fullname)

            with open(fullname, "rb") as f:
                print("uploading ", fullname, "with", dropbox_path + file)
                try:
                    dbx.files_upload(
                        f.read(),
                        dropbox_path + file,
                        mode=dropbox.files.WriteMode.overwrite,
                    )

                except dropbox.exceptions.ApiError as e:
                    print("Error on uploading file", file)


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print("Total elapsed time for %s: %.3f" % (message, t1 - t0))
