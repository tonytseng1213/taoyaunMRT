**專案名稱**  
MRT-side-project

**簡介**  
將從政府開放資料平台獲取的.json檔，用python自動化把資料解析成 CSV 格式，並且存入 Google Sheets。


**使用方式**  
**python**  **version**3.11

1.**安裝相依套件**：  
pip install pandas requests gspread io json google.oauth2.service_account os

2.**從政府開放資料平台獲得資料**  

*前往[政府開放資料平台](https://data.gov.tw)  ，獲取需要的資料並下載 JSON 檔案

3.**準備 Google Sheets**  

*建立一個 Google Sheets，並取得其編輯權限的憑證檔案（.json）  
  
*[可以參考](https://www.learncodewithmike.com/2020/08/python-write-to-google-sheet.html)  

4.**輸入變數**  

可以輸入main.py -h查看下列訊息:  

**-a** : Amount of data,default=10, type= int  

**-o** : default="csv" ,Output type (googlesheet or csv)

5.**必要輸入**  

*Path to the JSON file  

**googlesheet**:  

*Path to the Google service account credentials file  

*URL of the Google sheet  

*Name of the Google sheet  

**csv**: 

*file name : 要儲存的檔案名稱

6.**執行程式**  

*執行 main.py 檔案，程式將自動將政府開放資料匯入到 Google Sheets 中


**授權**  
本專案採用 MIT 授權


**如果您發現任何問題或想要增加功能，歡迎提交拉取請求或提出問題。感謝您的貢獻！**

**注意事項**  

*本專案僅供學習和測試用途，請勿用於商業用途或大規模資料處理  
*使用本專案前，請確保遵守政府開放資料平台的使用條款和相關規定  
*請小心管理您的 Google Sheets 憑證檔案，以免濫用和洩漏敏感資訊
