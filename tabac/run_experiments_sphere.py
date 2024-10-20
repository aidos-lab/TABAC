from tqdm import tqdm
import subprocess
import pickle

res_list_importance_scc = []
res_list_importance_topological = []
res_list_MCMC_scc = []
res_list_MCMC_topological = []

for theta in tqdm(["1","5","10"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "sphere", "--theta", theta,"-n", "100", "-N", "250", "--sampler", "importance", "--distance", "hausdorff"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_importance_scc.append(inner_list)

for theta in tqdm(["1","5","10"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "sphere", "--theta", theta, "-n", "100", "-N", "250", "--sampler", "importance", "--distance", "topological"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_importance_topological.append(inner_list)

for theta in tqdm(["1","5","10"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "sphere", "--theta", theta, "-n", "100", "-N", "250", "--sampler", "MCMC", "--distance", "hausdorff"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_MCMC_scc.append(inner_list)

for theta in tqdm(["1","5","10"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "sphere", "--theta", theta, "-n", "100", "-N", "250", "--sampler", "MCMC", "--distance", "topological"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_MCMC_topological.append(inner_list)

res_dic = {"Sphere Importance Hausdorff":res_list_importance_scc,"Sphere Importance topological":res_list_importance_topological,"Sphere MCMC Hausdorff":res_list_MCMC_scc,"Sphere MCMC topological":res_list_MCMC_topological}

with open('sphere.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)