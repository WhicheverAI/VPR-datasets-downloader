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

datasets_folder = join(os.curdir, "datasets")
dataset_name = "mapillary_sls"
dataset_folder = join(datasets_folder, dataset_name)
raw_data_folder = join(datasets_folder, dataset_name, "raw_data")
os.makedirs(dataset_folder, exist_ok=True)
os.makedirs(raw_data_folder, exist_ok=True)
os.makedirs(join(dataset_folder, "images", "test"), exist_ok=True)

#### Database
print("Downloading database archives")
filenames = [
    "msls_checksums.md5"    ,
    "msls_images_vol_1.zip" ,
    "msls_images_vol_2.zip" ,
    "msls_images_vol_3.zip" ,
    "msls_images_vol_4.zip" ,
    "msls_images_vol_5.zip" ,
    "msls_images_vol_6.zip" ,
    "msls_metadata.zip"     ,
    "msls_patch_v1.1.zip"   ,
]

urls = config.msls_urls
urls = urls.split("\n")
urls = [u.strip() for u in urls if u.strip()]
tars_paths = [join(raw_data_folder, f) for f in filenames]
for i, (url, tar_path) in enumerate(zip(urls, tars_paths)):
    check = tar_path.replace("PCIs_", "").replace(".tar", "")
    # if os.path.exists(check):
    #     print(f"I see {check}, won't download {tar_path} again. ")
    #     continue
    print(f"{i:>3} / {len(filenames)} ) downloading {tar_path}")
    util.download_heavy_file(url, tar_path)
    try:  # Unpacking database archives
        shutil.unpack_archive(tar_path, raw_data_folder)
    except shutil.ReadError:
        print("Error unpacking", tar_path)
        pass  # Some tars are empty files
# 也可以自己用 unzip '*.zip' 注意''不可以省略，否则会*被shell展开，反而不符合unzip语法

# 还需要自己运行format

