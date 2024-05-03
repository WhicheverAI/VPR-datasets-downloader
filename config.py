# In this config.py, you will know which urls you should fill in the config_private.py in order to makes the downloading works.


# Email arandjelovic.relja@gmail.com to get the full link of pitts and tokyo.
pitts_250k_url:str = "https://****/****/****/****/Pittsburgh250k" # Without a '/' at the end. 
tokyo247_url:str = "https://****/****/****/****/Tokyo247"


# 1. Read documentation at https://github.com/mapillary/mapillary_sls
# 2. Register an account at https://www.mapillary.com/dataset/places, then you can see the download page. 
# 3. Copy the links of the following files sequentially in the page shown in your browswer, by right click your mouse and select copy. 
msls_urls = """https:// strange path to msls_checksums.md5
https://****/ strange path to msls_images_vol_1.zip
https://****/ strange path to msls_images_vol_2.zip
https://****/ strange path to msls_images_vol_3.zip
https://****/ strange path to msls_images_vol_4.zip
https://****/ strange path to msls_images_vol_5.zip
https://****/ strange path to msls_images_vol_6.zip
https://****/ strange path to msls_metadata.zip
https://****/ strange path to msls_patch_v1.1.zip
"""
# TODO  In the future, we may parse the private html that you got from the MSLS team, 
# and then automatically reads the above urls for you. 

# svox
# The following url cannot be directly download!
# 1. Click the link in your browser, you will see the google drive page
# 2. Click the download button
# 3. Copy the download link from the browser download utils. 
# 4. set svox_url to that link in config_private.py
svox_url = "https://drive.google.com/uc?id=16iuk8voW65GaywNUQlWAbDt6HZzAJ_t9"

# Now the variables defined here would be overrided in config_private.py
from config_private import *