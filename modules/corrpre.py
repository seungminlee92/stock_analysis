import scipy.stats as sc
import numpy as np
from keras.layers import LSTM, Dense
from keras.models import Sequential

def data_corr(data):
    slope, intercept, r_value, p_value, stderr = sc.linregress(data[data.columns[0]], data[data.columns[1]])
    result = [slope, intercept, r_value, p_value, stderr]
    return result

def windowing(prices, window_size = 50):    # 입력된 데이터를 50개씩 리스트화 시켜 리스트로
    for_pred = []
    real_prices = []
    for i in range(len(prices) - window_size):
        for_pred.append([prices[i+j] for j in range(window_size)])
        real_prices.append(prices[window_size + i])
    return for_pred, real_prices

def normalize_list(windowed_prices):        # 나누어진 데이터를 각 1번째 데이터로 정규화
    result = []
    for window in windowed_prices:
        normalized_data = [((float(p)/float(window[0]))-1) for p in window]
        result.append(normalized_data)
    return result

def normalize_single(real_prices, for_pred):
    result = []
    for idx in range(len(real_prices)):
        normalized_sdata = real_prices[idx]/for_pred[idx][0]-1
        result.append(normalized_sdata)
    return result

def denormalize(norm_prices, for_pred):         # 비정규화
    result = []
    for idx in range(len(norm_prices)):
        denormalized_data = round((norm_prices[idx]+1)*for_pred[idx][0], 2)
        result.append(denormalized_data)
    return result

def to_1d_list(data):
    result = []
    for idx in range(len(data)):
        result.append(data[idx][0])
    return result

def pred(df, window_sizer, spliter, b_s = 1, epoch = 10):
    # 종가 데이터 추출
    prices = list(df[df.columns[0]])
    # 분석데이터, 비교데이터 분류
    for_pred, real_prices = windowing(prices, window_sizer)
    # 정규화
    norm_for_pred = np.array(normalize_list(for_pred))
    norm_real_prices = np.array(normalize_single(real_prices, for_pred))
    
    train_test_split = int(len(for_pred)*spliter)
    # train data
    x_train = norm_for_pred[:train_test_split, :]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    y_train = norm_real_prices[:train_test_split]
    # test data
    x_test = norm_for_pred[train_test_split:, :]
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = norm_real_prices[train_test_split :]
    # Modeling
    model = Sequential()
    model.add(LSTM(window_sizer, return_sequences = True, input_shape = (window_sizer, 1)))
    model.add(LSTM(64, return_sequences = True))
    model.add(LSTM(64, return_sequences = False))
    model.add(Dense(1, activation = 'linear'))
    model.compile(loss = 'mse', optimizer = 'adam')
    model.summary()
    # training
    model.fit(x_train, y_train, 
              validation_data = (x_test, y_test), 
              batch_size = b_s, 
              epochs = epoch)
    # prediction
    train_pred = to_1d_list(model.predict(x_train))
    test_pred = to_1d_list(model.predict(x_test))
    
    denorm_train_pred = denormalize(train_pred, for_pred)
    denorm_test_pred = [denorm_train_pred[-1]] + denormalize(test_pred, for_pred)
    return denorm_train_pred, denorm_test_pred, len(denorm_test_pred)

def fluctuate_prob(raw_df, test_df, test_len):
    rdf = list(raw_df[raw_df.columns[1]][-test_len:])
    tdf = list(test_df[test_df.columns[1]])
    idx = [['i_i', 'i_d', 'i_f'], 
           ['d_i', 'd_d', 'd_f'], 
           ['f_i', 'f_d', 'f_f']]
    nums = [[0, 0, 0], 
            [0, 0, 0], 
            [0, 0, 0]]
    for i in range(len(tdf)):
        if rdf[i] == 'increased':
            if tdf[i] == 'increased':
                nums[0][0] += 1
            elif tdf[i] == 'decreased':
                nums[0][1] += 1
            else:
                nums[0][2] += 1
        elif rdf[i] == 'deceased':
            if tdf[i] == 'increased':
                nums[1][0] += 1
            elif tdf[i] == 'decreased':
                nums[1][1] += 1
            else:
                nums[1][2] += 1
        elif rdf[i] == 'frozen':
            if tdf[i] == 'increased':
                nums[2][0] += 1
            elif tdf[i] == 'decreased':
                nums[2][1] += 1
            else:
                nums[2][2] += 1
    dic = dict(zip(idx[0]+idx[1]+idx[2], nums[0]+nums[1]+nums[2]))
    return dic

if __name__ == '__main__':
    pass