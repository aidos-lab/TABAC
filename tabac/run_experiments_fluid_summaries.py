from tqdm import tqdm
import subprocess
import pickle

res_list_rejection_mean = []
res_list_rejection_std = []


for theta in tqdm(["0.2","0.3","0.4"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "fluid", "--theta", theta, "-n", "40000", "-N", "250", "--sampler", "rejection", "--distance", "mean"], capture_output=True, text=True)
        if len(result.stdout)>0:
            fin_res = float(result.stdout)
        else:
            fin_res = 0
        print(fin_res)
        inner_list.append(fin_res)
    res_list_rejection_mean.append(inner_list)

for theta in tqdm(["0.2","0.3","0.4"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "fluid", "--theta", theta, "-n", "40000", "-N", "250", "--sampler", "rejection", "--distance", "std"], capture_output=True, text=True)
        if len(result.stdout) > 0:
            fin_res = float(result.stdout)
        else:
            fin_res = 0
        print(fin_res)
        inner_list.append(fin_res)
    res_list_rejection_std.append(inner_list)

res_dic = {"Fluid Rejection mean":res_list_rejection_mean, "Fluid Rejection std":res_list_rejection_std}

with open('fluid_3000_summaries.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)