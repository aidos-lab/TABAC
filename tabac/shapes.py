"""Shape sampling methods."""

import numpy as np


def embed(data, ambient=50):
    """Embed `data` in `ambient` dimensions.

    Parameters
    ----------
    data : array_like
        Input data set; needs to have shape `(n, d)`, i.e. samples are
        in the rows, dimensions are in the columns.

    ambient : int
        Dimension of embedding space. Must be greater than
        dimensionality of data.

    Returns
    -------
    array_like
        Input array of shape `(n, D)`, with `D = ambient`.

    Notes
    -----
    This function was originally authored by Nathaniel Saul as part of
    the `tadasets` package. [tadasets]_

    References
    ----------
    .. [tadasets] https://github.com/scikit-tda/tadasets
    """
    n, d = data.shape
    assert ambient > d

    base = np.zeros((n, ambient))
    base[:, :d] = data

    # construct a rotation matrix of dimension `ambient`.
    random_rotation = np.random.random((ambient, ambient))
    q, r = np.linalg.qr(random_rotation)

    base = np.dot(base, q)
    return base


def sample_from_sphere(n=100, r=1, d=2, noise=None, ambient=None, seed=None):
    """Sample `n` data points from a `d`-sphere in `d + 1` dimensions.

    Parameters
    -----------
    n : int
        Number of data points in shape.

    d : int
        Dimension of the sphere.

    r : float
        Radius of sphere.

    noise : float or None
        Optional noise factor. If set, data coordinates will be
        perturbed by a standard normal distribution, scaled by
        `noise`.

    ambient : int or None
        Embed the sphere into a space with ambient dimension equal to
        `ambient`. The sphere is randomly rotated into this
        high-dimensional space.

    seed : int, instance of `np.random.Generator`, or `None`
        Seed for the random number generator, or an instance of such
        a generator. If set to `None`, the default random number
        generator will be used.

    Returns
    -------
    torch.tensor
        Tensor of sampled coordinates. If `ambient` is set, array will be
        of shape `(n, ambient)`. Else, array will be of shape `(n, d + 1)`.

    Notes
    -----
    This function was originally authored by Nathaniel Saul as part of
    the `tadasets` package. [tadasets]_

    References
    ----------
    .. [tadasets] https://github.com/scikit-tda/tadasets

    """
    rng = np.random.default_rng(seed)
    data = rng.standard_normal((n, d + 1))

    # Normalize points to the sphere
    data = r * data / np.sqrt(np.sum(data**2, 1)[:, None])

    if noise:
        data += noise * rng.standard_normal(data.shape)

    if ambient is not None:
        assert ambient > d
        data = embed(data, ambient)

    return np.asarray(data)


def sample_from_percolation(n=100, p=.5, gray_level=255, seed=None):
    rng = np.random.default_rng(seed)
    N = n * n
    if p>1:
        p = 1
    data = np.zeros(N)
    idx = np.array([bool(x) for x in np.random.binomial(1, p, N)])

    data[idx] = np.random.randint(1, gray_level, idx.sum())
    return data

def sample_from_torus(n, r=1, R=2, seed=None):
    """Sample points uniformly from torus.

    Parameters
    ----------
    n : int
        Number of points to sample

    r : float
        Radius of the 'tube' of the torus.

    R : float
        Radius of the torus, i.e. the distance from the centre of the
        'tube' to the centre of the torus.

    seed : int, instance of `np.random.Generator`, or `None`
        Seed for the random number generator, or an instance of such
        a generator. If set to `None`, the default random number
        generator will be used.

    Returns
    -------
    torch.tensor of shape `(n, 3)`
        Tensor of sampled coordinates.
    """
    rng = np.random.default_rng(seed)
    angles = []

    while len(angles) < n:
        x = rng.uniform(0, 2 * np.pi)
        y = rng.uniform(0, 1 / np.pi)

        f = (1.0 + (r / R) * np.cos(x)) / (2 * np.pi)

        if y < f:
            psi = rng.uniform(0, 2 * np.pi)
            angles.append((x, psi))

    X = []

    for theta, psi in angles:
        a = R + r * np.cos(theta)
        x = a * np.cos(psi)
        y = a * np.sin(psi)
        z = r * np.sin(theta)

        X.append((x, y, z))

    return np.asarray(X)