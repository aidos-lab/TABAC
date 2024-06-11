from tqdm import tqdm
import subprocess
import pickle

res_list_importance_scc = []
res_list_importance_topological = []
res_list_rejection_mean = []
res_list_rejection_std = []


for theta in tqdm(["1","5","10"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "sphere", "--theta", theta, "-n", "100", "-N", "250", "--sampler", "rejection", "--distance", "mean"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_rejection_mean.append(inner_list)

for theta in tqdm(["1","5","10"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "sphere", "--theta", theta, "-n", "100", "-N", "250", "--sampler", "rejection", "--distance", "std"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_rejection_std.append(inner_list)

res_dic = {"Sphere Rejection mean":res_list_rejection_mean, "Sphere Rejection std":res_list_rejection_std}

with open('sphere.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)