import pandas as pd

# Sample employee table
data = {
    "employee_id": [101, 102, 103, 104, 104],  # Note: duplicate 104
    "first_name": ["Alice", "Bob", "Charlie", "David", "David"],
    "last_name": ["Smith", "Jones", "Brown", "Taylor", "Taylor"],
    "email": ["alice@company.com", "bob@company.com", None, "david@company.com", "david@company.com"],
    "department_id": [10, 20, 10, 30, 30],
    "salary": [70000, 80000, 75000, 90000, 90000]
}

df = pd.DataFrame(data)
df.to_csv("employees.csv", index=False)