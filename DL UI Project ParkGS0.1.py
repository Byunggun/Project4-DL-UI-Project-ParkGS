# #1. 프로젝트 UI제작
# - 기 제작된 UI 재구성(탭/메뉴 등 ML/DL 관련 알고리즘 기반 추론 결과 출력 폼)
# - 데이터 입력/모델생성/트레이닝 횟수/Learning-rate/모델 출력/예측/분류

#시작일 : 2018.10.26.

########################################################################################################################
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

    csvList.append(header_list)
    for row_list in csvReader:  # 모든행은 row에 넣고 돌리기.
        csvList.append(row_list)

        # print(csvList)

    drawSheet(csvList)

    filereader.close()

def openJSON() :
    global  csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
                filetypes=(("JSON파일", "*.json"), ("모든파일", "*.*")))
    filereader = open(input_file, 'r', newline='', encoding='utf-8')

    jsonDic = json.load(filereader)
    csvName = list(jsonDic.keys())
    jsonList = jsonDic[csvName[0]]
    # 헤더 추출
    header_list = list(jsonList[0].keys())
    csvList.append(header_list)
    # 행들 추출
    for tmpDic in jsonList:
        tmpList = []
        for header in header_list:
            data = tmpDic[header]
            tmpList.append(data)
        csvList.append(tmpList)

    drawSheet(csvList)

    filereader.close()

def saveCSV() :
    global csvList, input_file
    if csvList == [] :
        return
    saveFp = asksaveasfile(parent=window, mode='w', defaultextension='.csv',
               filetypes=(("CSV파일", "*.csv"), ("모든파일", "*.*")))
    filewriter = open(saveFp.name, 'w', newline='')
    csvWrite = csv.writer(filewriter)
    for row_list in csvList :
        csvWrite.writerow(row_list)

    filewriter.close()


def saveJSON() :
    global csvList, input_file
    if csvList == [] :
        return
    saveFp = asksaveasfile(parent=window, mode='w', defaultextension='.json',
               filetypes=(("JSON파일", "*.json"), ("모든파일", "*.*")))
    filewriter = open(saveFp.name, 'w', newline='')
    # csvList --> jsonDic
    fname = os.path.basename(input_file).split(".")[0]
    jsonDic = {}
    jsonList = []
    tmpDic = {}
    header_list = csvList[0]
    for i in range(1, len(csvList)) :
        rowList = csvList[i]
        tmpDic = {}
        for k in range(0, len(rowList)) :
            tmpDic[header_list[k]] = rowList[k]
        jsonList.append(tmpDic)

    jsonDic[fname] = jsonList
    json.dump(jsonDic, filewriter, indent=4)
    filewriter.close()

##
def csvData01() :
    global  csvList
    csvList = []
    input_file = "D:\Python\WooJaeNam\DataText\supplier_data.csv"
    filereader = open(input_file, 'r', newline='')
    header = filereader.readline()
    header = header.strip()  # 앞뒤 공백제거
    header_list = header.split(',')
    # part Number, Purchase Date
    idx1 = 0
    for h in header_list:
        if h.strip().upper() == 'part Number'.strip().upper():
            break
        idx1 += 1
    idx2 = 0
    for h in header_list:
        if h.strip().upper() == 'Purchase Date'.strip().upper():
            break
        idx2 += 1
    if idx1 > idx2:
        idx1, idx2 = idx2, idx1
    del (header_list[idx2])
    del (header_list[idx1])
    csvList.append(header_list)
    for row in filereader:  # 모든행은 row에 넣고 돌리기.
        row = row.strip()
        row_list = row.split(',')
        del (row_list[idx2])
        del (row_list[idx1])
        if row_list[0] == 'Supplier Y':
            continue
        cost = float(row_list[2][1:])
        cost *= 1.5
        cost = int(cost / 100) * 100
        cost_str = "${0:.2f}".format(cost)
        row_list[2] = cost_str
        csvList.append(row_list)

    drawSheet(csvList)
    filereader.close()

def csvData02() :
    global csvList
    csvList = []
    input_file = "D:\Python\WooJaeNam\DataText\CSV\supplier_data.csv"
    filereader = open(input_file, 'r', newline='')
    csvReader = csv.reader(filereader) # CSV 전용으로 열기
    header_list = next(csvReader)
    csvList.append(header_list)
    for row_list in csvReader:  # 모든행은 row에 넣고 돌리기.
        csvList.append(row_list)

    drawSheet(csvList)
    filereader.close()

