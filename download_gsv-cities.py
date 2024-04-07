from pathlib import Path
this_file = Path(__file__).resolve()
this_directory = this_file.parent

datasets_path = this_directory/"datasets"
dataset_name = "gsv-cities"
dataset_folder = datasets_path/dataset_name
raw_data_folder = dataset_folder/"raw_data"
images_folder = dataset_folder/"images"

raw_data_folder.mkdir(parents=True, exist_ok=True)
images_folder.mkdir(parents=True, exist_ok=True)

# Download from kaggle
# import subprocess
# subprocess.check_output("kaggle d download amaralibey/gsv-cities")
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
api.model_list_cli()
api.dataset_download_files("amaralibey/gsv-cities", path=raw_data_folder.as_posix(), unzip=True)

# Download the visualization notebook
# kaggle kernels pull amaralibey/gsv-cities-visualizing-the-dataset
# 