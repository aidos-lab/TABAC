import numpy as np
from scipy.stats import norm

def importance_sampling_estimator(results, theta_true, gamma=10, std=.25):
    numerator = 0.0
    denominator = 0.0
    for result in results:
        theta, dist = result.theta, result.distance
        numerator += np.array(theta) * np.exp(-gamma * dist) * norm.pdf(theta, loc=theta_true, scale=std) * 200
        denominator += np.exp(-gamma * dist) * norm.pdf(theta, loc=theta_true, scale=std) * 200
        theta_pred = numerator / denominator
    return theta_pred