import math
import copy

"""American Put Function"""


def american_put(strike, sigma, r, s_0, maturity, n):

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
    # print(stock_prices)

    def put_exercise(k, price):  # put exercise function
        return max(0, k - price)

    final_payoffs = []
    for x in range(n+1):
        final_payoffs.append(put_exercise(strike, stock_prices[n][x]))

    # Values and Hedges
    v = copy.deepcopy(stock_prices)[0:n]  # Payoff array, delete the last time step's values
    v.append(final_payoffs)  # Append final payoffs vector from part d)

    strategy = copy.deepcopy(v)[0:n+1]  # Strategy array: 1 if optimal to exercise, 0 if continue
    for j in range(len(strategy[n])):
        strategy[n][j] = 1

    for t in range(n-1, -1, -1):  # Back-recursion loop to calculate all v's
        for i in range(t+1):

            """This is the step where the modification from HW3 comes in"""
            exercise = put_exercise(strike, stock_prices[t][i])
            cont = (1 / (1 + rn)) * (pn * v[t + 1][i + 1] + (1 - pn) * v[t + 1][i])
            v[t][i] = max(exercise, cont)

            if exercise > cont:
                strategy[t][i] = 1
            else:
                strategy[t][i] = 0

    # boundary function for creating a graph
    def boundary(time):
        champ = -1
        for z in range(0, len(strategy[time])):  # iterates over the array for this time length
            if strategy[time][z] == 1:
                champ = stock_prices[time][z]
        return champ

    for t in range(n + 1):
        print ("%s %s" % (t / 1000.0, boundary(t)))

    print(v[0][0])


american_put(30.0, 0.2, 0.035, 30.0, 1.0, 1000)
american_put(50, 0.2874075174331665, 0.02, 50, 0.25, 1000)
# strike, sigma, r, s_0, maturity, n):