def csvData03() :  # 여러개 csv 파일의 행개수 합계 궁금함.
    global csvList
    csvList = []
    dirName = askdirectory()
    # 폴더에서 *.csv 파일 목록만 뽑기
    import glob
    import os
    file_list = glob.glob(os.path.join(dirName, "*.csv"))
    for  input_file  in  file_list :
        filereader = open(input_file, 'r', newline='')
        csvReader = csv.reader(filereader)  # CSV 전용으로 열기
        header_list = next(csvReader)
        rowCount = 0
        for  row in csvReader :
            rowCount += 1
        csvList.append([os.path.basename(input_file),'-->', rowCount])
        filereader.close()

    drawSheet(csvList)

def  excelData01() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetCount = workbook.nsheets  # 속성
    for worksheet in workbook.sheets():
        sheetName = worksheet.name
        sRow = worksheet.nrows
        sCol = worksheet.ncols
        print(sheetName, sRow, sCol)


def  excelData02() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetCount = workbook.nsheets  # 속성
    sheet1 = workbook.sheets()[0]
    sheetName = sheet1.name
    sRow = sheet1.nrows
    sCol = sheet1.ncols
    #print(sheetName, sRow, sCol)
    # Worksheet --> csvList
    for i  in range(sRow) :
        tmpList = []
        for k in range(sCol) :
            value = sheet1.cell_value(i,k)
            tmpList.append(value)
        csvList.append(tmpList)

    drawSheet(csvList)

def  excelData03() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetCount = workbook.nsheets  # 속성
    for worksheet in workbook.sheets():
        sRow = worksheet.nrows
        sCol = worksheet.ncols
        # Worksheet --> csvList
        for i  in range(sRow) :
            tmpList = []
            for k in range(sCol) :
                value = worksheet.cell_value(i,k)
                tmpList.append(value)
            csvList.append(tmpList)

    drawSheet(csvList)

