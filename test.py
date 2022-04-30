from getSentiment import getSentiment
import pandas as pd
import matplotlib.pyplot as plt

print("Hello")
dataframe = getSentiment("AAPL")
lines = dataframe.plot(x='date', y='Analysis',kind = 'line')
plt.show()