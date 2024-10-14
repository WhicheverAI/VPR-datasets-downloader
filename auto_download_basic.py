#%%
from auto_batch import auto_run, command_executor, this_directory

#%%

all_pys = [
    "download_pitts250k_and_30k.py",
    "format_pitts30k.py",
    "format_pitts250k.py",
    "download_mapillary.py",
    "format_mapillary.py"
]
commands = [f"python {f}" for f in all_pys]
run_names = [f for f in all_pys]
#%%
step1 = lambda :auto_run(command_executor, commands, run_names[0:1], "basic_download_and_format_step_1")
step2 = lambda :auto_run(command_executor, commands, run_names[1:3], "basic_download_and_format_step_2")
step3 = lambda :auto_run(command_executor, commands, run_names[3:], "basic_download_and_format_step_3")

step1()
import threading

threads = [threading.Thread(target=step2), threading.Thread(target=step3)]
for t in threads:
    t.start()
for t in threads:
    t.join()