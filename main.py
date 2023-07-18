import pandas as pd
import requests
import io
from google.oauth2.service_account import Credentials
import gspread
import json
import argparse
import os

def get_user_input():
    #arg設定
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", help="Amount of data",default=10, type= int)
    # parser.add_argument("-e", choices=["big5", "csv"], default="csv", help="Encoding type (big5 or csv)")
    parser.add_argument("-o", choices=["googlesheet", "csv"], default="csv", help="Output type (googlesheet or csv)")

    args = parser.parse_args()

    amount = args.a
    # encoding = args.e
    storage = args.o 
   
    return amount, storage

amount, storage = get_user_input()

def file_to_dataframe(file_path, amount):    
    # 開啟檔案並讀取內
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    # 取得資料網址
    print(data[0])
    count = 0  
    url_list = []
    json_data_name = input("\n輸入想要抓取的欄位名稱,default為'資料下載網址'\n欄位名稱:")
    if json_data_name == "":
        json_data_name ="資料下載網址"
    for item in data:
        url = item[json_data_name]
        url_list.append(url) # 將獲取到的資料網址加入list
        count += 1  
        
        if count == amount:
            break  

    #將存在url list裡的連結讀取成資料，並存入data frames
    datalist = []
    for url in url_list:
        response = requests.get(url)
        data = response.content
    # 解析CSV檔案
        try:
            df = pd.read_csv(io.BytesIO(data), encoding= "utf-8")
        except :
            # df = pd.read_csv(io.StringIO(data), encoding= "big5")
            df = pd.read_csv(io.BytesIO(data), encoding="big5")
            # df = pd.read_csv(io.BytesIO(data.decode("big5")))


        datalist.append(df)
        print("解析成功")

    return datalist

def check_and_save_csvfilename():
    filename = input("enter filename: ")
    if os.path.isfile(filename+".csv"):
        # 文件存在，找到一个可用的新文件名
        i = 1
        while True:
            base_filename = filename.replace(".csv", "")
            new_filename = f"{base_filename}{i}.csv"
            if i == 1:
                print(f"檔案 {filename} 已存在")
            else:
                print(f"檔案 {filename}{i-1} 已存在")
           
            if not os.path.isfile(new_filename):
                print(f"將使用新檔名 {new_filename} 存檔")
                break
            i += 1
        return new_filename
    else:
        # 文件不存在，直接使用原文件名
        print(f"將使用檔名 {filename} 存檔")
        return filename + ".csv"


def to_csv(mydata, new_filename):
    for df in mydata:
       df.to_csv(new_filename, index=False, mode='a', header=not os.path.isfile(new_filename), encoding="utf-8-sig")
    print(f"{new_filename} 儲存成功")

def file_to_googlesheet(data_frames):
    credentials_file = input("enter Google service account credentials file: ")
    sheet_url = input("enter Google sheet URL: ")
    sheet_name = input("enter Google sheet name: ")
    #與google sheet建立連線
    scope = ["https://www.googleapis.com/auth/spreadsheets"]

    #替換json憑證
    creds = Credentials.from_service_account_file(credentials_file,scopes=scope)
    gs = gspread.authorize(creds)
    sheet = gs.open_by_url(sheet_url)

    #選擇資料表
    worksheet = sheet.worksheet(sheet_name)

    # 將資料以逗號分隔的方式匯入工作表
    for row in data_frames:
        data_rows = [row.columns.values.tolist()] + row.values.tolist()
        worksheet.append_rows(data_rows)
    print("資料已存入google sheet")



def main():
    amount, storage = get_user_input()

    file_paths = input("Enter file paths (separated by commas): ").split(",")

    for file_path in file_paths:
        # 移除首尾的空格

        mydata= file_to_dataframe(file_path.strip(), amount)

        if storage == "googlesheet":
            print(mydata[0].head(5))
            file_to_googlesheet(mydata)
        elif storage == "csv":
            # print(mydata[0])
            new_filename = check_and_save_csvfilename()
            # mydata = pd.concat(mydata, ignore_index=True)
            # print(mydata)
            to_csv(mydata, new_filename)

if __name__ == "__main__":
    main()
