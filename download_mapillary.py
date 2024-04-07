
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
urls = ["https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An8t-3LMOE6eyv7YZ5CD_ReDw-_DCGg2KLySdox-cFJUwtaKsQRjSRgz6gvDgaBpJnkfXoFHLGSTWnfmV5-ofbaqWwlduOhznfVmA0z5xBdLwcqKSXTdDLl1LjZo.md5?ccb=10-5&oh=00_AfCnJjIKujvj5aKPbF0c0U9r9xO1EC3q92RtuUyytHsZKg&oe=65B5ED4C&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An-x6BOZeUDmFXVxCKtosZWgMZzQiLR1iBxkevoDhNKLyXwMULUhqUB5pExN3EDE7RfPewnC6_Omad8kkRV1vwyOhWXqOJp3-3d6hWARSf_41taXCsAlVF1gp5gf2S7W.zip?ccb=10-5&oh=00_AfDq4qO9Cdb041poIMeTP0N01pGh5kd6uhHn4zsgsf8QiQ&oe=65B5D2D1&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An9l_yexUWNWbUOGWt-7HVC-ONHffIDJQeVnpo4Fp3-X7p6f7NoevyddUQ4WdsoufwUjzW2nhB29AMgdRm8WSxAup2B6qZikAC4tGtMaC0x3PLJn76tkBpMhjqlb_lLs.zip?ccb=10-5&oh=00_AfBS6TjzX1Yp2ZHVYHdPjqZTnaf8zb4Xz7xH0kv95rz9dQ&oe=65B5E3F7&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An-McnhyZtsCZK-zzwCIPBlWXhBl4d3Qas_TyqLiRHb8VvEP_ilvcJftXCAcmvirTo1NBF_EJKzEgSdrFu0owLWvywQ4S7y6GNpFYb7XxokmgVpeGlisqVTWkOE4Wi9P.zip?ccb=10-5&oh=00_AfDF_tVdGMNsGJ3H1ItUudlC406dXAo5VQ9zeGEN4CAF-A&oe=65B5D46E&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An8vpu-mDXBO2YvVoOO9wcXuIVUF_6yTrxKFB4Wp4tFjaVnRcEqlmvTTdFk-lxjv0VVGFoowHUXsCUuUiykQ8d7dKaLx6Atvtw07uLfPbDhTrpoWdlA-FasNCMKuxCvp.zip?ccb=10-5&oh=00_AfAONZvNV-tfRZkdcy2OpHIgDOPgORUMI0j4-yAWWsleIw&oe=65B5CD2B&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An9e0HGaRi-9kM8QyF5wNHyA-DVxI_C_aN9rC3iAXHLN9_RoW9P8SUHRR39AeszPqegQnqk-LL49sYIjsAIdS23yl9rwu1NPOdDbjFmvzlTYERwsxv6nAObVUBNOjDrN.zip?ccb=10-5&oh=00_AfALxCtBUBqgKyX2wwmPWPN4TdK-26fBoEnY_Yk-3wEn2w&oe=65B5D53E&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An-zh-eec0DwQv9bkj0KVhowIEpbMW6qg578XP4PU51TH-5PpQtKYJDb8kax3KBOn1qXKeM9jUsKeaqkaEIxqpZFfsJ6tITsg2jsz7Wd9mSTWSLR3EuyXcjLzBGDImv_.zip?ccb=10-5&oh=00_AfAdaVt8kT7k8wmnhLkb2SuEga7dC5wGosUW6kZ3O5EMWA&oe=65B5C921&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An9znN6Evsbp2KNZvdYc0NsYCk961Vy0u_j6ACpZ_QoylW800rBKCSeZQAq765BP03K_qyPpPK8aCNU6wnVa44M6cmx4X-iTJVQ8zCwaH5BJom47I8Xr25XLTw.zip?ccb=10-5&oh=00_AfCnILk4J-8s5msMa4GUQCbzXFXEw211j_YQ3oZ1HhW2XQ&oe=65B5EE98&_nc_sid=6de079"
        ,"https://scontent-sin6-2.xx.fbcdn.net/m1/v/t6/An9DCNVm9dpPbX3zG544xA35U2Qqb7oPWrN3-_39Fp9NxF2oKLx3cKw3QKzPL5bsNokN-NodhGD-mHrUZsXVfA3Zil71HcjIZXJ3Lk8P5jktf3sftUlmO_9sohJb.zip?ccb=10-5&oh=00_AfB_RWyXAELtjhvWahYMZLgTi8dLqJr2g5o3JioyQieHVA&oe=65B5D772&_nc_sid=6de079"
        ]
tars_paths = [join(raw_data_folder, f) for f in filenames]
for i, (url, tar_path) in enumerate(zip(urls, tars_paths)):
    check = tar_path.replace("PCIs_", "").replace(".tar", "")
    if os.path.exists(check):
        print(f"I see {check}, won't download {tar_path} again. ")
        continue
    print(f"{i:>3} / {len(filenames)} ) downloading {tar_path}")
    util.download_heavy_file(url, tar_path)
    try:  # Unpacking database archives
        shutil.unpack_archive(tar_path, raw_data_folder)
    except shutil.ReadError:
        print("Error unpacking", tar_path)
        pass  # Some tars are empty files
# 也可以自己用 unzip '*.zip' 注意''不可以省略，否则会*被shell展开，反而不符合unzip语法

# 还需要自己运行format

