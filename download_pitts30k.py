
import os
import utm
import math
import shutil
from glob import glob
from tqdm import tqdm
from os.path import join

import util
import map_builder

datasets_folder = join(os.curdir, "datasets")
dataset_name = "pitts30k"
dataset_folder = join(datasets_folder, dataset_name)
raw_data_folder = join(datasets_folder, dataset_name, "raw_data")
os.makedirs(dataset_folder, exist_ok=True)
os.makedirs(raw_data_folder, exist_ok=True)
os.makedirs(join(dataset_folder, "images", "test"), exist_ok=True)

#### Database
print("Downloading database archives")
import re

raw_text = """[   ]	000.tar	2015-11-19 00:48	880M	 
[   ]	001.tar	2015-11-19 01:05	815M	 
[   ]	002.tar	2015-11-19 01:22	811M	 
[   ]	003.tar	2015-11-19 01:39	796M	 
[   ]	004.tar	2015-11-19 01:56	810M	 
[   ]	005.tar	2015-11-19 02:12	802M	 
[   ]	006.tar	2015-11-19 02:28	789M	 
[   ]	groundtruth.tar	2015-11-19 03:26	45M	 
[   ]	md5sums.txt	2020-06-08 14:28	636	 
[   ]	netvlad_v100_datasets.tar.gz	2020-08-26 13:13	2.1M	 
[   ]	pose.txt	2008-08-27 20:32	957K	 
[   ]	queries_real.tar	2015-11-19 03:43	856M	 
[   ]	readGt.m	2015-11-19 03:44	849	 
"""
# 使用正则表达式匹配方括号中的内容
file_names = re.findall(r'\[\s*\]\s+(\S+)', raw_text)
print(file_names)

urls = [f"https://data.ciirc.cvut.cz/public/projects/2015netVLAD/Pittsburgh250k/{file_name}"
        for file_name in file_names]
tars_paths = [join(raw_data_folder, f) for f in file_names]

for i, (url, tar_path) in enumerate(zip(urls, tars_paths)):
    check = tar_path.replace("PCIs_", "").replace(".tar", "")
    if os.path.exists(check):
        print(f"I see {check}, won't download {tar_path} again. ")
    else:
        print(f"{i:>3} / {len(file_names)} ) downloading {tar_path}")
        util.download_heavy_file(url, tar_path)
    try:  # Unpacking database archives
        shutil.unpack_archive(tar_path, raw_data_folder)
    except shutil.ReadError as e:
        # raise e
        print (e) # 可能不是tar，那就是正常的
        # pass  # Some tars are empty files

# 还需要自己运行format