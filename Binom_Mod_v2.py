import math
import copy


# Computes option values and hedges using the binomial model
# (Initial Price, Number of Steps, Maturity, Annualized IR, Volatility, Strike Price, Indicator: (1 if call,  if put))
def binomial_model(s_0, n, maturity, r, s, strike, call_indicator):

    # b) Starting Step Calculations
    dt = maturity / n  # time between periods
    rn = math.exp(r * dt) - 1.0  # 1-step r
    un = math.exp(s * math.sqrt(dt))
    dn = 1 / un
    pn = (1 + rn - dn) / (un - dn)

    # c) Forward Recursion: All Stock Price Values
    stock_prices = [[s_0]]  # stock price array
    for t in range(1, n+1):
        temp = []
        for i in range(t+1):
            if i == 0:
                temp.append(stock_prices[t - 1][i] * dn)  # compute all downs case
            else:
                temp.append(stock_prices[t - 1][i - 1] * un)  # compute other cases
        stock_prices.append(temp)
    # print(stock_prices)

    # d) Payoff Functions
    # I integrated this part into the binomial model function so it doesn't need
    # a payoff vector as input (Prof. Soner said this was acceptable)
    def call_final_pay(k, price):  # call option payoff function
        return max(0, price - k)

    def put_final_pay(k, price):  # put option payoff function
        return max(0, k - price)

    final_payoffs = []
    if call_indicator == 0:
        for x in range(n+1):
            final_payoffs.append(put_final_pay(strike, stock_prices[n][x]))
    else:
        for x in range(n + 1):
            final_payoffs.append(call_final_pay(strike, stock_prices[n][x]))
    # print(final_payoffs)

    # e) Values and Hedges
    v = copy.deepcopy(stock_prices)[0:n]  # Payoff array, delete the last time step's values
    v.append(final_payoffs)  # Append final payoffs vector from part d)

    h = copy.deepcopy(stock_prices)[0:n]  # Hedge Array (smaller than v array) (Shortcut to get dimensions correct)

    for t in range(n-1, -1, -1):  # Back-recursion loop to calculate all v's
        for i in range(t+1):
            v[t][i] = (1 / (1 + rn)) * (pn * v[t + 1][i + 1] + (1 - pn) * v[t + 1][i])
            h[t][i] = (v[t+1][i+1] - v[t+1][i]) / (stock_prices[t+1][i+1] - stock_prices[t+1][i])

    # print (v)
    return v[0][0]

print(binomial_model(50, 1000, 0.25, 0.02, 0.28903043270111084, 50, 0))




