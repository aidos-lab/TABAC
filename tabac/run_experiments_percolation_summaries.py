from tqdm import tqdm
import subprocess
import pickle

res_list_rejection_mean = []
res_list_rejection_std = []

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "perc", "--theta", theta, "50", "-n", "100", "-N", "250", "--sampler", "rejection", "--distance", "mean"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_rejection_mean.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "perc", "--theta", theta, "50", "-n", "100", "-N", "250", "--sampler", "rejection", "--distance", "std"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_rejection_std.append(inner_list)

res_dic = {"Perc Rejection mean":res_list_rejection_mean, "Perc Rejection std":res_list_rejection_std}

with open('perc.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)