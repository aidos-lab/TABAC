from tqdm import tqdm
import subprocess
import pickle
from concurrent.futures import ProcessPoolExecutor

num_simulations = "1000"
thetas = ["0.2", "0.3", "0.4"]


# Function to run the subprocess and process the result
def run_simulation(args):
    sampler, distance, theta, num_simulations = args
    result = subprocess.run(
        ["python", "experiments_auxiliary.py", "--shape", "fluid", "--theta", theta, "-n", "40000", "-N",
         num_simulations, "--sampler", sampler, "--distance", distance],
        capture_output=True, text=True
    )
    if len(result.stdout) > 0:
        return float(result.stdout)
    else:
        return 0


# Define the parameters for each run
def generate_tasks(sampler, distance, thetas, num_simulations):
    tasks = []
    for theta in thetas:
        for _ in range(5):  # Each theta runs 5 times
            tasks.append((sampler, distance, theta, num_simulations))
    return tasks


# Main function to execute all simulations in parallel
def parallel_run():
    res_list_importance_scc = []
    res_list_importance_topological = []
    res_list_MCMC_scc = []
    res_list_MCMC_topological = []

    # Create the task lists for each of the four combinations
    tasks_importance_scc = generate_tasks("importance", "hausdorff", thetas, num_simulations)
    tasks_importance_topological = generate_tasks("importance", "cubical", thetas, num_simulations)
    tasks_MCMC_scc = generate_tasks("MCMC", "hausdorff", thetas, num_simulations)
    tasks_MCMC_topological = generate_tasks("MCMC", "cubical", thetas, num_simulations)

    # Combine all tasks into a single list
    all_tasks = tasks_importance_scc + tasks_importance_topological + tasks_MCMC_scc + tasks_MCMC_topological

    # Use ProcessPoolExecutor to parallelize all tasks
    with ProcessPoolExecutor(max_workers=None) as executor:  # Adjust max_workers if necessary
        # Execute all tasks and show a single progress bar for all tasks
        results = list(tqdm(executor.map(run_simulation, all_tasks, chunksize=5), total=len(all_tasks)))

    # Split the results back into the respective lists
    res_list_importance_scc = results[:15]
    res_list_importance_topological = results[15:30]
    res_list_MCMC_scc = results[30:45]
    res_list_MCMC_topological = results[45:]

    # Reshape the flat lists into a list of lists with 5 elements each (as per the original structure)
    def reshape_results(flat_list, num_groups=3, num_per_group=5):
        return [flat_list[i * num_per_group:(i + 1) * num_per_group] for i in range(num_groups)]

    res_list_importance_scc = reshape_results(res_list_importance_scc)
    res_list_importance_topological = reshape_results(res_list_importance_topological)
    res_list_MCMC_scc = reshape_results(res_list_MCMC_scc)
    res_list_MCMC_topological = reshape_results(res_list_MCMC_topological)

    # Save results as a dictionary
    res_dic = {
        "Fluid Importance hausdorff": res_list_importance_scc,
        "Fluid Importance topological": res_list_importance_topological,
        "Fluid MCMC hausdorff": res_list_MCMC_scc,
        "Fluid MCMC topological": res_list_MCMC_topological
    }

    # Save to file
    with open('fluid_3000_' + num_simulations + '.pkl', 'wb') as fp:
        pickle.dump(res_dic, fp)


# Execute the parallel run
if __name__ == "__main__":
    parallel_run()
