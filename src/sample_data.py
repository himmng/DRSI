# import pandas as pd

# # Sample employee table
# data = {
#     "employee_id": [101, 102, 103, 104, 104],  # Note: duplicate 104
#     "first_name": ["Alice", "Bob", "Charlie", "David", "David"],
#     "last_name": ["Smith", "Jones", "Brown", "Taylor", "Taylor"],
#     "email": ["alice@company.com", "bob@company.com", None, "david@company.com", "david@company.com"],
#     "department_id": [10, 20, 10, 30, 30],
#     "salary": [70000, 80000, 75000, 90000, 90000]
# }

# df = pd.DataFrame(data)
# df.to_csv("employees.csv", index=False)

# import pandas as pd

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# file_path = 'https://api.slingacademy.com/v1/sample-data/files/employees.csv'
# dataframe = pd.read_csv(file_path, storage_options={
#                         'User-Agent': 'Mozilla/5.0'})

# dataframe.to_csv("employees.csv", index=False)
# print(dataframe.head())
# print(dataframe.describe())

# import kagglehub
# import pandas as pd
# # Download latest version
# path = kagglehub.dataset_download("zuhairkhan13/cleaning-practice-with-errors-and-missing-values")
# data_pd = pd.read_csv(path)
# data_pd.to_csv("employees.csv", index=False)
# print("Path to dataset files:", path)