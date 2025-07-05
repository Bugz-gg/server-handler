import os
import subprocess
import zipfile


def get_saves_list():
    ls = []
    for filename in os.listdir("/opt/factorio/saves/"):
        ls.append(filename[:-4])
    return ls


def send_down():
    cmd = f"docker compose down"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True), cmd


def send_start(save_name: str):
    cmd = f"SAVE_NAME={save_name} docker compose up -d"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True), cmd


def send_upload_factorio(save_file: zipfile.ZipFile):

    # dest_dir = '/opt/factorio/saves/'    
    # cmd = "mv /opt/factorio/saves/"
    dest_dir = './temp/'#/opt/factorio/saves/'
    save_file.extractall(dest_dir)
    return 
    # result = subprocess.run(cmd, input=save_file, capture_output=True)
    # return result, cmd
