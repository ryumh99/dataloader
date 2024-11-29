import subprocess
import re
import numpy as np

def extract_values(output):
    # extract
    avg_runtime_match = re.search(r"Average Runtime:\s*([\d.]+)", output)
    std_runtime_match = re.search(r"Standard Deviation:\s*([\d.]+)",output)
    param_search_time_match = re.search(r"Parameter Search Time:\s*([\d.)+)",output)
    
    avg_runtime = float(avg_runtime_match.group(1)) if avg_runtime_match else None
    std_runtime = float(std_runtime_match.group(1)) if std_runtime_match else None
    param_search_time = float(param_search_time_match.group(1)) if param_search_time_match else None
    return avg_runtime , std_runtime, param_search_time

def run_and_average(script_path, runs = 5):
    avg_runtimes = []
    std_runtimes = []
    param_search_times = []

    for _ in range(runs):
        #subprocess execute and capture
        result = subprocess.run(['python',script_path],capture_output=True, text= True )

        avg_runtime , std_runtime, param_search_time = extract_values(result.stdout)
    
        if avg_runtime is not None:
            avg_runtimes.append(avg_runtime)
        if std_runtime is not None:
            std_runtimes.append(std_runtime)
        if param_search_time is not None:
            param_search_times.append(param_search_time)
        
        avg_runtime_mean = np.mean(avg_runtimes) if avg_runtimes else None
        std_runtime_mean = np.mean(std_runtimes) if std_runtimes else None
        param_search_time_mean = np.mean(param_search_times) if param_search_times else None
        
        return avg_runtime_mean, std_runtime_mean, param_search_time_mean


if __name__ == "__main__":
    

    dataloader_default_avg_runtime, dataloader_default_std_runtime, dataloader_default_param_search_time = run_and_average('dataloader_default', runs=5)

    dataloader_grid_cutline_avg_runtime, dataloader_grid_cutline_std_runtime, dataloader_grid_cutline_param_search_time = run_and_average('dataloader_grid_cutline', runs=5)

    dataloader_binary_avg_runtime, dataloader_binary_std_runtime, dataloader_binary_param_search_time = run_and_average('dataloader_binary',runs=5)

   # 결과 출력
    print("Dataloader Default Script Average Results:")
    print(f"Average Runtime: {dataloader_default_avg_runtime:.4f} ms")
    print(f"Average Standard Deviation: {dataloader_default_std_runtime:.4f} ms")
    print(f"Average Parameter Search Time: {dataloader_default_param_search_time:.4f} seconds")
    # 결과 출력
    print("Dataloader Grid Cutline Script Average Results:")
    print(f"Average Runtime: {dataloader_grid_cutline_avg_runtime:.4f} ms")
    print(f"Average Standard Deviation: {dataloader_grid_cutline_std_runtime:.4f} ms")
    print(f"Average Parameter Search Time: {dataloader_grid_cutline_param_search_time:.4f} seconds")
    # 결과 출력
    print("Dataloader Binary Script Average Results: ")
    print(f"Average Runtime : {dataloader_binary_avg_runtime:.4f} ms")
    print(f"Average Standard Deviation: {dataloader_binary_std_runtime:.4f} ms")
    print(f"Average Parameter Search Time: {dataloader_binary_param_search_time:.4f} seconds")
