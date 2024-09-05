from tqdm import tqdm
import subprocess
import pickle

res_list_importance_scc = []
res_list_importance_topological = []
res_list_MCMC_scc = []
res_list_MCMC_topological = []

num_simulations = "750"

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "vicsek", "--theta", theta, "-n", "2000", "-N", num_simulations, "--sampler", "importance", "--distance", "hausdorff"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_importance_scc.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "vicsek", "--theta", theta, "-n", "2000", "-N", num_simulations, "--sampler", "importance", "--distance", "topological"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_importance_topological.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "vicsek", "--theta", theta, "-n", "2000", "-N", num_simulations, "--sampler", "MCMC", "--distance", "hausdorff"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_MCMC_scc.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "vicsek", "--theta", theta, "-n", "2000", "-N", num_simulations, "--sampler", "MCMC", "--distance", "topological"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_MCMC_topological.append(inner_list)

res_dic = {"Vicsek Importance hausdorff":res_list_importance_scc,"Vicsek Importance topological":res_list_importance_topological,"Vicsek MCMC hausdorff":res_list_MCMC_scc,"Vicsek MCMC topological":res_list_MCMC_topological}

with open('vicsek_50_'+num_simulations+'.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)
