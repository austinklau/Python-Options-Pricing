import math
import copy


# a) Inputs
S0 = input("Initial Stock Price: ")
n = input("Number of Periods: ")
T = input("Maturity: ")
r = input("Interest Rate: ")
s = input("Volatility: ")
payoff = input("Payoff Vector: ")


# b) Starting Step Calculations
dt = T / n  # time between periods
rn = math.exp(r * dt) - 1.0  # 1-step r
un = math.exp(s * math.sqrt(dt))
dn = 1 / un
pn = (1 + rn - dn) / (un - dn)


# c) Forward Recursion: All Stock Price Values
stock_prices = [[S0]]  # stock price array
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
def call_final_pay(strike, price):  # call option payoff function
    return max(0, price - strike)


def put_final_pay(strike, price):  # put option payoff function
    return max(0, strike - price)


ind = input("Type 0 for Put Option, 1 for Call Option: ")
K = input("Strike Price: ")
final_payoffs = []
if ind == 0:
    for x in range(n+1):
        final_payoffs.append(put_final_pay(K, stock_prices[n][x]))
else:
    for x in range(n + 1):
        final_payoffs.append(call_final_pay(K, stock_prices[n][x]))
# print(final_payoffs)


# e) Values and Hedges
v = copy.copy(stock_prices)[0:n]  # Payoff Matrix, delete the last time step's values
v.append(final_payoffs)  # Append final payoffs vector from part d)

for t in range(n-1, -1, -1):  # Back-recursion loop to calculate all v's
    for i in range(t+1):
        v[t][i] = (1 / (1 + rn)) * (pn * v[t + 1][i + 1] + (1 - pn) * v[t + 1][i])

# print (v)
print("vo = " [0][0])


