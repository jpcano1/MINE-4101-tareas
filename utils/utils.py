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

def extract_file(filename):
    with zipfile.ZipFile(filename) as zfile:
        print("\nExtrayedo Zip File...")
        zfile.extractall()
        print("Eliminando Zip File...")
        os.remove(filename)
    return

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
        extract_file(filename)
    return

def download_file_from_google_drive(id_, filename, size=None,
                                    chnksz=1000, zip=False):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, filename, size=None,
                              chnksz=1000):
        with open(filename, "wb") as f:
            gen = response.iter_content(chunk_size=chnksz)
            for chunk in tqdm(gen, total=size, unit="KB"):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
            f.close()

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()    

    response = session.get(URL, params={ 'id' : id_ }, stream=True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id_, 'confirm' : token }
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, filename, size=size,
                          chnksz=chnksz)
    response.close()
    if zip:
        extract_file(filename)
    return