def  excelData05() :
    global csvList, input_file
    csvList = []
    input_file = askopenfilename(parent=window,
      filetypes=(("엑셀파일", "*.xls;*.xlsx"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    sheetNameList = []
    for worksheet in workbook.sheets():
        sheetNameList.append(worksheet.name)

    ##################################
    def selectSheet() :
        selectedIndex = listbox.curselection()[0]
        subWindow.destroy()
        sheet1 = workbook.sheets()[selectedIndex]
        sRow = sheet1.nrows
        sCol = sheet1.ncols
        for i in range(sRow):
            tmpList = []
            for k in range(sCol):
                value = sheet1.cell_value(i, k)
                tmpList.append(value)
            csvList.append(tmpList)
        drawSheet(csvList)

    subWindow = Toplevel(window)  # window의 하위로 지정
    listbox = Listbox(subWindow)
    button = Button(subWindow, text='선택', command=selectSheet)
    listbox.pack(); button.pack()
    for  sName in sheetNameList :
        listbox.insert(END, sName)
    subWindow.lift()

def openExcel():
    global  csvList, input_file
    csvList = []
    #엑셀 파일 선택해 열기
    input_file = askopenfilename(parent=window,
                    filetypes=(("Excel파일", "*.xls"), ("모든파일", "*.*")))
    workbook = xlrd.open_workbook(input_file)
    # 엑셀 시트의 내용 추출하기
    sheet = workbook.sheet_by_index(0)
    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    # print(sheet_data)
    # 제목만 csvlist에 넣기
    header_list=list(sheet_data[0])
    csvList.append(header_list)
    # 제목+내용 모두 csvlst에 넣기
    for row_list in sheet_data:  # 모든행은 row에 넣고 돌리기.
        csvList.append(row_list)

    drawSheet(csvList)

def saveExcel() :
    global csvList, input_file
    if csvList == [] :
        return
    saveFp = asksaveasfile(parent=window, mode='w', defaultextension='.xls',
               filetypes=(("Excel파일", "*.xls"), ("모든파일", "*.*")))
    fileName = saveFp.name

    # csvList --> xls
    outWorkbook = xlwt.Workbook()
    outSheet = outWorkbook.add_sheet('sheet1') # 이름을 추후에 지정하세요.

    for i in range(len(csvList)) :
        for k in range(len(csvList[i])) :
            outSheet.write(i,k, csvList[i][k])

    outWorkbook.save(fileName)

#########{작업 중. 다 안읽어 지는데}
# def openText():
#     global  csvList, input_file
#     csvList = []
#     input_file = askopenfilename(parent=window,
#                     filetypes=(("Txt파일", "*.txt"), ("모든파일", "*.*")))
#     filereader = open(input_file, 'r', newline='')
#     csvReader = csv.reader(filereader) # CSV 전용으로 열기
#     header_list = next(csvReader)
#
#     # print(header_list)
#
#     csvList.append(header_list)
#     for row_list in csvReader:  # 모든행은 row에 넣고 돌리기.
#         csvList.append(row_list)
#
#         # print(csvList)
#
#     drawSheet(csvList)
#
#     filereader.close()

################################################################################################################################
#
# def saveText():
#     global csvList, input_file
#     if csvList == [] :
#         return
#     saveFp = asksaveasfile(parent=window, mode='w', defaultextension='.txt',
#                filetypes=(("Txt파일", "*.txt"), ("모든파일", "*.*")))
#     filewriter = open(saveFp.name, 'w', newline='')


#####

def sqliteData01() :

    con = sqlite3.connect('c:/temp/userDB')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)

    csvList = []

    # 데이터베이스 내의 테이블 목록이 궁금?
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    cur.execute(sql)
    tableNameList = []
    while True :
        row = cur.fetchone()
        if row == None:
            break
        tableNameList.append(row[0]);

    ##################################
    def selectTable() :
        selectedIndex = listbox.curselection()[0]
        subWindow.destroy()
        # 테이블의 열 목록 뽑기
        # print(colNameList)
        #colNameList = ["userID", "userName", "userAge"]
        #csvList.append(colNameList)
        sql = "SELECT * FROM " + tableNameList[selectedIndex]
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            row_list = []
            for ii in range(len(row)) :
                row_list.append(row[ii])

            csvList.append(row_list)

            drawSheet(csvList)

    subWindow = Toplevel(window)  # window의 하위로 지정
    listbox = Listbox(subWindow)
    button = Button(subWindow, text='선택', command=selectTable)
    listbox.pack(); button.pack()
    for  sName in tableNameList :
        listbox.insert(END, sName)
    subWindow.lift()

    ####################################


def sqliteData02() :
    global csvList, input_file
    con = sqlite3.connect('c:/temp/userDB')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)
    # 열이름 리스트 만들기
    colList = []
    for data in csvList[0] :
        colList.append(data.replace(' ', ''))
    tableName = os.path.basename(input_file).split(".")[0]
    try:
        sql = "CREATE TABLE " + tableName + "("
        for colName in colList :
            sql += colName + " CHAR(20),"
        sql = sql[:-1]
        sql += ")"
        cur.execute(sql)
    except:
        pass

    for i in range(1, len(csvList)) :
        rowList = csvList[i]
        sql = "INSERT INTO " +  tableName + " VALUES("
        for row in rowList:
            sql += "'" + row + "',"
        sql = sql[:-1]
        sql += ")"
        cur.execute(sql)

    con.commit()

    cur.close()
    con.close()  # 데이터베이스 연결 종료
    print('Ok!')


def mysqlData01() :
    con = pymysql.connect(host='192.168.59.129', user='root',
                          password='1234', db='userDB', charset='utf8')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)
    csvList = []
    # 데이터베이스 내의 테이블 목록이 궁금?
    sql = "SHOW TABLES"
    cur.execute(sql)
    tableNameList = []
    while True :
        row = cur.fetchone()
        if row == None:
            break
        tableNameList.append(row[0]);

    ##################################
    def selectTable() :
        selectedIndex = listbox.curselection()[0]
        subWindow.destroy()
        # 테이블의 열 목록 뽑기
        colNameList = []
        sql = "DESC " + tableNameList[selectedIndex]
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            colNameList.append(row[0]);

        csvList.append(colNameList)
        sql = "SELECT * FROM " + tableNameList[selectedIndex]
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            row_list = []
            for ii in range(len(row)) :
                row_list.append(row[ii])

            csvList.append(row_list)

            drawSheet(csvList)

    subWindow = Toplevel(window)  # window의 하위로 지정
    listbox = Listbox(subWindow)
    button = Button(subWindow, text='선택', command=selectTable)
    listbox.pack(); button.pack()
    for  sName in tableNameList :
        listbox.insert(END, sName)
    subWindow.lift()

    ####################################


