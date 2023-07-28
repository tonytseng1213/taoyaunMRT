import pandas as pd
import requests
import io
from google.oauth2.service_account import Credentials
import gspread
import json
import argparse
import os
import mysql.connector
import yaml

def get_user_input():
    #arg設定
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", help="Amount of data",default=None, type= int)
    parser.add_argument("-o", choices=["googlesheet", "csv", "mysql"], default="csv", help="Output type (googlesheet, csv, or mysql)")
    parser.add_argument("-c" , help="Path to the config.yaml file")
    
    args = parser.parse_args()

    amount = args.a
    storage = args.o 
    config_file = args.c
    #處理amount輸入變數
    if amount is None or not isinstance(amount, int):
        amount = float('inf') 
    #處理storage輸入變數
    if storage not in ["googlesheet", "csv", "mysql"]:
        storage = "csv"
    return amount, storage, config_file

def file_to_dataframe(file_path, amount):    

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    # 取得資料網址
    count = 0  
    url_list = []
    print(data[0])
    json_data_name = input("\n輸入想要抓取的欄位名稱,default為'資料下載網址'\n欄位名稱:")
    if json_data_name == "":
        json_data_name ="資料下載網址"
    for item in data:
        url = item[json_data_name]
        url_list.append(url) # 將獲取到的資料網址加入list
        count += 1  
        
        if count == amount:
            break  

    datalist = []
    for url in url_list:
        response = requests.get(url)
        data = response.content
    # 解析CSV檔案
        try:
            df = pd.read_csv(io.BytesIO(data), encoding= "utf-8")
        except :
            df = pd.read_csv(io.BytesIO(data), encoding="big5")

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

def file_to_googlesheet(datalist,config_file):
    if config_file:
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        
        credentials_file = config.get("credentials_file", "")
        sheet_url = config.get("sheet_url", "")
        sheet_name = config.get("sheet_name", "")
    else:    
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
    for row in datalist:
        data_rows = [row.columns.values.tolist()] + row.values.tolist()# 
        worksheet.append_rows(data_rows)
    print("資料已存入google sheet")

def data_to_mysql(datalist, config):
    try:
        # 建立與 MySQL 資料庫的連線
        db = mysql.connector.connect(
            user=config['mysql_user'],
            password=config['mysql_password'],
            host=config['mysql_host'],
            database=config['mysql_database']
        )

        # 建立資料表（如果需要）
        cursor = db.cursor()

        column_list = []
        for column_name, column_type in config["column_types"].items():
            column_list.append("`{}` {}".format(config["column_names"][column_name], column_type))

        create_table_query = """
            CREATE TABLE IF NOT EXISTS {} (
                {}
            )
        """.format(config["table_name"], ",\n".join(column_list))

        cursor.execute(create_table_query)
        # 將每個 DataFrame 的資料插入資料表
        for df in datalist:
            for row in df.itertuples(index=False):
                insert_query = "INSERT INTO {} ({}) VALUES ({})".format(
                    config["table_name"],
                    ", ".join(["`{}`".format(column) for column in config["column_names"].values()]),  # 指定欄位名稱
                    ", ".join(["%s"] * len(config["column_names"]))  # 使用多個 %s 來表示值的替代位置
                )
                values = tuple(row)
                cursor.execute(insert_query, values)

        # 提交變更並關閉連線
        db.commit()
        cursor.close()
        db.close()
        print("資料成功寫入mySQL")
    except mysql.connector.Error as e:
        print("MySQL 錯誤：", e)
        print("請確認mySQL資料表的欄位與資料型態是否合理")
   

def main():
    amount, storage, config_file = get_user_input()

    if config_file:
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            
        amount = config.get("amount", "")
            
        try:
            file_paths = config['file_paths']
        except KeyError:
            file_paths = input("Enter file paths (separated by commas): ").split(",")
        
        
        for file_path in file_paths:
            mydata = file_to_dataframe(file_path.strip(), amount)
            
            if storage == "googlesheet":
                file_to_googlesheet(mydata, config_file)
            
            elif storage == "csv":
                
                new_filename = check_and_save_csvfilename() 
                to_csv(mydata, new_filename)
            else:
                data_to_mysql(mydata, config)   
        
    else:
        if storage == "googlesheet" or storage == "csv":
            file_paths = input("Enter file paths (separated by commas): ").split(",")

            new_filename = check_and_save_csvfilename() if storage == "csv" else None

            for file_path in file_paths:
                mydata = file_to_dataframe(file_path.strip(), amount)

                if storage == "googlesheet":
                    file_to_googlesheet(mydata, config_file)
                elif storage == "csv":
                    to_csv(mydata, new_filename)
        else:
            # 若 storage 為 "mysql"，強制使用者輸入 config_file
            while not config_file:
                config_file = input("Enter yaml file: ")

            with open(config_file, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            file_paths = config['file_paths']

            for file_path in file_paths:
                mydata = file_to_dataframe(file_path.strip(), amount)

            data_to_mysql(mydata, config)

if __name__ == "__main__":
    main()
