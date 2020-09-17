import numpy as np
import scipy.stats
from scipy.stats import norm
import copy
import math


class PutOption:

    # Constructor. Note that p in this assignment is p* on paper, the option price
    def __init__(self, r, T, K, S0, p, n=None):
        # n only matters for the AmericanPutOption case
        self.S0 = S0
        self.r = r
        self.T = T
        self.K = K
        self.p = p
        self.n = n

    # Compute and return option price given parameters
    def compute_price(self, sigma):
        # Overwritten by subclass compute_price methods
        raise NotImplementedError

    # Compute implied volatility with parameters fed into the constructor
    def implied_volatility(self, sigma0=.5, n_iter=20):

        # BISECTION METHOD
        price = self.compute_price(sigma0)  # 1 for initial guess

        # No need to declare python variables outside loops! They are declared implicitly...

        # Calculate initial sigma interval
        if price < self.p:
            sig_low = sigma0
            sig_high = 2 * sigma0
            while self.compute_price(sig_high) <= self.p:  # runs until this quantity > p
                sig_high *= 2
        else:  # price > p in this case
            sig_high = sigma0
            sig_low = sigma0 / 2.0
            while self.compute_price(sig_low) >= self.p:  # runs until this quantity < p
                sig_low /= 2

        # Make sigma converge st compute_price(sigma) = p
        for _ in range(n_iter):
            sig_mid = (sig_low + sig_high) / 2
            if self.compute_price(sig_mid) < self.p:
                sig_low = sig_mid
            else:
                sig_high = sig_mid

        return (sig_low + sig_high) / 2  # By this time the interval is sufficiently small!


class EuropeanPutOption(PutOption):

    # Constructor
    def __init__(self, r, T, K, S0, p):
        super(EuropeanPutOption, self).__init__(r=r, T=T, K=K, S0=S0, p=p, n=None)

    # Black-Scholes formula for European option price. Overrides method in PutOption
    def compute_price(self, sigma):
        d1 = ((self.r + (sigma**2 / 2)) * self.T + np.log(self.S0 / self.K)) / (sigma * (self.T**0.5))
        d2 = ((self.r - (sigma**2 / 2)) * self.T + np.log(self.S0 / self.K)) / (sigma * (self.T**0.5))
        bs = np.exp(-self.r * self.T) * self.K * (1 - norm.cdf(d2)) - self.S0 * (1 - norm.cdf(d1))  # B-S put formula
        print(bs)
        return bs


class AmericanPutOption(PutOption):

    # Constructor (Actually uses n != None here)
    def __init__(self, r, T, K, S0, p, n):
        super(AmericanPutOption, self).__init__(r=r, T=T, K=K, S0=S0, p=p, n=n)

    # n-step Binomial pricing formula. Overrides method in PutOption
    def compute_price(self, sigma):

        dt = self.T / self.n
        rn = np.exp(self.r * dt) - 1.0
        un = np.exp(sigma * math.sqrt(dt))
        dn = 1 / un
        pn = (1 + rn - dn) / (un - dn)

        # Forward Recursion to calculate stock price values
        stock_prices = [[self.S0]]
        for t in range(1, self.n+1):  # iterate from 1 to n time stems
            temp = []
            for i in range(t+1):
                if i == 0:
                    temp.append(stock_prices[t-1][i] * dn)
                else:
                    temp.append(stock_prices[t-1][i-1] * un)
            stock_prices.append(temp)

        final_payoffs = []
        for x in range(self.n + 1):
            final_payoffs.append(max(0, self.K - stock_prices[self.n][x]))

        v = copy.deepcopy(stock_prices)[0:self.n]  # This will become the payoff array
        # (This is messy code but it's an easy way to get an array with the correct dimensions)
        v.append(final_payoffs)

        # Back Recursion Loop
        for t in range(self.n - 1, -1, -1):
            for i in range(t+1):
                exercise = max(0, self.K - stock_prices[t][i])
                cont = (1 / (1 + rn)) * (pn * v[t+1][i+1] + (1 - pn) * v[t+1][i])
                v[t][i] = max(exercise, cont)
        print(v[0][0])
        return v[0][0]


#####################################################################

# Question 3
american_option = AmericanPutOption(r=0.02, T=1/4, K=50, S0=50, p=2.75, n=1000)
print(american_option.implied_volatility())

european_option = EuropeanPutOption(r=0.02, T=1/4, K=50, S0=50, p=2.75)
print(european_option.implied_volatility())