def mysqlData02() :
    global csvList, input_file
    con = pymysql.connect(host='192.168.59.129', user='root',
                          password='1234', db='userDB', charset='utf8')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()  # 연결 통로 생성 (쿼리문을 날릴 통로)
    # 열이름 리스트 만들기
    colList = []
    for data in csvList[0] :
        colList.append(data.replace(' ', ''))
    tableName = os.path.basename(input_file).split(".")[0]
    try:
        sql = "CREATE TABLE " + tableName + "("
        for colName in colList :
            sql += colName + " CHAR(20),"
        sql = sql[:-1]
        sql += ")"
        cur.execute(sql)
    except:
        pass

    for i in range(1, len(csvList)) :
        rowList = csvList[i]
        sql = "INSERT INTO " +  tableName + " VALUES("
        for row in rowList:
            sql += "'" + row + "',"
        sql = sql[:-1]
        sql += ")"
        cur.execute(sql)

    con.commit()

    cur.close()
    con.close()  # 데이터베이스 연결 종료
    print('Ok!')

def autoData01() :

    con = sqlite3.connect('c:/temp/userDB')
    cur = con.cursor()

    # 폴더 선택하고, 그 안의 파일목록들 추출하기.
    dirName = askdirectory()
    file_list = glob.glob(os.path.join(dirName, "*.csv"))

    # 각 파일을 SQLite에 저장하기. (파일당 테이블 1개)
    for input_file in file_list:
        filereader = open(input_file, 'r', newline='')
        csvReader = csv.reader(filereader)
        colList = next(csvReader)  # 열이름들
        tableName = os.path.basename(input_file).split(".")[0]
        try:
            sql = "CREATE TABLE " + tableName + "("
            for colName in colList:
                cList = colName.split()
                colName = ''
                for col in cList:
                    colName += col + '_'
                colName = colName[:-1]
                sql += colName + " CHAR(20),"
            sql = sql[:-1]
            sql += ')'
            print(sql)
            cur.execute(sql)

        except:
            print('테이블 이상 -->', input_file)
            continue

        for rowList in csvReader:
            sql = "INSERT INTO " + tableName + " VALUES("
            for data in rowList:
                sql += "'" + data + "',"
            sql = sql[:-1] + ')'
            try :
                cur.execute(sql)
            except :
                pass

        filereader.close()
        con.commit()

    cur.close()
    con.close()
    print("OK!")

def autoData02() :
    con = pymysql.connect(host='192.168.59.129', user='root',
                          password='1234', db='userDB', charset='utf8')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()

    # 폴더 선택하고, 그 안의 파일목록들 추출하기.
    dirName = askdirectory()
    file_list = glob.glob(os.path.join(dirName, "*.csv"))

    # 각 파일을 SQLite에 저장하기. (파일당 테이블 1개)
    for input_file in file_list:
        filereader = open(input_file, 'r', newline='')
        csvReader = csv.reader(filereader)
        colList = next(csvReader)  # 열이름들
        tableName = os.path.basename(input_file).split(".")[0]
        try:
            sql = "CREATE TABLE " + tableName + "("
            for colName in colList:
                cList = colName.split()
                colName = ''
                for col in cList:
                    colName += col + '_'
                colName = colName[:-1]
                sql += colName + " CHAR(20),"
            sql = sql[:-1]
            sql += ')'
            print(sql)
            cur.execute(sql)

        except:
            print('테이블 이상 -->', input_file)


        for rowList in csvReader:
            sql = "INSERT INTO " + tableName + " VALUES("
            for data in rowList:
                sql += "'" + data + "',"
            sql = sql[:-1] + ')'
            try :
                cur.execute(sql)
            except :
                pass

        filereader.close()
        con.commit()

    cur.close()
    con.close()
    print("OK!")

def autoData03() :

    con = sqlite3.connect('c:/temp/userDB')
    cur = con.cursor()

    # 저장할 폴더 선택하기.
    dirName = askdirectory()

    # 각 테이블을 CSV로 저장하기. (테이블당 파일 1개)
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    cur.execute(sql)
    tableNameList = []
    while True:
        row = cur.fetchone()
        if row == None:
            break
        tableNameList.append(row[0]);

    # 각 파일을 SQLite에 저장하기. (파일당 테이블 1개)
    for tableName in tableNameList:
        output_file =  dirName + '/' + tableName + '.csv'
        filewriter = open(output_file, 'w', newline='')
        csvWrite = csv.writer(filewriter)

        # 열이름 추출
        # 테이블의 열 목록 뽑기
        sql = "SELECT * FROM " + tableName
        cursor = con.execute(sql)
        colNameList = list(map(lambda x: x[0], cursor.description))
        csvWrite.writerow(colNameList)

        # CSV에 행 데이터 쓰기
        sql = "SELECT * FROM " + tableName
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            row_list = []
            for ii in range(len(row)):
                row_list.append(row[ii])

            csvWrite.writerow(row_list)

        filewriter.close()
        print(output_file + ' 생성.')

    cur.close()
    con.close()
    print("OK!")

