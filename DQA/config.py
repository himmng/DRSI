import os
import json
import pandas as pd

class Config:
    def __init__(self, config_path=None, data_path=None, path='default'):
        """
        Initialise config and data directories.
        Automatically sets paths one level above current file if 'default' is used.
        """
        if path == 'default':
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_path = data_path or os.path.join(base_path, 'data')
            self.config_path = config_path or os.path.join(base_path, 'config')
        else:
            self.data_path = data_path
            self.config_path = config_path

        os.makedirs(self.config_path, exist_ok=True)

    def read_file(self, file_path):
        """
        Reads a supported file and returns a small sample DataFrame.
        Handles CSV, TXT, Excel, Parquet, and JSON formats.
        """
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == ".csv":
                return pd.read_csv(file_path, nrows=5)
            elif ext == ".txt":
                try:
                    return pd.read_csv(file_path, sep="\t", nrows=5)
                except Exception:
                    return pd.read_csv(file_path, sep="|", nrows=5)
            elif ext in [".xls", ".xlsx"]:
                return pd.read_excel(file_path, nrows=5)
            elif ext == ".parquet":
                return pd.read_parquet(file_path).head()
            elif ext == ".json":
                df = pd.read_json(file_path)
                if isinstance(df, dict):
                    df = pd.json_normalize(df)
                return df.head()
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except Exception as e:
            raise ValueError(f"Error reading {file_path}: {e}")

    def get_config(self, rules='default'):
        """
        Loops through all supported files inside data_dir,
        extracts their headers, and generates JSON config templates
        for each file inside config_dir.
        """
        supported_extensions = [".csv", ".txt", ".xls", ".xlsx", ".parquet", ".json"]

        # Loop through every file in the data directory
        for filename in os.listdir(self.data_path):
            file_path = os.path.join(self.data_path, filename)
            ext = os.path.splitext(filename)[1].lower()

            if ext not in supported_extensions:
                print(f"Skipping unsupported file type: {filename}")
                continue

            try:
                df = self.read_file(file_path)
            except Exception as e:
                print(f"Skipping {filename} due to read error: {e}")
                continue

            dataset_name = os.path.splitext(filename)[0]

            # Default rule config: every column must be not_null
            dataset_rules = {col: ["not_null"] for col in df.columns}

            # Define a generic config structure
            config = {
                "dataset_name": dataset_name,
                "columns": dataset_rules,
                "rules_config": {
                    "regex_patterns": {
                        "email": "[^@]+@[^@]+\\.[^@]+"
                    },
                    "ranges": {
                        "age": [18, 100],
                        "salary": [20000, 500000]
                    },
                    "allowed_values": {},
                    "date_format": "%Y-%m-%d"
                }
            }

            # Save each config file inside /config/
            config_file = os.path.join(self.config_path, f"{dataset_name}_config.json")
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

            print(f"Config generated for: {dataset_name} → {config_file}")
