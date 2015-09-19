
from math import sqrt
from scipy.stats import truncnorm


def define_tempo(lower=60, upper=160):

    mu, sigma = (lower+upper)/2, sqrt(pow(upper-lower, 2)/12.)

    upper = (upper-mu)/sigma
    lower = (lower-mu)/sigma

    return truncnorm(lower, upper, loc=mu, scale=sigma).rvs()
