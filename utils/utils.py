import numpy as np
import requests
import sys
from tqdm.auto import tqdm
import zipfile
import os

"""
OS Functions
"""
def create_and_verify(*args):
    full_path = os.path.join(*args)
    exists = os.path.exists(full_path)
    if exists:
        return full_path
    else:
        raise FileNotFoundError("La ruta no existe")

def read_listdir(dir_):
    listdir = os.listdir(dir_)
    full_dirs = []
    for d in listdir:
        full_dir = create_and_verify(dir_, d)
        full_dirs.append(full_dir)
    return np.sort(full_dirs)

"""
Miscellaneous Functions
"""
def download_content(url, filename, chnksz=1000, zip=False):
    try:
        r = requests.get(url, stream=True)
    except Exception as e:
        print("Error de conexión con el servidor")
        sys.exit()
        
    with open(filename, "wb") as f:
        
        try:
            total = int(np.ceil(int(r.headers.get("content-length"))/chnksz))
        except:
            total = 0

        gen = r.iter_content(chunk_size=chnksz)

        for pkg in tqdm(gen, total=total, unit="KB"):
            f.write(pkg)

        f.close()
        r.close()
    
    if zip:
        with zipfile.ZipFile(filename, "r") as zfile:
            print("\nExtrayedo Zip File...")
            zfile.extractall()
            print("Eliminando Zip File...")
            os.remove(filename)
    return