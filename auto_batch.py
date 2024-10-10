#%%
import itertools
import os
from pathlib import Path
this_file = Path(__file__).resolve()
this_directory = this_file.parent
import json
# from datetime import date, datetime
import datetime
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
        

#%%
import datetime
import pickle
import subprocess
def command_executor(content
                    # , verbose=True
                    )->str:
    print(f"executing command:\n\t {content}")
    os.chdir(this_directory.as_posix())
    # 需要把内容实时打印到这个终端，同时得到output，同时需要shell
    # output = subprocess.check_output(content, shell=True, stderr=subprocess.STDOUT)
    # output = subprocess.check_output(content, shell=True, stderr=subprocess.PIPE)
    process = subprocess.Popen(content, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    output = ""
    # 实时读取输出
    for line in process.stdout:
        print(line, end='')  # 打印到屏幕
        output += line  # 将输出内容追加到变量

    # 等待命令执行完成
    process.wait()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(returncode=process.returncode, cmd=content, output=output.encode('utf-8'))
    # if verbose:
    #     output = subprocess.check_output(content, shell=True, stderr=subprocess.STDOUT)
    # else:
    #     output = subprocess.check_output(content, shell=True, stderr=subprocess.DEVNULL)
    return output.strip()
   
#%%    
from decorator import decorator
@decorator
def auto_try_decorator(func, *args, **kwargs):
    try:
        return dict(status='done', output=func(*args, **kwargs))
    except subprocess.CalledProcessError as e:
        return dict(status='error', output=e.output.decode('utf-8'))
    

from typing import Callable
def auto_run(executor:Callable=command_executor, argses:list = None,
             run_names:list=None, 
             plan_name = "default_plan", auto_try=True
             , output_dir="auto_run_output"):
    if argses is None:
        argses = ["echo Welcome to auto_run!"]
    if auto_try:
        executor = auto_try_decorator(executor)
    if run_names is None:
        run_names = [f"run_{i}" for i in range(len(argses))]
    running_plan_dict = {run_name:args for run_name, args in zip(run_names, argses)}
    memory_file = f'auto_run_memory_{plan_name}.json'
    output_dir = this_directory / output_dir
    output_dir.mkdir(exist_ok=True, parents=True)
    with open(output_dir / f'plans_{plan_name}.json', 'w') as f:
        json.dump(running_plan_dict, f, ensure_ascii=False, indent=4, cls=ComplexEncoder)
        
    def dump_mem(memory):
            
        if (output_dir/memory_file).exists():
            with open(output_dir/(memory_file), 'r') as f:
                old_memory = json.load(f)
        else:
            old_memory = {}
        new_memory = {**old_memory, **memory}
        
        with open(output_dir/(memory_file), 'w') as f:
            json.dump(new_memory, f, ensure_ascii=False, indent=4)
            
        return new_memory

    memory = dump_mem(dict())
    
    import time
    num_of_done = 0
    # def loop_all_runs_once():
    for running_round in itertools.count():
        if num_of_done == len(running_plan_dict):  
            print("all runs are done, exiting...")
            break
        num_of_done = 0
        print(f"new running round {running_round}")
        # for run_name, args in zip(run_names, argses):
        for run_name, args in running_plan_dict.items():
            if run_name in memory:
                d = memory[run_name][-1]
                status = d.get('status', 'unknown')
                print(f"run_name {run_name} has been executed with status {status}")
                if status == 'error':
                    print("retrying...")
                    
                    memory[run_name].append(dict(status='running', output='retrying...'))
                    memory = dump_mem(memory)
                    
                    new_output = executor(args)
                    print(f"exited, status is {new_output['status']}")
                    memory[run_name].append(new_output)
                    
                elif status == 'done':
                    num_of_done+=1
                    continue
                elif status == 'running':
                    print("Other instance of this script is running this task, skipping...")
                    continue
                else:
                    print("status unknown, changing it to error")
                    memory[run_name].append(dict(status='error'))
            else:
                print(f"executing run_name {run_name}")
                memory[run_name] = [
                    dict(status='running', output='executing...')
                ]
                memory = dump_mem(memory)
                new_output = executor(args)
                print(f"exited, status is {new_output['status']}")
                memory[run_name] = [
                    new_output
                ]
            if new_output['status'] == 'done':
                num_of_done+=1
            memory = dump_mem(memory)
            time.sleep(5)
    
#%%

auto_run()


# %%
