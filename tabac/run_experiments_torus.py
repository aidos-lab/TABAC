from tqdm import tqdm
import subprocess
import pickle

res_list_importance_scc = []
res_list_importance_topological = []
res_list_MCMC_scc = []
res_list_MCMC_topological = []


for R in tqdm([["1","2"], ["3","5"], ["5","10"]]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary_torus.py", "--shape", "torus", "--theta", R[0], R[1], "-n", "100", "-N", "250", "--sampler", "importance", "--distance", "hausdorff"], capture_output=True, text=True)
        fin_res = result.stdout
        fin_res = [float(fin_res[:6]),float(fin_res.split(" ")[-1][:6])]
        inner_list.append(fin_res)
    res_list_importance_scc.append(inner_list)

for R in tqdm([["1","2"], ["3","5"], ["5","10"]]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary_torus.py", "--shape", "torus", "--theta", R[0], R[1], "-n", "100", "-N", "250", "--sampler", "importance", "--distance", "topological"], capture_output=True, text=True)
        fin_res = result.stdout
        fin_res = [float(fin_res[:6]),float(fin_res.split(" ")[-1][:6])]
        inner_list.append(fin_res)
    res_list_importance_topological.append(inner_list)

for R in tqdm([["1","2"], ["3","5"], ["5","10"]]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary_torus.py", "--shape", "torus", "--theta", R[0], R[1], "-n", "100", "-N", "250", "--sampler", "MCMC", "--distance", "hausdorff"], capture_output=True, text=True)
        fin_res = result.stdout
        fin_res = [float(fin_res[:6]),float(fin_res.split(" ")[-1][:6])]
        inner_list.append(fin_res)
    res_list_MCMC_scc.append(inner_list)

for R in tqdm([["1","2"], ["3","5"], ["5","10"]]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary_torus.py", "--shape", "torus", "--theta", R[0], R[1], "-n", "100", "-N", "250", "--sampler", "MCMC", "--distance", "topological"], capture_output=True, text=True)
        fin_res = result.stdout
        fin_res = [float(fin_res[:6]),float(fin_res.split(" ")[-1][:6])]
        inner_list.append(fin_res)
    res_list_MCMC_topological.append(inner_list)

res_dic = {"Torus Importance Hausdorff":res_list_importance_scc,"Torus Importance topological":res_list_importance_topological,"Torus MCMC Hausdorff":res_list_MCMC_scc,"Torus MCMC topological":res_list_MCMC_topological}

with open('torus.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)