
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
datasets_folder = os.path.abspath(datasets_folder)
dataset_name = "pitts_all"
dataset_folder = join(datasets_folder, dataset_name)
raw_data_folder = join(datasets_folder, dataset_name, "raw_data")
os.makedirs(dataset_folder, exist_ok=True)
os.makedirs(raw_data_folder, exist_ok=True)
os.makedirs(join(dataset_folder, "images", "test"), exist_ok=True)

# #### Database
# print("Downloading database specification")

# datasets_specification_tar = join(raw_data_folder, "netvlad_v100_datasets.tar.gz")
# util.download_heavy_file(
#     "https://www.di.ens.fr/willow/research/netvlad/data/netvlad_v100_datasets.tar.gz",
#     datasets_specification_tar
# )
# shutil.unpack_archive(datasets_specification_tar, raw_data_folder)
# change the name to "datasets" folder 
# 不需要，直接解压就是datasets文件夹
# shutil.move(join(raw_data_folder, "netvlad_v100_datasets"), join(raw_data_folder, "datasets"))

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
[   ]	007.tar	2015-11-19 02:44	782M	 
[   ]	008.tar	2015-11-19 03:00	786M	 
[   ]	009.tar	2015-11-19 03:16	814M	 
[   ]	010.tar	2015-11-19 03:25	470M	 
[   ]	groundtruth.tar	2015-11-19 03:26	45M	 
# [   ]	md5sums.txt	2020-06-08 14:28	636	 
[   ]	netvlad_v100_datasets.tar.gz	2020-08-26 13:13	2.1M	 
[   ]	pose.txt	2008-08-27 20:32	957K	 
[   ]	queries_real.tar	2015-11-19 03:43	856M	 
[   ]	readGt.m	2015-11-19 03:44	849	 
"""
raw_text = "\n".join([i  for i in raw_text.split("\n") if not i.startswith("#")])
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

# 把raw_data文件夹软链接到pitts30k和pitts250k
print("Linking raw data to pitts30k and pitts250k")

# os.symlink(join(datasets_folder, "pitts30k", "raw_data/"),raw_data_folder, target_is_directory=True)
# os.symlink(join(datasets_folder, "pitts250k", "raw_data/"), raw_data_folder, target_is_directory=True)
# ln -s 设计有问题，新建的软链接不能有层级结构，必须是直接的文件夹，所以得先cd进去。
os.makedirs(join(datasets_folder, "pitts30k"), exist_ok=True)
os.makedirs(join(datasets_folder, "pitts250k"), exist_ok=True)
os.chdir(join(datasets_folder, "pitts30k"))
if not os.path.exists("raw_data"):
    os.symlink(raw_data_folder, "raw_data", target_is_directory=True)
os.chdir(join(datasets_folder, "pitts250k"))
if not os.path.exists("raw_data"):  
    os.symlink(raw_data_folder, "raw_data", target_is_directory=True)


# 还需要自己运行format