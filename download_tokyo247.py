import config 

import os
import utm
import math
import shutil
from glob import glob
from tqdm import tqdm
from os.path import join

import util
import map_builder
import warnings

curdir = os.path.abspath(os.curdir)
datasets_folder = join(curdir, "datasets")
dataset_name = "tokyo247"
dataset_folder = join(datasets_folder, dataset_name)
raw_data_folder = join(datasets_folder, dataset_name, "raw_data")
os.makedirs(dataset_folder, exist_ok=True)
os.makedirs(raw_data_folder, exist_ok=True)
os.makedirs(join(dataset_folder, "images", "test"), exist_ok=True)

raw_data_tokyo247 = join(raw_data_folder, dataset_name)
raw_data_datasets = join(raw_data_folder, "datasets")

#### Download tokyo247.mat
# tokyo247 和 pitts 都是 relja 在 netvlad 提出的。
# tokyo247.mat 需要在 pitts30k 的文件里面下载。

pitts30k_folder = join(curdir, "datasets", 'pitts30k')
if not os.path.exists(pitts30k_folder):
    warnings.warn("You'd better download pitts_30k before you download this in order to get `tokyo247.mat`. ")
else:
    # ln -s 设计有问题，新建的软链接不能有层级结构，必须是直接的文件夹，所以得先cd进去。
    # os.chdir(raw_data_datasets)
    # os.symlink(join(pitts30k_folder, "raw_data", "datasets", "tokyo247.mat"), 
    #         "tokyo247.mat", target_is_directory=False)
    os.chdir(raw_data_folder)
    if not os.path.exists("datasets"):
        os.symlink(join(pitts30k_folder, "raw_data", "datasets"),
               "datasets", target_is_directory=True)
               

#### Download Database
print("Downloading database archives")
import re

raw_text = """[   ]	03814.tar	2016-03-17 06:20	2.9G	 
[   ]	03815.tar	2016-03-17 06:20	2.1G	 
[   ]	03816.tar	2016-03-17 06:20	2.2G	 
[   ]	03817.tar	2016-03-17 06:20	2.4G	 
[   ]	03818.tar	2016-03-17 06:21	2.5G	 
[   ]	03819.tar	2016-03-17 06:21	2.8G	 
[   ]	03820.tar	2016-03-17 06:21	2.2G	 
[   ]	03821.tar	2016-03-17 06:21	2.3G	 
[   ]	03822.tar	2016-03-17 06:21	2.5G	 
[   ]	03823.tar	2016-03-17 06:21	2.3G	 
[   ]	03824.tar	2016-03-17 06:22	2.0G	 
[   ]	03825.tar	2016-03-17 06:22	2.3G	 
[   ]	03826.tar	2016-03-17 06:22	2.3G	 
[   ]	03827.tar	2016-03-17 06:22	2.6G	 
[   ]	03828.tar	2016-03-17 06:22	2.2G	 
[   ]	03829.tar	2016-03-17 06:22	566M	 
[TXT]	Readme.txt	2018-01-29 04:36	794	 
[   ]	dbfnames.mat	2014-11-18 05:43	19M	 
[TXT]	md5sum_list.txt	2016-03-17 06:22	720	 	 
"""

raw_text = "\n".join([i  for i in raw_text.split("\n") if not i.startswith("#")])
# 使用正则表达式匹配方括号中的内容
file_names = re.findall(r'\[\s*\]\s+(\S+)', raw_text)
print(file_names)

urls = [f"{config.tokyo247_url}/{file_name}"
        for file_name in file_names]
tars_paths = [join(
    # raw_data_folder, 
    raw_data_tokyo247,
                   f) for f in file_names]

for i, (url, tar_path) in enumerate(zip(urls, tars_paths)):
    check = tar_path.replace("PCIs_", "").replace(".tar", "")
    if os.path.exists(check):
        print(f"I see {check}, won't download {tar_path} again. ")
    else:
        print(f"{i:>3} / {len(file_names)} ) downloading {tar_path}")
        util.download_heavy_file(url, tar_path)
    if tar_path.endswith(".tar"):
        try:  # Unpacking database archives
            shutil.unpack_archive(tar_path, raw_data_tokyo247)
        except shutil.ReadError as e:
            # raise e
            print (e) # 可能不是tar，那就是正常的
            # pass  # Some tars are empty files

# shutil.move(join(raw_data_tokyo247, "dbfnames.mat"), join(raw_data_datasets, "tokyo247.mat"))

