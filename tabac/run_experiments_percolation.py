from tqdm import tqdm
import subprocess
import pickle
from concurrent.futures import ProcessPoolExecutor

thetas = ["0.15", "0.3", "0.6"]
num_simulations = "1000"

# Function to run the subprocess and process the result
def run_simulation(args):
    shape, theta, sampler, distance, num_simulations = args
    result = subprocess.run(
        ["python", "experiments_auxiliary.py", "--shape", shape, "--theta", theta, "50", "-n", "100", "-N",
         num_simulations, "--sampler", sampler, "--distance", distance],
        capture_output=True, text=True
    )
    return float(result.stdout) if result.stdout else 0


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
    shape = "perc"
    samplers = ["importance", "MCMC"]
    distances = ["scc", "cubical"]

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

    # Define the split points based on the order of tasks
    num_tasks_per_category = num_thetas * num_samplers * num_distances * num_repeats

    res_list_importance_scc = results[:num_thetas * num_repeats]
    res_list_importance_topological = results[num_thetas * num_repeats:num_thetas * 2 * num_repeats]
    res_list_MCMC_scc = results[num_thetas * 2 * num_repeats:num_thetas * 3 * num_repeats]
    res_list_MCMC_topological = results[num_thetas * 3 * num_repeats:]

    # Reshape the flat lists into a list of lists with 5 elements each (as per the original structure)
    def reshape_results(flat_list, num_groups=3, num_per_group=5):
        return [flat_list[i * num_per_group:(i + 1) * num_per_group] for i in range(num_groups)]

    res_list_importance_scc = reshape_results(res_list_importance_scc)
    res_list_importance_topological = reshape_results(res_list_importance_topological)
    res_list_MCMC_scc = reshape_results(res_list_MCMC_scc)
    res_list_MCMC_topological = reshape_results(res_list_MCMC_topological)

    # Save results as a dictionary
    res_dic = {
        "Perc Importance SCC": res_list_importance_scc,
        "Perc Importance topological": res_list_importance_topological,
        "Perc MCMC SCC": res_list_MCMC_scc,
        "Perc MCMC topological": res_list_MCMC_topological
    }

    # Save to file
    with open('perc_' + num_simulations + '.pkl', 'wb') as fp:
        pickle.dump(res_dic, fp)


# Execute the parallel run
if __name__ == "__main__":
    parallel_run()
