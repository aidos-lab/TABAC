# Bayesian Computation Meets Topology

This file is intended to explain how to run and reproduce the
experiments shown in the paper. Moreover, a command line interface
is provided for the purpose of demonstration.

## Installation

```console
$ poetry install
```

Alternatively, `pip install .` should also work, but be aware that this
might install things into the wrong virtual environment.

## Experiments

We now describe how to reproduce the main experiments.
The experiments for torus and sphere should take only a few
minutes, depending on your machine. The experiments for
percolation and Vicsek model might take longer, up to several 
hours depending on the parameter configuration.

### Torus

The experiment for the torus can be run by:

```console
$ poetry run python tabac/cli.py [--shape torus] [-h] [--theta r R] [-n N] [-N N] [--distance {topological,hausdorff,mean,std}] [--sampler {importance,MCMC,rejection}] 

optional arguments:
  -h, --help           show this help message and exit
  --theta r R	  specify parameters to be estimated. In this case, `r' is the inner radius and `R' is the outer radius
  			  of the torus.
  -n N                  Number of points for each data set
  -N N                  Number of samples for rejection sampling procedure
  --distance {topological,hausdorff,mean,std}
                        Select either L2-distance between corresponding persistence diagrams, Hausdorff distance between 
                        the resulting point clouds or L2 distance between the mean/standard deviation summary statistics of the 
                        respective data.
  --sampler {importance,MCMC,rejection}
  			Select either importance sampling, MCMC sampling or rejection sampling.
```

For example, the experiment for the torus with inner radius 5, outer radius 10 and w.r.t. the Hausdorff distance
and with importance sampling can be run by:

```console
$ poetry run python tabac/cli.py --shape torus --theta 5 10 -n 100 -N 250 --sampler importance --distance hausdorff
```

This creates a plot that shows the Hausdorff distance
with respect to the `theta` parameter(s) (here, the radii of the torus),
and the estimated parameters are printed out.

### Sphere

The experiment for the sphere can be run by:

```console
$ poetry run python tabac/cli.py [--shape sphere] [-h] [--theta r] [-n N] [-N N] [--distance {topological,hausdorff,mean,std}] [--sampler {importance,MCMC,rejection}] 

optional arguments:
  -h, --help           show this help message and exit
  --theta r 		  specify parameters to be estimated. In this case, `r' is the radius
  			  of the sphere.
  -n N                  Number of points for each data set
  -N N                  Number of samples for rejection sampling procedure
  --distance {topological,hausdorff,mean,std}
                        Select either L2-distance between corresponding persistence diagrams, Hausdorff distance between 
                        the resulting point clouds or L2 distance between the mean/standard deviation summary statistics of the 
                        respective data.
  --sampler {importance,MCMC,rejection}
  			Select either importance sampling, MCMC sampling or rejection sampling.
```

For example, the experiment for the sphere with radius 1 and w.r.t. the topological distance
and with MCMC sampling can be run by:

```console
$ poetry run python tabac/cli.py --shape sphere --theta 1 -n 100 -N 250 --sampler MCMC --distance topological
```

This creates a plot that shows the topological distance
with respect to the `theta` parameter(s) (here, the radius of the sphere),
and the estimated parameters are printed out.

### Percolation model

The experiments for the percolation model can be run by:

```console
$ poetry run python tabac/cli.py [--shape perc] [-h] [--theta p v] [-n N] [-N N] [--distance {cubical,scc,mean,std}] [--sampler {importance,MCMC,rejection}] 

optional arguments:
  -h, --help           show this help message and exit
  --theta p v	  specify parameters to be estimated. In this case, `p' is the probability for a pixel to be non-zero, and `v' is the maximum
  			  greyscale value.
  -n N                  Number of points for each data set
  -N N                  Number of samples for rejection sampling procedure
  --distance {cubical,scc,mean,std}
                        Select either L2-distance between corresponding persistence diagrams(w.r.t. cubical persistence),
                        SCC distance between the resulting images, or L2 distance between the mean/standard deviation summary statistics of the 
                        respective data
  --sampler {importance,MCMC,rejection}
  			Select either importance sampling, MCMC sampling or rejection sampling.
```

For example, the experiment for the percolation model with p=0.6, a maximum greyscale value of 50 and w.r.t. the topological distance
and with MCMC sampling can be run by:

```console
$ poetry run python tabac/cli.py --shape perc --theta 0.6 50 -n 100 -N 250 --sampler MCMC --distance cubical
```

This creates a plot that shows the topological distance
with respect to the `theta` parameter(s) (here, the probability for a pixel to be non-zero, and the maximum greyscale value),
and the estimated parameters are printed out.

### Vicsek model

The experiments for the Vicsek model can be run by:

```console
$ poetry run python tabac/cli.py [--shape vicsek] [-h] [--theta eta] [-n N] [-N N] [--distance {topological,hausdorff,mean,std}] [--sampler {importance,MCMC,rejection}] 

optional arguments:
  -h, --help           show this help message and exit
  --theta eta	  specify parameters to be estimated. In this case, `eta' is the noise parameter in the model.
  -n N                  Number of points for each data set
  -N N                  Number of samples for rejection sampling procedure
  --distance {topological,hausdorff,mean,std}
                        Select either L2-distance between corresponding persistence diagrams,
                        Hausdorff distance between 
                        the resulting point clouds or L2 distance between the mean/standard deviation summary statistics of the 
                        respective data.
  --sampler {importance,MCMC,rejection}
  			Select either importance sampling, MCMC sampling or rejection sampling.
```

For example, the experiment for the Vicsek model with eta=0.15 and w.r.t. the Hausdorff distance
and with importance sampling can be run by:

```console
$ poetry run python tabac/cli.py --shape vicsek --theta 0.15 -n 100 -N 250 --sampler importance --distance hausdorff
```

This creates a plot that shows the topological distance
with respect to the `theta` parameter(s) (here, the noise parameter in the model),
and the estimated parameters are printed out.
The experiment calculates the results after 50 iterations of the model. This parameter
can be adjusted in the `vicsek_new.py' file, by changing `t = 50' to a different iteration
value.


### Fluid model

The experiments for the Lattice Boltzmann model can be run by:

```console
$ poetry run python tabac/cli.py [--shape fluid] [-h] [--theta eta] [-n N] [-N N] [--distance {cubical,hausdorff,mean,std}] [--sampler {importance,MCMC,rejection}] 

optional arguments:
  -h, --help           show this help message and exit
  --theta eta	  specify parameters to be estimated. In this case, `eta' is the noise parameter for the initialisation in the model.
  -n N                  Number of points for each data set (we set this to 40000 in our experiments)
  -N N                  Number of samples for rejection sampling procedure
  --distance {topological,hausdorff,mean,std}
                        Select either L2-distance between corresponding persistence diagrams,
                        Hausdorff distance between 
                        the resulting point clouds or L2 distance between the mean/standard deviation summary statistics of the 
                        respective data
  --sampler {importance,MCMC,rejection}
  			Select either importance sampling, MCMC sampling or rejection sampling.
```

For example, the experiment for the fluid model with eta=0.3 and w.r.t. the L2 distance between the mean summary statistics
and with importance sampling can be run by:

```console
$ poetry run python tabac/cli.py --shape fluid --theta 0.3 -n 40000 -N 250 --sampler importance --distance mean
```

This creates a plot that shows the topological distance
with respect to the `theta` parameter(s) (here, the noise parameter in the model),
and the estimated parameters are printed out.
The experiment calculates the results after 3000 iterations of the model. This parameter
can be adjusted in the `fluid.py' file, by changing `Nt = 3000' to a different iteration
value.

