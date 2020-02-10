from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup as bs

def del_comma(st):              # 문자의 , 없애는 함수
    ar = st.split(',')
    k = ''
    for i in ar:
       k += i
    return k 

def str2fl(st):
    return float(st)

def stock_1_data(data_len, stock_num):                          # 데이터 1개 파싱
    stock_num =  stock_num # input('종목 코드 입력 : ')
    data_len1 =  data_len # input('가져올 데이터 수 (10 단위로 입력 가능): ')
    data_len2 = int(data_len1) // 10

    # if str(data_len1)[-1] == '0':
    date_list = []
    stock_list = []

    for n in range(data_len2):
        url = f'http://finance.naver.com/item/sise_day.nhn?code={stock_num}&page={n+1}'
        html = urlopen(url)
        source = bs(html.read(), 'html.parser')
        sr_lists = source.find_all('tr')
        for j in sr_lists:
            if j.span != None:
                date_list.append(j.td.text.replace('.', '-'))
                stock_list.append(j.find_all('td', class_ = 'num')[0].text)

    df = pd.Series(stock_list, 
                    index = date_list)
    df = df.map(del_comma)
    df = df.map(str2fl)

    result = pd.DataFrame(df, columns = [stock_num]).sort_index()
    # else:
    #     result = f'데이터는 10배수로만 가져올 수 있습니다. 입력한 수 : {data_len1}'    
    
    return result

def stock_2_data(data_len, stock_num1, stock_num2):             # 데이터 두개 파싱
    stock_num1 = stock_num1 # input('첫 번째 종목 코드 입력 : ')
    stock_num2 = stock_num2 # input('두 번째 종목 코드 입력 : ')
    data_len1 = data_len # input('가져올 데이터 수 (10 단위로 입력 가능): ')
    data_len2 = int(data_len1) // 10

    if str(data_len1)[-1] == '0':
        search_list = [stock_num1, stock_num2]
        date_list = []
        stock_list = []

        for stock_num in search_list: 
            for n in range(data_len2):
                url = f'http://finance.naver.com/item/sise_day.nhn?code={stock_num}&page={n+1}'
                html = urlopen(url)
                source = bs(html.read(), 'html.parser')
                sr_lists = source.find_all('tr')
                for j in sr_lists:
                    if j.span != None:
                        date_list.append(j.td.text.replace('.', '-'))
                        stock_list.append(j.find_all('td', class_ = 'num')[0].text)

            df = pd.Series(stock_list, 
                        index = date_list)
            df = df.map(del_comma)
            df = df.map(str2fl)
            
        stock_1 = df[:int(len(df)/2)]
        stock_2 = df[int(len(df)/2):]
        result = pd.concat([stock_1, stock_2], 
                           axis = 1, 
                           keys = [stock_num1, stock_num2]).sort_index()
    else:
        result = f'데이터는 10배수로만 가져올 수 있습니다. 입력한 수 : {data_len1}'    
    
    return result

def additional_data(data_len, stock_num):
    stock_num =  stock_num
    data_len1 =  data_len
    data_len2 = int(data_len1) // 20

    date_list = []
    price_list = []
    trade_volume_list = []
    foreign_pct_list = []
    for n in range(data_len2):
        url = f'http://finance.naver.com/item/frgn.nhn?code={stock_num}&page={n+1}'
        html = urlopen(url)
        source = bs(html.read(), 'html.parser')
        section = source.find('table', summary = '외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다.')
        sr_lists = section.find_all('tr')
        for j in sr_lists:
            if j.span != None:
                date_list.append(j.td.text.replace('.', '-'))
                price_list.append(j.find_all('td', class_ = 'num')[0].text)
                trade_volume_list.append(j.find_all('td', class_ = 'num')[3].text)
                foreign_pct_list.append(j.find_all('td', class_ = 'num')[7].text[:-1])

    price_list = pd.Series(price_list, index = date_list).map(del_comma).map(str2fl)
    trade_volume_list = pd.Series(trade_volume_list, index = date_list).map(del_comma).map(str2fl)
    foreign_pct_list = pd.Series(foreign_pct_list, index = date_list).map(str2fl)

    result = pd.DataFrame([price_list, trade_volume_list, foreign_pct_list], 
                          index = [stock_num, '거래량', '외국인보유율']).T.sort_index()
    
    return result

def get_stocklist():
    df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    df[df.columns[1]] = df[df.columns[1]].map('{:06d}'.format)
    return df

def change_data(df, key):
    if key in list(df[df.columns[0]]):
        df = df[df.회사명 == key]
        stock_number = str(df[df.회사명 == key][df.columns[1]].values[0])
        return stock_number
    elif key in list(df[df.columns[1]]):
        df = df[df.종목코드 == key]
        stock_name = str(df[df.종목코드 == key][df.columns[0]].values[0])
        return stock_name

if __name__ == '__main__':
    pass