def autoData04()  :
    con = pymysql.connect(host='192.168.59.129', user='root',
                          password='1234', db='userDB', charset='utf8')  # 데이터베이스 지정(또는 연결)
    cur = con.cursor()

    # 저장할 폴더 선택하기.
    dirName = askdirectory()

    # 각 테이블을 CSV로 저장하기. (테이블당 파일 1개)
    sql = "SHOW TABLES"
    cur.execute(sql)
    tableNameList = []
    while True:
        row = cur.fetchone()
        if row == None:
            break
        tableNameList.append(row[0]);

    # 각 파일을 SQLite에 저장하기. (파일당 테이블 1개)
    for tableName in tableNameList:
        output_file =  dirName + '/' + tableName + '.csv'
        filewriter = open(output_file, 'w', newline='')
        csvWrite = csv.writer(filewriter)

        # 열이름 추출
        # 테이블의 열 목록 뽑기
        # 테이블의 열 목록 뽑기
        colNameList = []
        sql = "DESC " + tableName
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            colNameList.append(row[0]);
        csvWrite.writerow(colNameList)

        # CSV에 행 데이터 쓰기
        sql = "SELECT * FROM " + tableName
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            row_list = []
            for ii in range(len(row)):
                row_list.append(row[ii])

            csvWrite.writerow(row_list)

        filewriter.close()
        print(output_file + ' 생성.')

    cur.close()
    con.close()
    print("OK!")


#{작업중}
def linearRegression(): #선형회귀
    ### 데이터 불러오기{작업중}
    # 1) speed, distance 추출
    cars = np.loadtxt('D:\Python\DlgsPark\data\Regression data/cars.csv', delimiter=",")
    # print(cars)
    # print(cars.shape)

    xx, yy = [], []
    for row in cars:
        xx.append(row[0])  # spped
        yy.append(row[1])  # distance
    # print(xx)
    # print(yy)

    #매개변수
    #learning_rate버튼
    # learning_rate=askfloat('Learning Rate','Learning Rate를 0.1~.0.01 사이에서 선택하세요', minvalue=0.01, maxvalue=0.1) #askfloat #{작업 중}자연상수?
    learning_rate = askfloat('Learning Rate', 'Learning Rate를 입력하시오(1e-8~0.1) ', minvalue=1e-8,maxvalue=0.1) #박제 님 코드
    label1 = Label(window, text=" Learning Rate : ")
    label1.grid(row=1, column=1)
    label1val = Label(window, text=learning_rate, relief='ridge')
    label1val.grid(row=1, column=2)
    #trainning_epochs버튼
    trainning_epochs=askinteger('훈련 횟수','훈련 횟수(2001~20001)를 적어주세요',  minvalue=1, maxvalue=20001)
    label2 = Label(window, text=" trainning_epochs: ")
    label2.grid(row=2, column=1)
    label2val = Label(window, text=trainning_epochs, relief='ridge')
    label2val.grid(row=2, column=2)

    ### Linear regression(선형회귀) 모델만들기 : feed_dict 사용
    w = tf.Variable(tf.random_normal([1]))  # w=정규분포 난수 1개인 변수
    b = tf.Variable(tf.random_normal([1]))  # b=정규분포 난수 1개인 변수

    x = tf.placeholder(tf.float32, shape=[None])
    y = tf.placeholder(tf.float32, shape=[None])
    hf = w * x + b  # 가설함수(예측함수)

    cost = tf.reduce_mean(tf.square(hf - y))

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    train = optimizer.minimize(cost)
    ######## 여기까지 <그래프 정의>
    ######## 여기서부터 <그래프 실행>
    ### 출력하기
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for step in range(trainning_epochs):
            cv, _ = sess.run([cost, train], feed_dict={x: xx, y: yy})
            if step % 200 == 0:
                print(step, cv)
        print("=====모델 완성=====")

        hfv, cv, wv, bv = sess.run([hf, cost, w, b], feed_dict={x: xx, y: yy})
        print("\n예측값: \n", hfv, "비용(cost): ", cv,"가중치(w): ", wv, "편향(b): ", bv)

    #{작업중}
    ### 비용
    label4 = Label(window, text="비용(cost)")
    label4.grid(row=4, column=1)

    ### 가중치& 편향

    ### 예측해보기
    valueofPredic = askinteger('예측해보기', '예상하고 싶은 값은 무엇인가요?')
    label3 = Label(window, text=" 예측값: ")
    label3.grid(row=3, column=1)
    label3val = Label(window, text=valueofPredic, relief='ridge')
    label3val.grid(row=3, column=2)
    print(sess.run(hf, feed_dict={x:valueofPredic}))
