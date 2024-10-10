#%%
from auto_batch import auto_run, command_executor, this_directory

#%%
download_pys = [f for f in this_directory.glob('*.py') if f.name.startswith("download")]
format_pys = [f for f in this_directory.glob('*.py') if f.name.startswith("format")]


# # TODO 可以有更加智能的方法决定顺序, 避免被卡
all_pys = download_pys + format_pys
commands = [f"python {f.name}" for f in all_pys]
run_names = [f.stem for f in all_pys]
#%%
auto_run(command_executor, commands, run_names, "download_and_format")
    