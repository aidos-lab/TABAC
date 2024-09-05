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
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "perc", "--theta", theta, "50", "-n", "100", "-N", num_simulations, "--sampler", "importance", "--distance", "scc"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_importance_scc.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "perc", "--theta", theta, "50", "-n", "100", "-N", num_simulations, "--sampler", "importance", "--distance", "cubical"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_importance_topological.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "perc", "--theta", theta, "50", "-n", "100", "-N", num_simulations, "--sampler", "MCMC", "--distance", "scc"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_MCMC_scc.append(inner_list)

for theta in tqdm(["0.15","0.3","0.6"]):
    inner_list = []
    for i in range(5):
        result = subprocess.run(["python", "experiments_auxiliary.py", "--shape", "perc", "--theta", theta, "50", "-n", "100", "-N", num_simulations, "--sampler", "MCMC", "--distance", "cubical"], capture_output=True, text=True)
        fin_res = float(result.stdout)
        inner_list.append(fin_res)
    res_list_MCMC_topological.append(inner_list)

res_dic = {"Perc Importance SCC":res_list_importance_scc,"Perc Importance topological":res_list_importance_topological,"Perc MCMC SCC":res_list_MCMC_scc,"Perc MCMC topological":res_list_MCMC_topological}

with open('perc_'+num_simulations+'.pkl', 'wb') as fp:
    pickle.dump(res_dic, fp)