###{작업 중}

    # # 3. 비교 : ex)True Prediction:1 True Y:1
    # pred = sess.run(prediction, feed_dict={x: xdata, y: ydata})
    # # Flatten(평평하게 해줌) : 1차원으로 변경 ex)[[[100]],[[001]]] => [100,001,...]]
    # # flatten 함수는 np에 있음. 그래서 ydata의 구조를 리스트->array로 변경
    # ydata = np.array(ydata, dtype=np.int32)
    # for p, y in zip(pred, ydata.flatten()):
    #     print("{}, prediction:{}, True Y: {}".format(p == y, p, y))

###

    #{작업 중} 입력한 w,b,interate,train횟수,cost 출력하기
    #{작업 중} 그래프

    sess.close()
    print("linearRegression OK!")

#{작업 중}
def BinaryClassification():
    return

def multinomailClassification():
    return

def SVM():
    #파일 불러오기 {작업중}
    a=openCSV()
    tbl = pd.read_csv(a)

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
fileMenu.add_command(label='CSV 저장', command=saveCSV)
fileMenu.add_separator()
fileMenu.add_command(label='JSON 열기', command=openJSON)
fileMenu.add_command(label='JSON 저장', command=saveJSON)
fileMenu.add_separator()
fileMenu.add_command(label='Excel 열기', command=openExcel)
fileMenu.add_command(label='Excel 저장', command=saveExcel)
fileMenu.add_separator()
# fileMenu.add_command(label='Text 열기', command=openText)#작업 중
# fileMenu.add_command(label='Text 저장', command=saveText) #작업 중


csvMenu = Menu(mainMenu)
mainMenu.add_cascade(label='CSV 데이터 분석', menu=csvMenu)
csvMenu.add_command(label='특정 열,행 제거', command=csvData01)
csvMenu.add_command(label='csv 패키지 활용', command=csvData02)
csvMenu.add_command(label='여러 CSV 행수 알기', command=csvData03)

excelMenu = Menu(mainMenu)
mainMenu.add_cascade(label='Excel 데이터 분석', menu=excelMenu)
excelMenu.add_command(label='Excel정보 보기', command=excelData01)
excelMenu.add_command(label='Excel내용 보기 - 1st', command=excelData02)
excelMenu.add_command(label='Excel내용 보기 - All', command=excelData03)
excelMenu.add_command(label='Excel내용 보기 - Select', command=excelData05)

sqliteMenu = Menu(mainMenu)
mainMenu.add_cascade(label='SQLite 데이터 분석', menu=sqliteMenu)
sqliteMenu.add_command(label='SQLite 정보 읽기', command=sqliteData01)
sqliteMenu.add_command(label='SQLite 정보 쓰기', command=sqliteData02)

mysqlMenu = Menu(mainMenu)
mainMenu.add_cascade(label='MySQL 데이터 분석', menu=mysqlMenu)
mysqlMenu.add_command(label='MySQL 정보 읽기', command=mysqlData01)
mysqlMenu.add_command(label='MySQL 정보 쓰기', command=mysqlData02)

autoMenu = Menu(mainMenu)
mainMenu.add_cascade(label='대량 데이터 처리 자동화', menu=autoMenu)
autoMenu.add_command(label='대량 CSV --> SQLite', command=autoData01)
autoMenu.add_command(label='대량 CSV --> MySQL', command=autoData02)
autoMenu.add_separator()
autoMenu.add_command(label='SQLite --> 대량 CSV', command=autoData03)
autoMenu.add_command(label='MySQL --> 대량 CSV', command=autoData04)

mlMenu = Menu(mainMenu)
mainMenu.add_cascade(label='Machine-Learning', menu=mlMenu)
mlMenu.add_command(label='선형회귀(Linear Regression)', command=linearRegression)
mlMenu.add_command(label='로지스틱 분류(Logistic(Binary) classification)', command=BinaryClassification)
mlMenu.add_command(label='다범주 분류(Multinomial Classification)', command=multinomailClassification)
mlMenu.add_command(label='서포트 벡터 머신(SVM)', command=SVM) #SVM & f1-score

#+정규화


window.mainloop()

##