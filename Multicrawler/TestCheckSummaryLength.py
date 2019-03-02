import glob
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt


rotTomDF = pd.read_csv("C:\\Users\\chris\\OneDrive\\Documenten\\IR_DS2019\\TextProcessing\\PagesProcessedBackUp\\RottenTomatoes.csv")


listSumLength = []
rotTomDF["summary"]

for index, row in rotTomDF.iterrows():
    try:
        summary = row["summary"].split()
        lensum = len(summary)
        listSumLength.append(lensum)
    except:
        print("could not split: ",  row["summary"])


listSumLength.sort()
listSumLength

matplotlib.pyplot.plot(listSumLength)
plot.show()

plt.plot(listSumLength)
plt.show()
