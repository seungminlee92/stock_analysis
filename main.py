import os
import sys
import time

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager, rc, rcParams
from numpy import polyval
from PyQt5 import uic
from PyQt5.QtWidgets import *

from modules.corrpre import data_corr#, fluctuate_prob, pred
from modules.get_data import change_data, get_stocklist, stock_1_data, stock_2_data
from modules.table_view import add_fluctuate, add_index, df_tableView, make_pd

from UI.design import Ui_MainWindow

font_name = font_manager.FontProperties(
    fname = 'c:/Windows/Fonts/malgun.ttf'
).get_name()
rc('font', family = font_name)
rcParams['axes.unicode_minus'] = False

# Ui_MainWindow = uic.loadUiType('UI/20.01.11.ui')[0]

class WindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('v.20.01.11')
        
        # global values
        self.stock_list = get_stocklist()
        self.empty_df = pd.DataFrame()
        
        # UI Buttons
        # tab_1 : 종목 리스트 및 코드 검색
        self.Load_data_btn1.clicked.connect(self.load_data)
        self.stock_name1.returnPressed.connect(self.find_number)
        self.Search_btn1.clicked.connect(self.find_number)
        self.stock_name1.setEnabled(False)
        self.stock_num1.setEnabled(False)
        self.Search_btn1.setEnabled(False)

        # tab_2 : 데이터 검색 및 추출
        self.Search_btn2.clicked.connect(self.copy_data_s)
        self.Reset_btn2.clicked.connect(self.stop_search)
        self.data_len2.returnPressed.connect(self.copy_data_s)
        self.stock_num2.returnPressed.connect(self.copy_data_s)
        self.save_btn2.clicked.connect(self.save2csv)
        self.Reset_btn2.setEnabled(False)
        self.label2_3.setEnabled(False)
        self.start_date2.setEnabled(False)
        self.label2_4.setEnabled(False)
        self.end_date2.setEnabled(False)
        self.label2_5.setEnabled(False)
        self.save_btn2.setEnabled(False)
        
        self.result = self.stock_num_list = ''
        
        # tab_3 : 두 종목 상관관계 분석
        self.Start_btn3.clicked.connect(self.start_corr_stats)
        self.Reset_btn3.clicked.connect(self.stop_corr)
        self.show_graph_btn3.clicked.connect(self.show_corr)
        self.data_len3.returnPressed.connect(self.start_corr_stats)
        self.stock_num3_1.returnPressed.connect(self.start_corr_stats)
        self.stock_num3_2.returnPressed.connect(self.start_corr_stats)
        self.Reset_btn3.setEnabled(False)
        self.label3_4.setEnabled(False)
        self.start_date3.setEnabled(False)
        self.label3_5.setEnabled(False)
        self.end_date3.setEnabled(False)
        self.label3_6.setEnabled(False)
        self.stock.setEnabled(False)
        self.cor.setEnabled(False)
        self.show_graph_btn3.setEnabled(False)
        
        self.corr_list = self.stock_prices = self.stock_name_list = self.data_len = ''

        # # tab_4 : 주가 예측
        # #action btns
        # self.Start_btn4.clicked.connect(self.pre_pred)
        # self.Reset_btn4.clicked.connect(self.stop_pred)
        # self.start_pred_btn4.clicked.connect(self.start_pred)
        # self.data_len4.returnPressed.connect(self.pre_pred)
        # self.stock_num4.returnPressed.connect(self.pre_pred)
        # self.show_graph_btn4.clicked.connect(self.show_pred)
        # self.Reset_btn4.setEnabled(False)
        # self.label4_3.setEnabled(False)
        # self.start_date4.setEnabled(False)
        # self.label4_4.setEnabled(False)
        # self.end_date4.setEnabled(False)
        # self.label4_5.setEnabled(False)
        # self.window_sizer.setEnabled(False)
        # self.w_s_default.setEnabled(False)
        # self.w_s_manual.setEnabled(False)
        # self.spliter.setEnabled(False)
        # self.spliter_default.setEnabled(False)
        # self.spliter_manual.setEnabled(False)
        # self.b_s.setEnabled(False)
        # self.b_s_default.setEnabled(False)
        # self.b_s_manual.setEnabled(False)
        # self.epoch.setEnabled(False)
        # self.epoch_default.setEnabled(False)
        # self.epoch_manual.setEnabled(False)
        # self.start_pred_btn4.setEnabled(False)
        # self.show_graph_btn4.setEnabled(False)
        
        # self.w_s = self.train_pred = self.test_pred = self.test_len = '' 
    # UI Actions
    # tab1
    def load_data(self):
        self.stock_name1.setEnabled(True)
        self.Search_btn1.setEnabled(True)
        self.stock_num1.setEnabled(True)
        df = self.stock_list
        
        self.result1.setText(f'{len(df)}개의 데이터를 불러왔습니다.')
    
        model = df_tableView(df)
        self.tableView1.setModel(model)
        
    def find_number(self):
        df = self.stock_list
        stock_name = self.stock_name1.text().upper()
        model = df_tableView(df.head(0))
        stock_num = ''

        if len(stock_name) == 0:
            result = '입력된 검색어가 없습니다.'
        else:
            similar = []
            names = list(df[df.columns[0]])
            # names += [idx.lower() for idx in names]
            for idx in names:
                # if stock_name in idx or stock_name in idx.lower():
                if stock_name in idx:
                    # similar.append(idx.upper())
                    similar.append(idx)
                    
            if len(similar) == 0:
                result = '일치하는 종목이 없습니다.'
            elif len(similar) == 1:
                stock_num = change_data(df, stock_name)
                df = df[df.회사명 == stock_name]
                model = df_tableView(df)
                result = f'{stock_name}에 대한 검색을 완료했습니다.'
            else:
                df1 = pd.DataFrame()
                for name in similar:
                    df2 = df[df.회사명 == name]
                    df1 = pd.concat([df1,df2], ignore_index = True)
                model = df_tableView(df1)
                result = f'{stock_name}과(와) 유사한 항목에 대한 검색을 완료했습니다.'
        self.tableView1.setModel(model)
        self.stock_num1.setText(stock_num)
        self.result1.setText(result)
        
    # tab2
    def copy_data_s(self):
        data_len = self.data_len2.text()
        stock_num = str(self.stock_num2.text())
        
        df = self.stock_list
        text = ''
        try:
            if len(str(data_len)) == 0:
                text = '불러올 데이터 갯수를 입력하세요.'
            elif len(str(stock_num)) == 0:
                text = '종목 코드를 입력하세요.'
            elif data_len.isdigit() == False:
                text = '데이터 갯수는 숫자로만 입력가능합니다'
            elif stock_num.isdigit() == False:
                text = '종목코드는 숫자로만 입력가능합니다.'
            elif int(data_len) % 10 != 0:
                text = '올바른 데이터 갯수가 아닙니다. (10의 배수로만 입력가능)'
            elif stock_num not in list(df[df.columns[1]]):
                raise KeyError
            else:
                self.Reset_btn2.setEnabled(True)
                self.data_len2.setEnabled(False)
                self.label2_3.setEnabled(True)
                self.start_date2.setEnabled(True)
                self.label2_4.setEnabled(True)
                self.end_date2.setEnabled(True)
                self.label2_5.setEnabled(True)
                self.save_btn2.setEnabled(True)

                if len(self.stock_num_list) == 0:
                    self.result = stock_1_data(data_len, stock_num)
                    self.stock_num_list = []
                    
                    stock_name = change_data(df, stock_num)
                    self.result_ = add_index(self.result, stock_name)
                    text = f'{data_len}개의 {stock_name} 데이터를 불러왔습니다.'
                    # print(list(self.result.co))
                    self.start_date2.setText(self.result.index[0])
                    self.end_date2.setText(self.result.index[-1])
                else:
                    if stock_num not in self.stock_num_list:
                        add = stock_1_data(data_len, stock_num)
                        stock_name = change_data(df, stock_num)
                        add = add_index(add, stock_name)
                        self.result_ = pd.merge(self.result_, add[add.columns[1]],
                                                how = 'outer', 
                                                left_index = True, 
                                                right_index = True)
                        text = f'{data_len}개의 {stock_name} 데이터를 불러왔습니다.'
                    else:
                        text = f'이미 존재하는 종목입니다.'
                        self.stock_num_list.remove(stock_num)

                self.stock_num_list.append(stock_num)
                model = df_tableView(self.result_)
                self.tableView2.setModel(model)
        except KeyError:
            text = '존재하지 않는 종목 코드 입니다. (첫번째 탭에서 확인가능)'
        finally:
            self.result2_1.setText(text)

    def stop_search(self):
        # model = df_tableView(self.empty_df)
        text = '초기화되었습니다.'
        
        self.Search_btn2.setEnabled(True)
        self.Reset_btn2.setEnabled(False)
        self.data_len2.setEnabled(True)
        self.stock_num2.setEnabled(True)
        self.label2_3.setEnabled(False)
        self.start_date2.setEnabled(False)
        self.label2_4.setEnabled(False)
        self.end_date2.setEnabled(False)
        self.label2_5.setEnabled(False)
        self.save_btn2.setEnabled(False)

        self.result2_1.setText(text)
        self.result2_2.setText('')
        # self.tableView2.setModel(model)
        self.stock_num_list = self.result = ''

    def save2csv(self):
        
        folderPath = QFileDialog.getExistingDirectory()
        folderPath = os.path.realpath(folderPath)

        self.result.to_csv(f'{folderPath}/data.csv', 
                      mode = 'w', 
                      index = False, 
                      encoding = 'euc-kr')
        
        self.result2_2.setText(f'저장 위치 : {folderPath}')

    # tab3
    def start_corr_stats(self): # 상관계수 출력
        self.data_len = self.data_len3.text()
        self.corr_list = []
        stock_num1 = str(self.stock_num3_1.text())
        stock_num2 = str(self.stock_num3_2.text())
        df = self.stock_list
        try:
            if len(str(self.data_len)) == 0:
                text = '불러올 데이터 갯수를 입력하세요.'
            elif len(str(stock_num1)) == 0:
                text = '종목 코드 1을 입력하세요.'
            elif len(str(stock_num2)) == 0:
                text = '종목 코드 2를 입력하세요.'
            elif stock_num1 == stock_num2:
                text = '같은 종목 코드를 넣을 수 없습니다.'
            elif self.data_len.isdigit() == False:
                text = '데이터 갯수는 숫자로만 입력가능합니다'
            elif stock_num1.isdigit() == False:
                text = '종목코드는 숫자로만 입력가능합니다.'
            elif stock_num2.isdigit() == False:
                text = '종목코드는 숫자로만 입력가능합니다.'
            elif int(self.data_len) % 10 != 0:
                text = '올바른 데이터 갯수가 아닙니다. (10의 배수로만 입력가능)'
            elif stock_num1 not in list(df[df.columns[1]]):
                reason = stock_num1
                raise KeyError
            elif stock_num2 not in list(df[df.columns[1]]):
                reason = stock_num2
                raise KeyError
            else:
                self.Start_btn3.setEnabled(False)
                self.Reset_btn3.setEnabled(True)
                self.data_len3.setEnabled(False)
                self.stock_num3_1.setEnabled(False)
                self.stock_num3_2.setEnabled(False)
                self.label3_4.setEnabled(True)
                self.start_date3.setEnabled(True)
                self.label3_5.setEnabled(True)
                self.end_date3.setEnabled(True)
                self.label3_6.setEnabled(True)
                self.stock.setEnabled(True)
                self.cor.setEnabled(True)
                self.show_graph_btn3.setEnabled(True)
                
                stock_name1 = change_data(df, stock_num1)
                stock_name2 = change_data(df, stock_num2)
                self.stock_name_list = [stock_name1, stock_name2]
                
                df = stock_2_data(self.data_len, stock_num1, stock_num2)
                self.corr_list, self.stock_prices = data_corr(df), df
                corr = \
