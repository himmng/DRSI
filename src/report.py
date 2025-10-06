import pandas as pd
from datetime import datetime

def generate_report(results, table_name):
    df = pd.DataFrame(results, columns=["Column", "Check", "Failed_Count"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/{table_name}_data_quality_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Report saved to {filename}")
