import os
import pathlib
import re
import shutil

import pandas as pd


def check_Directory_Exist(path):
    basename = os.path.basename(path)
    if basename != "":
        dir_path = os.path.dirname(os.path.abspath(path))
    elif basename == "":
        dir_path = path
    else:
        print("path is not path or dir")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return path


def concat_Directory_DataFrame(file_dir, pattern):
    alert_report_All = []
    for f in os.listdir(file_dir):
        if re.fullmatch(pattern, f):
            file_path = os.path.join(file_dir, f)
            alert_report_country = pd.read_csv(file_path)

            alert_report_All.append(alert_report_country)

    alert_report_All = pd.concat(alert_report_All, axis=0)
    return alert_report_All


def copy_File_2Folder(file_path, destination_dir):
    _ = shutil.copy(file_path, destination_dir)


def move_File_2Folder(file_path, destination_dir):
    if os.path.isfile(file_path):
        shutil.copy2(file_path, destination_dir)
        os.remove(file_path)
    else:
        shutil.move(file_path, destination_dir)