f'''=========={stock_name1}~{stock_name2}==========
slope : {round(self.corr_list[0], 5)}
intercept : {round(self.corr_list[1], 5)}
r-value : {round(self.corr_list[2], 5)}
p-value : {round(self.corr_list[3], 5)}'''
                text = f'{stock_name1}과(와) {stock_name2}에 대한 분석을 완료했습니다.'
                self.log3.append(corr)
        except KeyError:
            text = f'{reason}는(은) 존재하지 않는 종목 코드 입니다. (첫번째 탭에서 확인가능)'
        finally:
            self.result3_1.setText(text)
            self.start_date3.setText(df.index[0])
            self.end_date3.setText(df.index[-1])
    
    def show_corr(self):
        text = '그래프 종류를 선택하세요.'
        df = self.stock_prices
        name1, name2 = self.stock_name_list
        if self.stock.isChecked():
            text = '주가 그래프 생성 완료'
            title = f'최근 {self.data_len}일간 주가'
            xlabel, ylabel = 'data', 'price'
            df.plot()
            plt.legend(self.stock_name_list)
        elif self.cor.isChecked():
                text = '상관관계 그래프 생성 완료'
                data1, data2 = df.T.iloc[:,:].values
                ry = polyval(self.corr_list[:2], data1)
                title = f'{name1}와 {name2} 관계'
                xlabel, ylabel = f'{name1}', f'{name2}'
                plt.plot(data1, data2, 'k.')
                plt.plot(data1, ry, 'r')
            
        self.result3_2.setText(text)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
    
    def stop_corr(self):
        text = '초기화되었습니다.'
        
        self.Start_btn3.setEnabled(True)
        self.Reset_btn3.setEnabled(False)
        self.data_len3.setEnabled(True)
        self.stock_num3_1.setEnabled(True)
        self.stock_num3_2.setEnabled(True)
        self.label3_4.setEnabled(False)
        self.start_date3.setEnabled(False)
        self.label3_5.setEnabled(False)
        self.end_date3.setEnabled(False)
        self.label3_6.setEnabled(False)
        self.stock.setEnabled(False)
        self.cor.setEnabled(False)
        self.show_graph_btn3.setEnabled(False)
        self.result3_1.setText(text)

    # # tab4
    # def pre_pred(self):
    #     data_len = self.data_len4.text()
    #     stock_num = str(self.stock_num4.text())
        
    #     df = self.stock_list
    #     text = ''
    #     try:
    #         if len(str(data_len)) == 0:
    #             text = '불러올 데이터 갯수를 입력하세요.'
    #         elif len(str(stock_num)) == 0:
    #             text = '종목 코드를 입력하세요.'
    #         elif data_len.isdigit() == False:
    #             text = '데이터 갯수는 숫자로만 입력가능합니다'
    #         elif stock_num.isdigit() == False:
    #             text = '종목코드는 숫자로만 입력가능합니다.'
    #         elif int(data_len) % 10 != 0:
    #             text = '올바른 데이터 갯수가 아닙니다. (10의 배수로만 입력가능)'
    #         elif int(data_len) % 100 != 0:
    #             text = '데이터는 100개이상의 10의 배수로만 가져올 수 있습니다.'
    #         elif stock_num not in list(df[df.columns[1]]):
    #             raise KeyError
    #         else:
    #             self.Start_btn4.setEnabled(False)
    #             self.Reset_btn4.setEnabled(True)
    #             self.data_len4.setEnabled(False)
    #             self.stock_num4.setEnabled(False)
    #             self.label4_3.setEnabled(True)
    #             self.start_date2.setEnabled(True)
    #             self.label4_4.setEnabled(True)
    #             self.end_date2.setEnabled(True)
    #             self.label4_5.setEnabled(True)
    #             self.w_s_default.setEnabled(True)
    #             self.w_s_manual.setEnabled(True)
    #             self.window_sizer.setEnabled(True)
    #             self.spliter_default.setEnabled(True)
    #             self.spliter_manual.setEnabled(True)
    #             self.spliter.setEnabled(True)
    #             self.b_s_default.setEnabled(True)
    #             self.b_s_manual.setEnabled(True)
    #             self.b_s.setEnabled(True)
    #             self.epoch_default.setEnabled(True)
    #             self.epoch_manual.setEnabled(True)
    #             self.epoch.setEnabled(True)
    #             self.start_pred_btn4.setEnabled(True)
    #             self.show_graph_btn4.setEnabled(True)
                

    #             self.result = stock_1_data(data_len, stock_num)
    #             self.stock_num_list = []
                
    #             stock_name = change_data(df, stock_num)
    #             self.result_ = add_fluctuate(self.result)
    #             text = f'{data_len}개의 {stock_name} 데이터를 불러왔습니다.'
    #             model = df_tableView(self.result_.T)
            
    #             self.start_date4.setText(self.result_.index[0])
    #             self.end_date4.setText(self.result_.index[-1])                
    #             self.tableView4.setModel(model)
    #     except KeyError:
    #         text = '존재하지 않는 종목 코드 입니다. (첫번째 탭에서 확인가능)'
    #     finally:
    #         self.result4_1.setText(text)
    
    # def start_pred(self):
    #     self.Reset_btn4.setEnabled(False)
    #     df = self.result
    #     try:
    #         if self.w_s_default.isChecked():
    #             self.w_s = 5
    #         else:
    #             if len(self.window_sizer.text()) == 0:
    #                 reason = 'set size'
    #                 raise KeyError
    #             else:
    #                 self.w_s = int(self.window_sizer.text())
                    
    #         if self.spliter_default.isChecked():
    #             s = 0.7
    #         else:
    #             if len(self.spliter.text()) == 0:
    #                 reason = 'spliter'
    #                 raise KeyError
    #             else: s = float(self.spliter.text())
                
    #         if self.b_s_default.isChecked():
    #             b_s = 1
    #         else: 
    #             if len(self.b_s.text()) == 0:
    #                 reason = 'batch size'
    #                 raise KeyError
    #             else: b_s = int(self.b_s.text())
                
    #         if self.epoch_default.isChecked():
    #             epoch = 10
    #         else: 
    #             if len(self.epoch.text()) == 0:
    #                 reason = 'epoch'
    #                 raise KeyError
    #             else: epoch = int(self.epoch.text())
            
    #         self.train_pred, self.test_pred, self.test_len = pred(df, self.w_s, s, b_s, epoch)
    #     except KeyError: 
    #         text = f'{reason}를 올바르게 설정하세요'
    #         self.result4_1.setText(text)
    #     finally: 
    #         self.result4_2.setText('데이터 학습을 완료했습니다.')
    #         self.Reset_btn4.setEnabled(True)
            
    # def show_pred(self):
    #     df = self.result
    #     train_pred, test_pred, test_len = self.train_pred, self.test_pred, self.test_len
    #     train_pred_idx = df.index[self.w_s:-(test_len-1)]
    #     test_pred_idx = df.index[-test_len:]
        
    #     raw_df = make_pd(list(df[df.columns[0]]), df.index, 'real')
    #     train_df = make_pd(train_pred, train_pred_idx, 'trained')
    #     test_df = make_pd(test_pred, test_pred_idx, 'tested')
        
    #     self.result_df = raw_df.merge(
    #         train_df, 
    #         how = 'outer', 
    #         left_index = True, 
    #         right_index = True
    #     ).merge(
    #         test_df,
    #         how = 'outer', 
    #         left_index = True, 
    #         right_index = True
    #     )
        
    #     raw_df = self.result_
    #     test_df = add_fluctuate(test_df)
        
    #     prob_dic = fluctuate_prob(raw_df, test_df, test_len)
    #     acc = (prob_dic['i_i'] + prob_dic['d_d'] + prob_dic['f_f']) / sum(prob_dic.values())
    #     self.i_i.setText(str(prob_dic['i_i']))
    #     self.i_d.setText(str(prob_dic['i_d']))
    #     self.i_f.setText(str(prob_dic['i_f']))
    #     self.d_i.setText(str(prob_dic['d_i']))
    #     self.d_d.setText(str(prob_dic['d_d']))
    #     self.d_f.setText(str(prob_dic['d_f']))
    #     self.f_i.setText(str(prob_dic['f_i']))
    #     self.f_d.setText(str(prob_dic['f_d']))
    #     self.f_f.setText(str(prob_dic['f_f']))
    #     self.acc.setText(f'{str(round(acc, 2)*100)}%')
            
    #     self.result_df.plot()
    #     plt.show()
        
    # def stop_pred(self):
    #     model = df_tableView(self.empty_df)
    #     text = '초기화되었습니다.'

    #     self.Start_btn4.setEnabled(True)
    #     self.Reset_btn4.setEnabled(False)
    #     self.data_len4.setEnabled(True)
    #     self.stock_num4.setEnabled(True)
    #     self.label4_3.setEnabled(False)
    #     self.start_date2.setEnabled(False)
    #     self.label4_4.setEnabled(False)
    #     self.end_date2.setEnabled(False)
    #     self.label4_5.setEnabled(False)
    #     self.window_sizer.setEnabled(False)
    #     self.w_s_default.setEnabled(False)
    #     self.w_s_manual.setEnabled(False)
    #     self.spliter.setEnabled(False)
    #     self.spliter_default.setEnabled(False)
    #     self.spliter_manual.setEnabled(False)
    #     self.b_s.setEnabled(False)
    #     self.b_s_default.setEnabled(False)
    #     self.b_s_manual.setEnabled(False)
    #     self.epoch.setEnabled(False)
    #     self.epoch_default.setEnabled(False)
    #     self.epoch_manual.setEnabled(False)
    #     self.start_pred_btn4.setEnabled(False)
    #     self.show_graph_btn4.setEnabled(False)
    #     # self.tableView4.setModel(model)
    #     self.result4_1.setText(text)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
