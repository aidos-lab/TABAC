"""Approximate Bayesian Computation methods."""

from collections import namedtuple
from tqdm import tqdm
from scipy.stats import norm, multivariate_normal
import numpy as np


class ABCResult(namedtuple(
        'ABCResult',
        [
            'distance',
            'theta',
            'sample'
        ],
    )
):
    """ABC result storage class."""

    __slots__ = ()


class RejectionSampler:
    """Rejection sampler for Approximate Bayesian Computation.

    This generic functor wraps the standard rejection sampling algorithm
    for Approximate Bayesian Computation. It requires a function for the
    calculation of distances between observed and simulated samples, and
    optionally a threshold for rejecting samples. If the client does not
    provide a threshold, all samples will be returned.
    """

    def __init__(self, y, simulation_fn, distance_fn, epsilon=None):
        """Create new rejection sampler.

        Parameters
        ----------
        simulation_fn : callable
            Function for simulating a new sample. Calling ``simulation_fn()``
            needs to result in a tuple consisting of the parameters of
            the generated sample as well as the sample itself. The
            sample needs to be of the same type as `y`.

        distance_fn : callable
            Function for calculating the distance between observed and
            simulated samples. Calling ``distance_fn(y, z)`` needs to
            yield a scalar value.

        epsilon : float or None
            Rejection threshold. If set to `None`, the sampling
            procedure will return all samples.
        """
        self.y = y
        self.simulation_fn = simulation_fn
        self.distance_fn = distance_fn
        self.epsilon = epsilon

    def __call__(self, n_samples):
        """Perform rejection sampling for a number of samples.

        Parameters
        ----------
        n_samples : int
            Number of samples to simulate for the rejection sampling
            procedure.

        Returns
        -------
        List of tuples
            A list of tuples, with the first entry of each tuple
            corresponding to the distance of the simulated sample
            to the observed sample, and the second entry corresponding
            to the sample itself. If a rejection threshold has been set,
            only samples that fall below the threshold will be returned.
        """
        samples = [
            self.simulation_fn()
            for _ in tqdm(range(n_samples), desc='Sample simulation')
        ]

        distances = [
            self.distance_fn(self.y, sample[1])
            for sample in tqdm(samples, desc='Distance calculation')
        ]

        if self.epsilon is not None:
            return [
                ABCResult(d, s[0], s[1])
                for d, s in zip(distances, samples) if d <= self.espilon
            ]
        else:
            return [
                ABCResult(d, s[0], s[1])
                for d, s in zip(distances, samples)
            ]


class ImportanceSampler:
    """Importance sampler for Approximate Bayesian Computation.

    This generic functor wraps our new importance sampling algorithm for
    Approximate Bayesian Computation. It requires a function for getting
    distances between observed and simulated samples.
    """

    def __init__(self, y, simulation_fn, distance_fn, omega=1.0):
        """Create new importance sampler.

        Parameters
        ----------
        simulation_fn : callable
            Function for simulating a new sample. Calling ``simulation_fn()``
            needs to result in a tuple consisting of the parameters of
            the generated sample as well as the sample itself. The
            sample needs to be of the same type as `y`.

        distance_fn : callable
            Function for calculating the distance between observed and
            simulated samples. Calling ``distance_fn(y, z)`` needs to
            yield a scalar value.
        """
        self.y = y
        self.simulation_fn = simulation_fn
        self.distance_fn = distance_fn

    def __call__(self, n_samples):
        """Perform importance sampling for a number of samples.

        Parameters
        ----------
        n_samples : int
            Number of samples to simulate for the importance sampling
            procedure.

        Returns
        -------
        List of tuples
            A list of tuples, with the first entry of each tuple
            corresponding to the distance of the simulated sample
            to the observed sample, and the second entry corresponding
            to the sample itself.
        """
        samples = [
            self.simulation_fn()
            for _ in tqdm(range(n_samples), desc='Sample simulation')
        ]

        distances = [
            self.distance_fn(self.y, sample[1])
            for sample in tqdm(samples, desc='Distance calculation')
        ]

        return [
            ABCResult(d, s[0], s[1])
            for d, s in zip(distances, samples)
        ]



class MCMCSampler:
    """MCMC sampler for Approximate Bayesian Computation.

    This generic functor wraps our new MCMC sampling algorithm for
    Approximate Bayesian Computation. It requires a function for getting
    distances between observed and simulated samples.
    """

    def __init__(self, y, sample_fn, distance_fn, n, omega=1.0):
        """Create new importance sampler.

        Parameters
        ----------
        sample_fn : Sample function, must return an array-type object
        of shape `(n,d)`, where `n` is the number of samples, and
        `d` is the dimension of the respective sample point.

        distance_fn : callable
            Function for calculating the distance between observed and
            simulated samples. Calling ``distance_fn(y, z)`` needs to
            yield a scalar value.
        """
        self.n = n
        self.y = y
        self.sample_fn = sample_fn
        self.distance_fn = distance_fn


    def get_sample_MCMC(self,theta_0, X_0):
        std = .25
        U = np.random.uniform(0, 1)
        rng = np.random.default_rng(42)
        gamma = 10
        l = len(theta_0)
        cov = np.zeros((l, l))
        np.fill_diagonal(cov, (l, l), wrap=True)
        theta_candidate = [np.abs(norm.rvs(loc=t, scale=std)) for t in theta_0]
        X_candidate = self.sample_fn(self.n, *theta_candidate, seed=rng)
        numerator = np.exp(-gamma * self.distance_fn(X_candidate, self.y)) * multivariate_normal.pdf(theta_0,
                                                                                           mean=theta_candidate,
                                                                                           cov=cov)
        denominator = np.exp(-gamma * self.distance_fn(X_0, self.y)) * multivariate_normal.pdf(theta_candidate, mean=theta_0,
                                                                                     cov=cov)
        ratio = numerator / denominator
        if ratio > U:
            theta_0 = theta_candidate
            X_0 = X_candidate
        return theta_0, X_0

    def __call__(self, n_samples, theta_0, X_0):
        """Perform importance sampling for a number of samples.

        Parameters
        ----------
        n_samples : int
            Number of samples to simulate for the importance sampling
            procedure.

        Returns
        -------
        List of tuples
            A list of tuples, with the first entry of each tuple
            corresponding to the distance of the simulated sample
            to the observed sample, and the second entry corresponding
            to the sample itself.
        """
        samples = []
        for _ in tqdm(range(n_samples)):
            samples.append((theta_0,X_0))
            theta_0,X_0 = self.get_sample_MCMC(theta_0,X_0)

        distances = [
            self.distance_fn(self.y, sample[1])
            for sample in tqdm(samples, desc='Distance calculation')
        ]

        return [
            ABCResult(d, s[0], s[1])
            for d, s in zip(distances, samples)
        ]