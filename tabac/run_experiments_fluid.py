from tqdm import tqdm
import subprocess
import pickle
from concurrent.futures import ProcessPoolExecutor

thetas = ["0.2", "0.3", "0.4"]
num_simulations = "1000"
# Function to run the subprocess and process the result
def run_simulation(args):
    shape, theta, sampler, distance, num_simulations = args
    result = subprocess.run(
        ["python", "experiments_auxiliary.py", "--shape", shape, "--theta", theta, "-n", "40000", "-N", num_simulations,
         "--sampler", sampler, "--distance", distance],
        capture_output=True, text=True
    )
    if len(result.stdout) > 0:
        return float(result.stdout)
    else:
        return 0


# Define the parameters for each run
def generate_tasks(shape, thetas, samplers, distances, num_simulations):
    tasks = []
    for theta in thetas:
        for sampler in samplers:
            for distance in distances:
                for _ in range(5):  # Each combination runs 5 times
                    tasks.append((shape, theta, sampler, distance, num_simulations))
    return tasks


# Main function to execute all simulations in parallel
def parallel_run():
    shape = "fluid"
    samplers = ["importance", "MCMC"]
    distances = ["hausdorff", "cubical"]

    # Create task lists for each combination
    all_tasks = generate_tasks(shape, thetas, samplers, distances, num_simulations)

    # Use ProcessPoolExecutor to parallelize all tasks
    with ProcessPoolExecutor() as executor:
        # Execute all tasks and show a single progress bar for all tasks
        results = list(tqdm(executor.map(run_simulation, all_tasks), total=len(all_tasks)))

    # Split the results back into respective lists
    num_thetas = len(thetas)
    num_samplers = len(samplers)
    num_distances = len(distances)
    num_repeats = 5

    # Split results into categories
    res_list_importance_scc = results[:num_thetas * num_repeats]
    res_list_importance_topological = results[num_thetas * num_repeats:num_thetas * 2 * num_repeats]
    res_list_MCMC_scc = results[num_thetas * 2 * num_repeats:num_thetas * 3 * num_repeats]
    res_list_MCMC_topological = results[num_thetas * 3 * num_repeats:]

    # Reshape the flat lists into a list of lists with 5 elements each
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
