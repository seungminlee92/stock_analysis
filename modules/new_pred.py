import numpy as np
from keras.layers import LSTM, Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split

def windowing(prices, trade_volumes, foreign_pcts, window_size = 5):
    for_pred = []
    real = []
    for i in range(len(prices)-window_size):
        for_pred.append([[prices[i+j], trade_volumes[i+j], foreign_pcts[i+j]] for j in range(window_size)])
        real.append([prices[window_size + i], 
                     trade_volumes[window_size + i], 
                     foreign_pcts[window_size + i]])
    return for_pred, real

def norm_list(data):
    result = [(idx/data[0]-1) for idx in data]
    return result
# def normalize_pred(windowed_pred):
#     result = []
#     for window in windowed_pred:
#         process = []
#         for w in window:
#             norm_data = [((w[step]/window[0][step])-1) for step in range(len(w))]
#             process.append(norm_data)
#         result.append(process)
#     return result

# def normalize_real(windowed_real, windowed_pred):
#     result = []
#     for w in range(len(windowed_real)):
#         result1= [((windowed_real[w][idx]/windowed_pred[w][0][idx])-1) for idx in range(len(windowed_real[0]))]
#         result.append(result1)
#     return result

def mul_norm_pred(normalized_pred):
    result = []
    for window in normalized_pred:
        process = []
        for w in window:
            m = 1
            for idx in w:
                m *= idx
            process.append(m)
        result.append(process)
    return result

def mul_norm_real(normalized_real):
    result = []
    for w in normalized_real:
        m = 1
        for idx in w:
            m *= idx
        result.append(m)
    return result

def denormalize(norm_prices, for_pred):         # 비정규화
    pass

def to_1d_list(data):
    result = []
    for idx in range(len(data)):
        result.append(data[idx][0])
    return result

def pred(df, window_sizer = 5, spliter = 0.7, b_s = 1, epoch = 10):
    # 데이터 추출
    prices = list(df[df.columns[0]])
    trade_volumes = list(df[df.columns[1]])
    foreign_pcts = list(df[df.columns[2]])
    # data normalize
    norm_prices = norm_list(prices)
    norm_volumns = norm_list(trade_volumes)
    norm_foreign = norm_list(foreign_pcts)
    # x, y categorize
    for_x, for_y = windowing(norm_prices, norm_volumns, norm_foreign) 
    # train, test data
    x_train, x_test, y_train, y_test = train_test_split(for_x, norm_prices[5:], test_size=1-spliter)
    # data shaping
    x_train = np.array(mul_x(x_train))
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    y_train = np.array(y_train)
    x_test = np.array(mul_x(x_test))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = np.array(y_test)
    # Modeling
    model = Sequential()
    model.add(LSTM(window_sizer, return_sequences = True, input_shape = (window_sizer, 1)))
    model.add(LSTM(len(x_train), return_sequences = False))
    model.add(Dense(1, activation = 'linear'))
    model.compile(loss = 'mse', optimizer = 'adam')
    model.summary()
    # training
    model.fit(x_train, y_train, 
            validation_data = (x_test, y_test), 
            batch_size = b_s, 
            epochs = 100)
    # predicting
    train_pred = to_1d_list(model.predict(x_train))
    test_pred = to_1d_list(model.predict(x_test))
    denorm_train = [round((idx+1)*prices[0], 2) for idx in train_pred]
    denorm_test = [round((idx+1)*prices[0], 2) for idx in test_pred]
    denorm_test = [denorm_train[-1]] + denorm_test
    
    return denorm_train, denorm_test, len(denorm_test)

def fluctuate_prob(raw_df, test_df, test_len):
    pass

if __name__ == '__main__':
    pass