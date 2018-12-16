from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import csv
import json
import os
import os.path
import xlrd
import xlwt
import sqlite3
import pymysql
import glob
import numpy as np
import tensorflow as tf
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split #훈련/테스트 세트 구분
import pandas as pd
import matplotlib.pyplot as plt


def drawSheet(cList) :
    global cellList
    if cellList == None or cellList == [] :
        pass
    else :
        for row in cellList:
            for col in row:
                col.destroy()

    rowNum = len(cList)
    colNum = len(cList[0])
    cellList = []
    # 빈 시트 만들기
    for i in range(0, rowNum):
        tmpList = []
        for k in range(0, colNum):
            ent = Entry(window, text='')
            tmpList.append(ent)
            ent.grid(row=i, column=k)
        cellList.append(tmpList)
    # 시트에 리스트값 채우기. (= 각 엔트리에 값 넣기)
    for i in range(0, rowNum):
        for k in range(0, colNum):
            cellList[i][k].insert(0, cList[i][k])

def openCSV() :
    global  csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
                filetypes=(("CSV파일", "*.csv"), ("모든파일", "*.*")))
    filereader = open(input_file, 'r', newline='')
    csvReader = csv.reader(filereader) # CSV 전용으로 열기
    header_list = next(csvReader)

    # print(header_list)

    #{작업 중}
    csvList.append(header_list)
    for row_list in csvReader:  # 모든행은 row에 넣고 돌리기.
        csvList.append(row_list)

        print(csvList)
    return

    drawSheet(csvList)

    filereader.close()


def SVM():
    # 파일 불러오기 {작업중}
    file = openCSV()
    tbl = pd.read_csv(file)

    # 1) 1이하로 나오게 만들기(정규화와 유사, but 정규화x)
    # tbl = pd.read_csv("D:\Python\DlgsPark\data\SVM data/bmi.csv")
    print(tbl)
    return

    label = tbl["label"]
    w = tbl["weight"] / 100  # 몸무게/몸무게 최대 100
    h = tbl["weight"] / 200
    wh = pd.concat([w, h], axis=1)
    print(wh)  # 0.43   0.215 -> 2만건

    # 2) 학습용/테스트용 데이터 분리
    # train_test_split:랜덤으로 섞어 분리해줌
    data_train, data_test, label_train, label_test = train_test_split(wh,
                                                                      label)  # data_train(훈련용 데이터), data_test(테스트 데이터), label_train(훈련 레이블), label_test(테스트 레이블) 순으로 만들어짐.

    ########################SVM 핵심##############################################
    # 3) 학습용 데이터 트레이닝 시키기
    clf = svm.SVC()  # SVM 객체 생성
    clf.fit(data_train, label_train)  # 모델 생성 #입력 데이터(data_train)를 틀(label_train)에 끼워 넣겠다

    # 4) 테스트 데이터로 검증하기-예측하기
    predict = clf.predict(data_test)
    ##############################################################################
    # 정확도
    ac_score = metrics.accuracy_score(label_test, predict)  # 정확도 점수
    print("정답률=", ac_score)  # 정답률= 0.6398

    # 5)모델 평가{중요} : f1-score(<-confusion matrix) #############################
    cl_report = metrics.classification_report(label_test, predict)
    print("리포트=\n", cl_report)

    # 6) 시각화-산점도
    tbl = pd.read_csv("D:\Python\DlgsPark\data\SVM data/bmi.csv", index_col=2)  # index_col=2 : fat 가리킴
    # 산점도 그래프 작성{자주 쓰임}
    fig = plt.figure()  # plt : 그림이 들어가는 곳.
    ax = fig.add_subplot(1, 1, 1)  # subplot : 윈도우가 여러 개로 나뉨 #1,1,1 : 가로로 1칸 세로로 1칸 씩 #2,1,1 : 2행 1열로 나눈 후 2번째 행에 넣어라

    def scatter(lbl, color):
        b = tbl.loc[lbl]
        ax.scatter(b["weight"], b["height"], c=color, label=lbl)

    scatter("fat", "red")
    scatter("normal", "yellow")
    scatter("thin", "purple")
    ax.legend()  # 범례
    plt.savefig("D:\Python\DlgsPark\data\SVM data/bmi.png")

    plt.show()



## 전역 변수 ##
csvList, cellList = [], []
input_file = ''

## 메인 코드 ##
window = Tk()
window.title('Machine Learning 기반 데이터 분석틀(0.1)')
window.geometry('700x700')

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='CSV 열기', command=openCSV)
# fileMenu.add_command(label='CSV 저장', command=saveCSV)

mlMenu = Menu(mainMenu)
mainMenu.add_cascade(label='Machine-Learning', menu=mlMenu)
mlMenu.add_command(label='서포트 벡터 머신(SVM)', command=SVM) #SVM & f1-score

window.mainloop()