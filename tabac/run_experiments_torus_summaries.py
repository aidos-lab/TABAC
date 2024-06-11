from tqdm import tqdm
import subprocess
import pickle

res_list_rejection_mean = []
res_list_rejection_std = []


for R in tqdm([["1","2"], ["3","5"], ["5","10"]]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary_torus.py", "--shape", "torus", "--theta", R[0], R[1], "-n", "100", "-N", "250", "--sampler", "rejection", "--distance", "mean"], capture_output=True, text=True)
        fin_res = result.stdout
        fin_res = [float(fin_res[:6]),float(fin_res.split(" ")[-1][:6])]
        inner_list.append(fin_res)
    res_list_rejection_mean.append(inner_list)

for R in tqdm([["1","2"], ["3","5"], ["5","10"]]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary_torus.py", "--shape", "torus", "--theta", R[0], R[1], "-n", "100", "-N", "250", "--sampler", "rejection", "--distance", "std"], capture_output=True, text=True)
        fin_res = result.stdout
        fin_res = [float(fin_res[:6]),float(fin_res.split(" ")[-1][:6])]
        inner_list.append(fin_res)
    res_list_rejection_std.append(inner_list)

res_dic = {"Torus Rejection mean":res_list_rejection_mean, "Torus Rejection std":res_list_rejection_std}

with open('torus.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)