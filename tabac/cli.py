"""Toy example experiment."""

import argparse

import numpy as np
import pandas as pd

from scipy.stats import norm, multivariate_normal
from helpers import importance_sampling_estimator

from tabac.abc_functors import ImportanceSampler
from tabac.abc_functors import RejectionSampler
from tabac.abc_functors import MCMCSampler

from tabac.distances import TopologicalDistance
from tabac.distances import TopologicalDistanceCubical
from tabac.distances import hausdorff_distance
from tabac.distances import entropy_distance
from tabac.distances import mse_distance
from tabac.distances import rmse_distance
from tabac.distances import ergas_distance
from tabac.distances import scc_distance
from tabac.distances import uqi_distance
from tabac.distances import rase_distance
from tabac.distances import vifp_distance
from tabac.distances import mean_distance
from tabac.distances import std_distance

from tabac.shapes import sample_from_sphere
from tabac.shapes import sample_from_torus
from tabac.shapes import sample_from_percolation

from vicsek_new import *

from fluid import *

import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", default=100, type=int, help="Number of points for each data set"
    )
    parser.add_argument(
        "-N",
        default=250,
        type=int,
        help="Number of samples for rejection sampling procedure",
    )
    parser.add_argument(
        "--distance",
        choices=["topological", "hausdorff","entropy","cubical","mse","uqi","rmse","ergas","scc","rase","vifp","mean","std"],
        help="Select distance to use for simple rejection sampling",
    )
    parser.add_argument(
        "--shape",
        default="sphere",
        choices=["sphere", "torus", "vicsek","perc","fluid"],
        help="Select type of shape to sample from",
    )
    parser.add_argument(
        "--theta",
        nargs="*",
        help="True parameter(s) to estimate, possibly multivariate",
        type=float,
    )
    parser.add_argument(
        "--sampler",
        default="importance",
        choices=["importance", "rejection", "MCMC"],
        help="Select sampler",
    )

    args = parser.parse_args()

    n = args.n
    rng = np.random.default_rng(42)

    sample_fn = sample_from_sphere
    if args.shape == "torus":
        sample_fn = sample_from_torus
    elif args.shape == "perc":
        sample_fn = sample_from_percolation
    elif args.shape == "vicsek":
        sample_fn = sample_from_vicsek
    elif args.shape == "fluid":
        sample_fn = sample_from_fluid

    theta_true = args.theta

    y = sample_fn(n, *theta_true, seed=rng)
    std = .25

    def _simulation_fn():
        theta = [np.abs(norm.rvs(loc=t,scale=std)) for t in theta_true]
        return theta, sample_fn(n, *theta, seed=rng)


    distance_fn = TopologicalDistance()
    if args.distance == "hausdorff":
        distance_fn = hausdorff_distance
    if args.distance == "entropy":
        distance_fn = entropy_distance
    if args.distance == "cubical":
        distance_fn = TopologicalDistanceCubical()
    if args.distance == "mse":
        distance_fn = mse_distance
    if args.distance == "uqi":
        distance_fn = uqi_distance
    if args.distance == "rmse":
        distance_fn = rmse_distance
    if args.distance == "ergas":
        distance_fn = ergas_distance
    if args.distance == "scc":
        distance_fn = scc_distance
    if args.distance == "rase":
        distance_fn = rase_distance
    if args.distance == "vifp":
        distance_fn = vifp_distance
    if args.distance == "mean":
        distance_fn = mean_distance
    if args.distance == "std":
        distance_fn = std_distance

    if args.sampler =="MCMC":
        theta_0, X_0 = _simulation_fn()
        sampler = MCMCSampler(y, sample_fn, distance_fn, args.n)
        results = sampler(args.N, theta_0, X_0)
    else:
        Sampler = (
            ImportanceSampler if args.sampler == "importance" else RejectionSampler
        )
        sampler = Sampler(y, _simulation_fn, distance_fn=distance_fn)
        results = sampler(args.N)


    distances = []

    for result in results:
        distances.append(
            {
                "theta": result.theta,
                "distance": result.distance,
            }
        )

    ################################################
    # Point estimator
    ################################################

    if args.sampler == "MCMC":
        mcmc_estimate = np.mean(np.array([res.theta for res in results]),axis=0)
        print(f"MCMC estimator: {mcmc_estimate}")
    else:
        importance_sampling_estimate = importance_sampling_estimator(results=results, theta_true=theta_true, std=std)
        print(f"Importance Sampling estimator: {importance_sampling_estimate}")

    ################################################
    # Plots
    ################################################

    df = pd.DataFrame.from_records(distances)
    thetas = np.array([np.array(x) for x in df.theta.to_numpy()])

    k = np.array(theta_true).shape[0]
    for i in range(k):
        df["theta"+str(i)] = thetas[:,i]
        df["parameter_distance" + str(i)] = abs(df["theta"+str(i)] - theta_true[i])

    fig,axes = plt.subplots(k,1,squeeze=False)
    sns.set_style("darkgrid")
    for i in range(k):
        ax = sns.scatterplot(ax=axes[i,0],
            x="theta"+str(i),
            y="distance",
            data=df,
            hue="parameter_distance" + str(i),
        )
        ax.set_title('Distances between true and sampled parameter, for parameter '+str(i))
        ax.set(xlabel='theta'+str(i),ylabel='loss function distance')
        #plt.legend(title='distance of theta to true parameter')
    fig.tight_layout()
    plt.show(block=True)
