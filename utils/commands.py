import os
import subprocess


def get_saves_list():
    ls = []
    for filename in os.listdir("/opt/factorio/saves/"):
        ls.append(filename[:-4])
    return ls


def send_down():
    cmd = f"docker compose down"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def send_start(save_name: str):
    cmd = f"SAVE_NAME={save_name} docker compose up -d"
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)
