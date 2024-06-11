"""Functors for calculating distances."""

import numpy as np

from gtda.diagrams import PairwiseDistance
from gtda.homology import VietorisRipsPersistence, CubicalPersistence

from sklearn.metrics import pairwise_distances
from sklearn.neighbors import KernelDensity
from sewar.full_ref import rmse, uqi, ergas, scc, rase,  vifp

def uqi_distance(x,y):
    N = len(x)
    n = int(np.sqrt(N))
    x = x.reshape(n,n)
    y = y.reshape(n,n)
    return uqi(x,y)

def rmse_distance(x,y):
    N = len(x)
    n = int(np.sqrt(N))
    x = x.reshape(n,n)
    y = y.reshape(n,n)
    return rmse(x,y)

def ergas_distance(x,y):
    N = len(x)
    n = int(np.sqrt(N))
    x = x.reshape(n,n)
    y = y.reshape(n,n)
    return ergas(x,y)

def scc_distance(x,y):
    N = len(x)
    n = int(np.sqrt(N))
    x = x.reshape(n,n)
    y = y.reshape(n,n)
    return scc(x,y)

def rase_distance(x,y):
    N = len(x)
    n = int(np.sqrt(N))
    x = x.reshape(n,n)
    y = y.reshape(n,n)
    return rase(x,y)

def vifp_distance(x,y):
    N = len(x)
    n = int(np.sqrt(N))
    x = x.reshape(n,n)
    y = y.reshape(n,n)
    return vifp(x,y)


def entropy(data):
    data = np.array(data)
    data_norm = np.sqrt(np.sum(data*data, axis=1))
    data = data/data_norm[:, None]   # Normalized data to be on unit sphere


    ## estimate pdf using KDE with gaussian kernel
    kde = KernelDensity(kernel='gaussian').fit(data)

    log_p = kde.score_samples(data)  # returns log(p) of data sample
    p = np.exp(log_p)
    p = p/np.sum(p)
    # estimate p of data sample
    entropy = -np.sum(p * np.log(p))
    return entropy

def entropy_distance(x,y):
    return entropy(x)-entropy(y)

def mse_distance(x,y):
    return ((x - y)**2).mean()

def hausdorff_distance(x, y, metric='euclidean'):
    """Calculate Hausdorff distance between point clouds.

    Calculates the Hausdorff distance between two point clouds, i.e. two
    samples (one observed, one simulated).

    Parameters
    ----------
    x : np.array or array_like
        First data set; this is typically the observed data set.

    y : np.array or array_like
        Second data set; this is typically the simulated data set.

    metric : str
        Determines type of metric to calculate between the two point
        clouds. Can be any string understood by
        ``sklearn.metrics.pairwise_distances()``.

    Returns
    -------
    float
        Hausdorff distance between `x` and `y`.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    # Check whether dimensions are compatible.
    if x.shape[1] != y.shape[1]:
        return np.nan

    distances = pairwise_distances(X=x, Y=y)

    d_xy = np.max(np.min(distances, axis=1))
    d_yx = np.max(np.min(distances, axis=0))

    return max(d_xy, d_yx)

def mean_distance(x, y, metric='euclidean'):
    x = np.asarray(x)
    y = np.asarray(y)
    return np.linalg.norm(x.mean()-y.mean())

def std_distance(x, y, metric='euclidean'):
    x = np.asarray(x)
    y = np.asarray(y)
    return np.linalg.norm(x.std()-y.std())


class TopologicalDistance:
    """Functor for calculating distances based on topological concepts.

    The basic idea of this functor is to wrap the calculation of
    topological features, which are subsequently used to assess the
    distance between observed and simulated data.
    """

    def __init__(
        self,
        dimension=1,
        metric='wasserstein',
        sample_metric='euclidean',
    ):
        """Initialise new topological distance calculation functor.

        Parameters
        ----------
        dimension : int
            Maximum dimension for the calculation of topological
            features.

        metric : str
            Which type of metric to calculate between topological
            features. Must be understand by ``PairwiseDistance``
            class.

        sample_metric : str
            Determines type of metric to calculate between individual
            points, thus controlling *how* topological features are
            being calculated. Can be any string understood by
            ``scipy.spatial.distance.pdist()``.
        """
        self.vr = VietorisRipsPersistence(
            homology_dimensions=list(range(dimension + 1)),
            metric=sample_metric,
            n_jobs=-1,
        )
        self.dist = PairwiseDistance(metric=metric)

    def __call__(self, x, y):
        """Calculate topological distance between two samples.

        Parameters
        ----------
        x : np.array or array_like
            First data set; this is typically the observed data set.

        y : np.array or array_like
            Second data set; this is typically the simulated data set.

        Returns
        -------
        float
            Distance between `x` and `y`, calculated according to the
            parameters supplied to the class.
        """

        diagrams = self.vr.fit_transform([x, y])
        distance = self.dist.fit_transform(diagrams)

        return 0.5 * distance.sum()

class TopologicalDistanceCubical:
    """Functor for calculating distances based on topological concepts.

    The basic idea of this functor is to wrap the calculation of
    topological features, which are subsequently used to assess the
    distance between observed and simulated data.
    """

    def __init__(
            self,
            dimension=1,
            metric='wasserstein',
            sample_metric='euclidean',
    ):
        """Initialise new topological distance calculation functor.

        Parameters
        ----------
        dimension : int
            Maximum dimension for the calculation of topological
            features.

        metric : str
            Which type of metric to calculate between topological
            features. Must be understand by ``PairwiseDistance``
            class.

        sample_metric : str
            Determines type of metric to calculate between individual
            points, thus controlling *how* topological features are
            being calculated. Can be any string understood by
            ``scipy.spatial.distance.pdist()``.
        """
        self.vr = CubicalPersistence()
        self.dist = PairwiseDistance(metric=metric)

    def __call__(self, x, y):
        """Calculate topological distance between two samples.

        Parameters
        ----------
        x : np.array or array_like
            First data set; this is typically the observed data set.

        y : np.array or array_like
            Second data set; this is typically the simulated data set.

        Returns
        -------
        float
            Distance between `x` and `y`, calculated according to the
            parameters supplied to the class.
        """
        diagrams = self.vr.fit_transform([x, y])
        distance = self.dist.fit_transform(diagrams)

        return 0.5 * distance.sum()


