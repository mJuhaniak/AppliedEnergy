
from scipy.stats import entropy
import pandas as pd

PaloAlto = pd.read_csv(r"C:\Users\Martin\Projekt\PaloAlto_modified.csv", low_memory=False)
SD = 0
DE = 0
SD_sparsity = 0
DE_sparsity = 0


def computeSparsity():
    global SD_sparsity, DE_sparsity

    SD_zeros = (SD == 0).sum().sum()
    DE_zeros = (DE == 0).sum().sum()

    SD_sparsity = SD_zeros/(SD.shape[0]*SD.shape[1])
    DE_sparsity = DE_zeros/(DE.shape[0]*DE.shape[1])


def getEntropy():
    global PaloAlto, SD, DE

    counts = SD.to_numpy().flatten(order='C')
    return entropy(counts, base=2)


def prepareData():
    global PaloAlto

    PaloAlto['StartTime'] = pd.to_datetime(PaloAlto['Start Date']).dt.hour
    PaloAlto['Duration'] = PaloAlto['Charging Time (hh:mm:ss)'] / 3600
    PaloAlto['Energy'] = PaloAlto['Energy (kWh)']
    PaloAlto = PaloAlto.round({'Duration': 0, 'Energy': 0})


def createSparsityMatrix():
    global PaloAlto, SD, DE
    SD = PaloAlto.groupby('StartTime')['Duration'].value_counts().unstack('Duration', fill_value=0).reset_index()
    DE = PaloAlto.groupby('Duration')['Energy'].value_counts().unstack('Energy', fill_value=0).reset_index()

    SD.drop(SD.columns[0], axis=1, inplace=True)
    DE.drop(DE.columns[0], axis=1, inplace=True)

    SD.to_csv("SD_sparsity.csv", sep=';')
    DE.to_csv("DE_sparsity.csv", sep=';')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    prepareData()
    createSparsityMatrix()
    computeSparsity()
    print(SD_sparsity)
    print(DE_sparsity)
    print(getEntropy())


    print("--------")
    list = [[3, 0, 0], [0, 2, 0], [0, 0, 1]]
    dframe = pd.DataFrame(list)
    print(dframe)
    flattenedframe = dframe.to_numpy().flatten(order='C')
    print(flattenedframe)
    print(entropy(flattenedframe, base=2))


