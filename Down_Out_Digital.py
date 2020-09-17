import math
import copy

"""Digital Down and Out Option"""


def down_out_digital(barrier, sigma, r, s_0, maturity, n):

    # Starting Step Calculations
    dt = maturity / n  # time between periods
    rn = math.exp(r * dt) - 1.0  # 1-step r
    un = math.exp(sigma * math.sqrt(dt))
    dn = 1 / un
    pn = (1 + rn - dn) / (un - dn)

    # Forward Recursion: All Stock Price Values
    stock_prices = [[s_0]]  # stock price array
    for t in range(1, n+1): # iterate from 1 to n (time steps)
        temp = []
        for i in range(t+1):
            if i == 0:
                temp.append(stock_prices[t - 1][i] * dn)  # compute all downs case
            else:
                temp.append(stock_prices[t - 1][i - 1] * un)  # compute other cases
        stock_prices.append(temp)

    def digital_barrier(b, price):  # barrier function for final value array
        if price >= b:
            return 1
        else: return 0

    final_payoffs = []
    for x in range(n+1):
        final_payoffs.append(digital_barrier(barrier, stock_prices[n][x]))

    # Values and Hedges
    v = copy.deepcopy(stock_prices)[0:n]  # Payoff array, delete the last time step's values
    v.append(final_payoffs)  # Append final payoffs vector from part d)

    for t in range(n-1, -1, -1):  # Back-recursion loop to calculate all v's
        for i in range(t+1):

            """This is the step where the modification from HW3 comes in"""
            if stock_prices[t][i] < barrier:  # If node is below barrier, set value to 0
                v[t][i] = 0
            else:
                v[t][i] = (1 / (1 + rn)) * (pn * v[t + 1][i + 1] + (1 - pn) * v[t + 1][i])  # Else proceed as usual

    return v[0][0]


print(down_out_digital(15.0, 0.2, 0.035, 30.0, 1.0, 1000))
#  (barrier, sigma, r, s_0, maturity, n)

part_3 = []
for i in range(10, 32, 2):
    part_3.append([i, -math.log(down_out_digital(i, 0.2, 0.035, 30.0, 1.0, 1000))])
print(*part_3, sep = "\n")

