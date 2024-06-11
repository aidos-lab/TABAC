from tqdm import tqdm
import subprocess
import pickle

res_list_rejection_mean = []
res_list_rejection_std = []

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "vicsek", "--theta", theta, "-n", "2000", "-N", "250", "--sampler", "rejection", "--distance", "mean"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_rejection_mean.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "vicsek", "--theta", theta, "-n", "2000", "-N", "250", "--sampler", "rejection", "--distance", "std"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_rejection_std.append(inner_list)


res_dic = {"Vicsek Rejection mean":res_list_rejection_mean, "Vicsek Rejection std":res_list_rejection_std}

with open('vicsek_5.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)