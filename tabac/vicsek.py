"""Implementation of Vicsek model."""

import numpy as np

from sklearn.neighbors import NearestNeighbors


class VicsekModel:
    def __init__(self, n, L, v0, eta, seed=None):
        self.rng = np.random.default_rng(seed=seed)
        self.x = self.rng.uniform(0, L, size=(n, 2))
        self.v = np.full(shape=(n, 2), fill_value=v0)
        self.theta = self.rng.uniform(0, 2 * np.pi, size=n)

        # TODO: Make configurable? Most literature keeps those at unity
        # because everything can be rescaled anyway.
        self.dt = 1.0
        self.R = 1.0

        # "Static" parameters
        self.L = L
        self.eta = eta
        self.v0 = v0

    def step(self):
        nn = NearestNeighbors(radius=self.R)
        nn.fit(self.x)

        neighbors = nn.radius_neighbors(self.x, return_distance=False)

        theta = np.asarray(
            [
                (np.sin(self.theta[nb]).sum(), np.cos(self.theta[nb]).sum())
                for nb in neighbors
            ]
        )
        theta = np.arctan2(theta[:, 0], theta[:, 1])

        theta += self.rng.uniform(
            -0.5 * self.eta, 0.5 * self.eta, size=len(self.x)
        )

        self.theta = theta
        self.v = (
            self.v0 * np.asarray([np.cos(self.theta), np.sin(self.theta)]).T
        )

        self.x += self.dt * self.v

        # Check and restore boundary conditions if necessary.
        self.x[self.x < 0] += self.L
        self.x[self.x > self.L] -= self.L

        return self.x


########################################################################
# HIC SVNT DRACONES
########################################################################

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

model = VicsekModel(300, 25, 0.03, 0.10)

fig, ax = plt.subplots()
pos = ax.quiver(
    model.x[:, 0], model.x[:, 1], np.cos(model.theta), np.sin(model.theta)
)


def animate(i):
    x = model.step()
    pos.set_offsets(x)
    pos.set_UVC(np.cos(model.theta), np.sin(model.theta))

    return (pos,)


anim = FuncAnimation(fig, animate, np.arange(1, 10000), interval=1, blit=True)

plt.show()
