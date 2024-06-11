from tqdm import tqdm
import subprocess
import pickle

res_list_importance_scc = []
res_list_importance_topological = []
res_list_MCMC_scc = []
res_list_MCMC_topological = []

for theta in tqdm(["0.2","0.3","0.4"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "fluid", "--theta", theta, "-n", "40000", "-N", "250", "--sampler", "importance", "--distance", "hausdorff"], capture_output=True, text=True)
        if len(result.stdout)>0:
            fin_res = float(result.stdout)
        else:
            fin_res = 0
        print(fin_res)
        inner_list.append(fin_res)
    res_list_importance_scc.append(inner_list)

for theta in tqdm(["0.2","0.3","0.4"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "fluid", "--theta", theta, "-n", "40000", "-N", "250", "--sampler", "importance", "--distance", "cubical"], capture_output=True, text=True)
        if len(result.stdout) > 0:
            fin_res = float(result.stdout)
        else:
            fin_res = 0
        print(fin_res)
        inner_list.append(fin_res)
    res_list_importance_topological.append(inner_list)

for theta in tqdm(["0.2","0.3","0.4"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "fluid", "--theta", theta, "-n", "40000", "-N", "250", "--sampler", "MCMC", "--distance", "hausdorff"], capture_output=True, text=True)
        if len(result.stdout) > 0:
            fin_res = float(result.stdout)
        else:
            fin_res = 0
        print(fin_res)
        inner_list.append(fin_res)
    res_list_MCMC_scc.append(inner_list)

for theta in tqdm(["0.2","0.3","0.4"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "fluid", "--theta", theta, "-n", "40000", "-N", "250", "--sampler", "MCMC", "--distance", "cubical"], capture_output=True, text=True)
        if len(result.stdout) > 0:
            fin_res = float(result.stdout)
        else:
            fin_res = 0
        print(fin_res)
        inner_list.append(fin_res)
    res_list_MCMC_topological.append(inner_list)

res_dic = {"Fluid Importance hausdorff":res_list_importance_scc,"Fluid Importance topological":res_list_importance_topological,"Fluid MCMC hausdorff":res_list_MCMC_scc,"Fluid MCMC topological":res_list_MCMC_topological}

with open('fluid_3000.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)