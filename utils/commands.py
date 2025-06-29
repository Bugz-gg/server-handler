import os


def get_saves_list():
    ls = []
    for filename in os.listdir("/opt/factorio/saves/"):
        ls.append(filename[:-4])
    return ls
