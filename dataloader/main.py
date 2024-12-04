import subprocess
import re
import numpy as np

import argparse

from collections import Counter

def extract_values(output):
    # extract
    avg_runtime_match = re.search(r"Average Runtime:\s*([\d.]+)", output)
    std_runtime_match = re.search(r"Standard Deviation:\s*([\d.]+)",output)
    param_search_time_match = re.search(r"Parameter Search Time:\s*([\d.]+)",output)
    best_config_match = re.search(r"Best Configuration:\s*({.*})",output)
    
    avg_runtime = float(avg_runtime_match.group(1)) if avg_runtime_match else None
    std_runtime = float(std_runtime_match.group(1)) if std_runtime_match else None
    param_search_time = float(param_search_time_match.group(1)) if param_search_time_match else None
    best_config = eval(best_config_match.group(1)) if best_config_match else None

    return avg_runtime , std_runtime, param_search_time, best_config

def run_and_average(script_path,batch_size, runs = 5):
    avg_runtimes = []
    std_runtimes = []
    param_search_times = []
    best_configs = []

    for _ in range(runs):
        #subprocess execute and capture
        result = subprocess.run(['python',script_path, '--batch_size', str(batch_size)],capture_output=True, text= True )

        avg_runtime , std_runtime, param_search_time, best_config = extract_values(result.stdout)
    
        if avg_runtime is not None:
            avg_runtimes.append(avg_runtime)
        if std_runtime is not None:
            std_runtimes.append(std_runtime)
        if param_search_time is not None:
            param_search_times.append(param_search_time)
        if best_config is not None:
            best_configs.append(str(best_config))
        
        avg_runtime_mean = np.mean(avg_runtimes) if avg_runtimes else None
        std_runtime_mean = np.mean(std_runtimes) if std_runtimes else None
        param_search_time_mean = np.mean(param_search_times) if param_search_times else None

        best_config_counter = Counter(best_configs)
        most_common_config = eval(best_config_counter.most_common(1)[0][0]) if best_configs else None
        
        return avg_runtime_mean, std_runtime_mean, param_search_time_mean, most_common_config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch_size",type=int, default =2, help = "Batch size for DataLoader") # 32, ,64 ,128 ,256 
    args = parser.parse_args()
    batch_size = args.batch_size

    dataloader_default_avg_runtime, dataloader_default_std_runtime, dataloader_default_param_search_time, dataloader_default_most_common_config = run_and_average('dataloader_default', batch_size, runs=5)

    dataloader_grid_cutline_avg_runtime, dataloader_grid_cutline_std_runtime, dataloader_grid_cutline_param_search_time, dataloader_grid_cutline_most_common_config = run_and_average('dataloader_grid_cutline', batch_size, runs=5)

    dataloader_greedy_cutline_avg_runtime, dataloader_greedy_cutline_std_runtime, dataloader_greedy_cutline_param_search_time,dataloader_greedy_cutline_most_common_config = run_and_average('dataloader_greedy_cutlne', batch_size, runs = 5)



   # default 결과 출력
    print("Dataloader Default Script Average Results:")
    print(f"Average Runtime: {dataloader_default_avg_runtime:.4f} ms")
    print(f"Average Standard Deviation: {dataloader_default_std_runtime:.4f} ms")
    print(f"Average Parameter Search Time: {dataloader_default_param_search_time:.4f} seconds")
    print(f"Most Common Best Configuration: {ataloader_default_most_common_config}")
    # grid_cutline 결과 출력
    print("Dataloader Grid with Cutline Script Average Results:")
    print(f"Average Runtime: {dataloader_grid_cutline_avg_runtime:.4f} ms")
    print(f"Average Standard Deviation: {dataloader_grid_cutline_std_runtime:.4f} ms")
    print(f"Average Parameter Search Time: {dataloader_grid_cutline_param_search_time:.4f} seconds")
    print(f"Most Common Best Configuration: {dataloader_grid_cutline_most_common_config}")
    # greedy_cutline 결과 출력
    print("Dataloader Binary with Cutline Script Average Results: ")
    print(f"Average Runtime : {dataloader_greedy_cutline_avg_runtime:.4f} ms")
    print(f"Average Standard Deviation: {dataloader_greedy_cutline_std_runtime:.4f} ms")
    print(f"Average Parameter Search Time: {dataloader_greedy_cutline_param_search_time:.4f} seconds")
    print(f"Most Common Best Configuration: {dataloader_greedy_cutline_most_common_config}")
