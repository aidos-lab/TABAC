import numpy as np

from distances import *
from vicsek_new import Vicsek
from tqdm import tqdm
import matplotlib.pyplot as plt

t = 30
eta = .15

n = 2000
sample_size = 150

def sample_from_vicsek(n, eta, *args, **kwargs):
    rho = 3
    model = Vicsek(int(np.sqrt(n / rho)), rho, .5, eta)
    for i in range(t):
        pos = model.step()[0]
    return pos

dist_avg = []
for j in np.arange(.1,.5,.02):
    eta = j
    y = sample_from_vicsek(n, eta)
    distances = []
    dist = TopologicalDistance()
    for i in tqdm(range(sample_size)):
        s1 = sample_from_vicsek(n, eta)
        d = dist(x=s1, y=y)
        distances.append(d)
    dist_avg.append(np.mean(distances))


x = [t for t in np.arange(.1,.5,.02)]
plt.plot(x,dist_avg)
plt.title("Vicsek model after 30 iterations")
plt.xlabel('Noise parameter eta')
plt.ylabel('Average topological distance to ground truth data')
plt.show()

dist_avg = np.array(dist_avg)
np.save('Vicsek_30_timesteps', dist_avg)