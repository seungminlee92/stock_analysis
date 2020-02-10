import sys

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QTableView


class df_tableView(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent = None):
        return self._data.shape[0]

    def columnCount(self, parnet = None):
        return self._data.shape[1]

    def data(self, index, role = Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

def add_index(df, stock_name):
    df = df.reset_index().rename(columns = {'index':'날짜',
                                            df.columns[0]: f'{stock_name}'})
    return df

def add_fluctuate(df):
    price = list(df[df.columns[0]])

    result = [0]
    for idx in range(len(price)-1):
        if price[idx] < price[idx+1]:
            r = 'increased'
        elif price[idx] > price[idx+1]:
            r = 'decreased'
        else: r = 'frozen'
        result.append(r)
        
    df['fluctuate'] = result

    return df

def make_pd(lists, index, column_name):
    df = pd.DataFrame(data = lists, 
                      index = index, 
                      columns = [column_name])
    return df

if __name__ == '__main__':
    pass
