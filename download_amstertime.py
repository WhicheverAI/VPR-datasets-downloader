"""
This script download the AmsterTime dataset, from the paper by Yildiz et al
"AmsterTime: A Visual Place Recognition Benchmark Dataset for Severe Domain Shift"
- https://arxiv.org/abs/2203.16291.
The AmsterTime dataset is organize in pair of images, each pair being one query
and one database image. The query is a historical photo, while the database
image is a modern photo. Because their positions (e.g. GPS) are not available,
we create mock positions for each pair, with images within a pair having the
same position, and consecutive pairs being 100 meters away from each other.
"""

import os
import shutil
import py3_wget
from glob import glob
from tqdm import tqdm
from PIL import Image
from os.path import join


datasets_folder = join(os.curdir, "datasets")
dataset_name = "amstertime"
dataset_folder = join(datasets_folder, dataset_name)
raw_data_folder = join(datasets_folder, dataset_name, "raw_data")
database_folder = join(dataset_folder, "images", "test", "database")
queries_folder = join(dataset_folder, "images", "test", "queries")
os.makedirs(dataset_folder, exist_ok=True)
os.makedirs(database_folder, exist_ok=True)
os.makedirs(queries_folder, exist_ok=True)
os.makedirs(raw_data_folder, exist_ok=True)

py3_wget.download_file(
    url="https://data.4tu.nl/ndownloader/items/d2ee2551-986a-46bc-8540-b43f5b01ec4d/versions/4",
    output_path=join(raw_data_folder, "data.zip")
)

shutil.unpack_archive(join(raw_data_folder, "data.zip"), raw_data_folder)
shutil.unpack_archive(join(raw_data_folder, "AmsterTime-v1.0.zip"), raw_data_folder)

database_paths = sorted(glob(join(raw_data_folder, "new", "*.png")))
queries_paths = sorted(glob(join(raw_data_folder, "old", "*.jpg")))

for db_filepath, q_filepath in zip(tqdm(database_paths), queries_paths):
    db_filename = os.path.basename(db_filepath)
    q_filename = os.path.basename(q_filepath)
    # Query and DB images from the same pair have the same name
    assert os.path.splitext(db_filename)[0] == os.path.splitext(q_filename)[0]
    pair_name = os.path.splitext(db_filename)[0]
    # Simulate a distance of at least 100 meters between any two pairs of non-matching images
    mock_utm_east = int(pair_name) * 1000
    new_image_name = f"@0@{mock_utm_east}@@@@@{pair_name}@@@@@@@@.jpg"
    new_q_path = os.path.join(queries_folder, new_image_name)  # queries are in JPEG
    _ = shutil.move(q_filepath, new_q_path)
    new_db_path = os.path.join(database_folder, new_image_name)
    Image.open(db_filepath).convert("RGB").save(new_db_path)  # db images are in PNG, so convert to JPEG
    os.remove(db_filepath)

