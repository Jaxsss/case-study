import pandas as pd

# ask for input
balance = int(input('How much money do you have? '))
trade_amount = int(input('What should your per trade amount be? '))

# check if trade amount is not higher than balance
if trade_amount > balance:
    print("You don't have enough balance.")
    quit()

# read csv
df = pd.read_csv('testfile.csv')

# create array with all close values & create EMA list
sma = df['Close'].to_numpy()
ema = []

# function to calculate ema
def calculate_ema(prices, days, smoothing=2):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema

ema16 = calculate_ema(sma, 16)
ema32 = calculate_ema(sma, 32)

# variables
holding = 0
profit = 0
trade = 0
total_profit = 0

# main strategy loop
for x in range(1, len(sma)):
    try:
        if holding == 1:
            zisk = trade_amount + ((trade_amount / 100) * 0.05)
            ztrata = trade_amount - ((trade_amount / 100) * 0.03)
            close_next = df.loc[x, 'Close']
            stock_price_new = close_next * trade
            result = stock_price_new

            if result > zisk:
                profit = stock_price_new - trade_amount
                total_profit += profit
                balance = balance + profit
                holding = 0

            if result < ztrata:
                profit = stock_price_new - trade_amount
                total_profit += profit
                balance = balance + profit
                holding = 0

            continue

        if int(ema32[x]) == int(ema16[x]):
            stock_price = df.loc[x, 'Close']
            trade = trade_amount / stock_price
            holding = 1
    except:
        break

print("Total profit for this strategy is: ", total_profit)