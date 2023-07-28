# import unittest
# from unittest.mock import patch
# import main  

# class TestMinitest(unittest.TestCase):
    
#     @patch('builtins.input', side_effect=["1", "csv", "file1.json", "資料下載網址"])
#     @patch('requests.get')
#     @patch('builtins.open', unittest.mock.mock_open(read_data='[{"資料下載網址": "http://example.com/data.csv"}]'))
#     @patch('pandas.DataFrame.to_csv')
#     def test_file_to_dataframe_csv(self, mock_to_csv, mock_open, mock_get, mock_input):
#         mock_response = unittest.mock.Mock()
#         mock_response.content = b'data content'
#         mock_get.return_value = mock_response

#         main.main()

#         mock_open.assert_called_once_with('file1.json', 'r', encoding='utf-8')
#         mock_get.assert_called_once_with('http://example.com/data.csv')
#         mock_to_csv.assert_called_once()

#     if __name__ == '__main__':
#         unittest.main()

# import unittest
# import argparse
# from unittest.mock import patch
# import main

# class TestGetUserInput(unittest.TestCase):
#     @patch('builtins.input', side_effect=["10", "222"])
#     def test_get_user_input_with_invalid_input(self, mock_input):
#         expected_amount = float("inf")
#         expected_storage = "csv"
#         args = argparse.Namespace(a="10個", o="google sheet")

#         with patch('main.argparse.ArgumentParser.parse_args', return_value=args):
#             amount, storage = main.get_user_input()
#         print(f"Actual amount: {amount}")
#         print(f"Expected amount: {expected_amount}")

#         print(f"Actual storage: {storage}")
#         print(f"Expected storage: {expected_storage}")

#         self.assertEqual(amount, expected_amount)
#         self.assertEqual(storage, expected_storage)
        
#     @patch('builtins.input', side_effect=["5", "googlesheet"])
#     def test_get_user_input_with_valid_input(self, mock_input):
#         expected_amount = 5
#         expected_storage = "googlesheet"

#         # 使用argparse.Namespace來建立args物件
#         args = argparse.Namespace(a=5, o="googlesheet")

#         with patch('main.argparse.ArgumentParser.parse_args', return_value=args):
#             amount, storage = main.get_user_input()

#         self.assertEqual(amount, expected_amount)
#         self.assertEqual(storage, expected_storage)

# if __name__ == '__main__':
#     unittest.main()



# import unittest
# from unittest.mock import patch, MagicMock
# import main

# class TestFileToDataFrame(unittest.TestCase):
#     pd = "pandas"
#     data_content = b'data content'
#     expected_url = "https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=30836a4a-215a-43f9-a6c7-f890590f2c6b&rid=45647819-6d74-4571-a8b8-ee6f62eca0f6"

#     @patch('requests.get')
#     @patch('main.pd.read_csv')
#     @patch('io.BytesIO')
#     def test_file_to_dataframe_default_amount(self, mock_bytesio, mock_read_csv, mock_get):
#         with patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"資料下載網址": "' + self.expected_url + '"}]') as mock_open:
#             # 模拟 HTTP 请求的返回值
#             mock_response = MagicMock()
#             mock_response.content = self.data_content
#             mock_get.return_value = mock_response

#             # 调用被测试函数
#             datalist = main.file_to_dataframe("D:\Downloads\export1688045669.json", None)

#             # 验证 mock 函数是否按预期调用
#             mock_open.assert_called_once_with("D:\Downloads\export1688045669.json", 'r', encoding='utf-8')
#             mock_get.assert_called_once_with(self.expected_url)
#             mock_bytesio.assert_called_once_with(self.data_content)
#             mock_read_csv.assert_called_once_with(mock_bytesio.return_value, encoding="utf-8")

#             # 验证函数返回的结果是否符合预期
#             self.assertEqual(len(datalist), 1)
#             self.assertTrue(isinstance(datalist[0], MagicMock))
#             print("测试 file_to_dataframe 默认情况成功")

#     @patch('requests.get')
#     @patch('main.pd.read_csv')
#     @patch('io.BytesIO')
#     def test_file_to_dataframe_specific_amount(self, mock_bytesio, mock_read_csv, mock_get):
#         with patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='[{"資料下載網址": "' + self.expected_url + '"}]') as mock_open:
#             # 模拟 HTTP 请求的返回值
#             mock_response = MagicMock()
#             mock_response.content = self.data_content
#             mock_get.return_value = mock_response

#             # 调用被测试函数
#             datalist = main.file_to_dataframe("D:\Downloads\export1688045669.json", 2)  # 设置特定的 amount 值

