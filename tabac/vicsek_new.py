import numpy as np
import scipy as sp
from scipy import sparse
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Vicsek:
    def __init__(self, L, rho, factor, eta):
        self.L = L
        self.rho = rho
        self.factor = factor
        self.eta = eta

        self.N = int(self.rho * self.L ** 2)

        self.r0 = 1.0
        self.deltat = 1.0
        self.v0 = self.r0 / self.deltat * self.factor
        self.iterations = 10000

        state = np.random.get_state()
        np.random.seed(42)
        self.pos = np.random.uniform(0, self.L, size=(self.N, 2))
        self.orient = np.random.uniform(-np.pi, np.pi, size=self.N)
        np.random.set_state(state)

    def animate(self, i):
        print(i)
        global orient
        tree = cKDTree(self.pos, boxsize=[self.L, self.L])
        dist = tree.sparse_distance_matrix(tree, max_distance=self.r0, output_type='coo_matrix')

        # important 3 lines: we evaluate a quantity for every column j
        data = np.exp(orient[dist.col] * 1j)
        # construct  a new sparse marix with entries in the same places ij of the dist matrix
        neigh = sparse.coo_matrix((data, (dist.row, dist.col)), shape=dist.get_shape())
        # and sum along the columns (sum over j)
        S = np.squeeze(np.asarray(neigh.tocsr().sum(axis=1)))

        orient = np.angle(S) + self.eta * np.random.uniform(-np.pi, np.pi, size=self.N)

        cos, sin = np.cos(orient), np.sin(orient)
        self.pos[:, 0] += cos * self.v0
        self.pos[:, 1] += sin * self.v0

        self.pos[self.pos > self.L] -= self.L
        self.pos[self.pos < 0] += self.L

        qv.set_offsets(self.pos)
        qv.set_UVC(cos, sin, orient)
        return qv,

    def plot(self):
        pos = self.pos

        global orient
        orient = self.orient

        fig, ax = plt.subplots(figsize=(6, 6))

        global qv
        qv = ax.quiver(pos[:, 0], pos[:, 1], np.cos(orient[0]), np.sin(orient), orient, clim=[-np.pi, np.pi])

        anim = FuncAnimation(fig, self.animate, np.arange(1, 200), interval=1, blit=True)
        plt.show()

    def step(self):
        global orient
        orient = self.orient

        global pos
        pos = self.pos

        tree = cKDTree(self.pos, boxsize=[self.L, self.L])
        dist = tree.sparse_distance_matrix(tree, max_distance=self.r0, output_type='coo_matrix')

        # important 3 lines: we evaluate a quantity for every column j
        data = np.exp(orient[dist.col] * 1j)
        # construct  a new sparse marix with entries in the same places ij of the dist matrix
        neigh = sparse.coo_matrix((data, (dist.row, dist.col)), shape=dist.get_shape())
        # and sum along the columns (sum over j)
        S = np.squeeze(np.asarray(neigh.tocsr().sum(axis=1)))

        self.orient = np.angle(S) + self.eta * np.random.uniform(-np.pi, np.pi, size=self.N)

        cos, sin = np.cos(self.orient), np.sin(self.orient)
        self.pos[:, 0] += cos * self.v0
        self.pos[:, 1] += sin * self.v0

        self.pos[self.pos > self.L] -= self.L
        self.pos[self.pos < 0] += self.L
        return self.pos, self.orient


t = 5
def sample_from_vicsek(n, eta, *args, **kwargs):
    rho = 3
    model = Vicsek(int(np.sqrt(n / rho)), rho, .5, eta)
    for i in range(t):
        pos = model.step()[0]
    return pos