#             # 验证 mock 函数是否按预期调用
#             mock_open.assert_called_once_with("D:\Downloads\export1688045669.json", 'r', encoding='utf-8')
#             mock_get.assert_called_once_with(self.expected_url)
#             mock_bytesio.assert_called_once_with(self.data_content)
#             mock_read_csv.assert_called_once_with(mock_bytesio.return_value, encoding="utf-8")

#             # 验证函数返回的结果是否符合预期
#             self.assertEqual(len(datalist), 1)
#             self.assertTrue(isinstance(datalist[0], MagicMock))
#             print("测试 file_to_dataframe 特定 amount 成功")
# if __name__ == '__main__':
#     unittest.main()

# import unittest
# from unittest.mock import patch
# import main

# class TestCheckAndSaveCsvFilename(unittest.TestCase):

#     @patch('builtins.input', side_effect=["aa","aaa","aaa","ABC"])
#     def test_check_and_save_csvfilename_file_exists(self, mock_input):
#         results = ["aaa.csv", "aaa1.csv", "aaa2.csv", "aaa3.csv", "aaa4.csv", "aaa6.csv", "aaa7.csv", "aaa8.csv", "aaa9.csv", "aaa10.csv"]
#         def mock_isfile(filename):
#             if filename in results:
#                 return True
#             return False
#         rangeint = 4
#         # 调用被测试函数
#         with patch('os.path.isfile', side_effect=mock_isfile):
#             for _ in range(rangeint):
#                 result = main.check_and_save_csvfilename()
#                 results.append(result)
#         # 验证 mock 函数是否按预期调用
#         mock_input.assert_called()
#         self.assertEqual(mock_input.call_count, rangeint)

#         # 验证函数返回的结果是否符合预期
#         expected_results = ["aa.csv", "aaa5.csv", "aaa11.csv", "ABC.csv"]
#         self.assertEqual(results[-rangeint:], expected_results)
# if __name__ == '__main__':
#     unittest.main()


# import unittest
# import os
# import pandas as pd
# from main import to_csv

# class TestToCsv(unittest.TestCase):

#     def setUp(self):
#         # Create a temporary directory to store test files
#         self.test_dir = "test_files"
#         os.makedirs(self.test_dir, exist_ok=True)

#     def tearDown(self):
#         # Remove the temporary directory and its contents after the test
#         for file in os.listdir(self.test_dir):
#             os.remove(os.path.join(self.test_dir, file))
#         os.rmdir(self.test_dir)

#         # Reset the test_dir directory
#         os.makedirs(self.test_dir, exist_ok=True)

#     def test_to_csv(self):
#         # Generate test data (two dataframes)
#         df1 = pd.DataFrame({'A': [1, 2, 3], 'B': ['A', 'B', 'C']})
#         df2 = pd.DataFrame({'X': [10, 20, 30], 'Y': ['X', 'Y', 'Z']})
#         mydata = [df1, df2]

#         # Call the to_csv function with the test data
#         new_filename = os.path.join(self.test_dir, "test_output.csv")
#         to_csv(mydata, new_filename)

#         # Verify that the output file was created and contains the expected data
#         self.assertTrue(os.path.isfile(new_filename))
#         with open(new_filename, 'r', encoding="utf-8-sig") as file:
#             content = file.read()
#             self.assertIn("1,A", content)
#             self.assertIn("10,X", content)

# if __name__ == '__main__':
    # unittest.main()


import unittest
from unittest.mock import patch
import pandas as pd
import yaml
from data_to_MYSQL import data_to_mysql

class TestDataToMysql(unittest.TestCase):

    def setUp(self):
        # Load config from YAML file
        with open("config.yaml", "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        # Sample test data
        self.datalist = [
            pd.DataFrame({
                "營運日": ["2023-07-25", "2023-07-26"],
                "星期": ["Monday", "Tuesday"],
                "總運量": [100, 200]
            })
        ]

    def test_data_to_mysql(self):
        print("Input Data:")
        for df in self.datalist:
            print(df)

        print("\nConfig:")
        print(self.config)

        # 使用patch來模擬資料庫連線函數，使用測試資料庫而不是真實的資料庫連線
        with patch('mysql.connector.connect'):
            # Ensure that the function executes without any errors
            data_to_mysql(self.datalist, self.config)

            # You can add more assertions here to check if the data was inserted correctly into the database
            # For example, you can query the database and check if the data matches what you expect.

if __name__ == "__main__":
    unittest.main()


