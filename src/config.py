import os
import json
import pandas as pd

path = os.path.abspath(os.path.join(__file__, os.pardir))

def read_file(file_path):
    """
    Reads a file (CSV, TXT, Excel, Parquet) and returns a DataFrame.
    Tries to infer delimiter and handles common file types used in industry.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        return pd.read_csv(file_path, nrows=5)
    elif ext == ".txt":
        # Try common delimiters like tab or pipe
        try:
            return pd.read_csv(file_path, sep="\t", nrows=5)
        except Exception:
            return pd.read_csv(file_path, sep="|", nrows=5)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(file_path, nrows=5)
    elif ext == ".parquet":
        return pd.read_parquet(file_path)
    elif ext == ".json":
        # Load JSON-based table-style data if it’s a records format
        df = pd.read_json(file_path)
        if isinstance(df, dict):
            df = pd.json_normalize(df)
        return df.head()
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def get_config(data_dir="data", config_dir="config"):
    """
    Scans all supported files inside data_dir, extracts their headers,
    and generates JSON config templates for each file inside config_dir.
    """
    os.makedirs(config_dir, exist_ok=True)

    supported_extensions = [".csv", ".txt", ".xls", ".xlsx", ".parquet", ".json"]

    for filename in os.listdir(data_dir):
        ext = os.path.splitext(filename)[1].lower()

        if ext in supported_extensions:
            dataset_name = filename.replace(ext, "")
            file_path = os.path.join(data_dir, filename)
            
            try:
                df = read_file(file_path)
            except Exception as e:
                print(f"Skipping {filename}: {e}")
                continue

            # Generate a default config skeleton
            dataset_rules = {col: ["not_null"] for col in df.columns}

            config = {
                dataset_name: dataset_rules,
                "rules_config": {
                    "regex_patterns": {},
                    "ranges": {},
                    "allowed_values": {},
                    "date_format": "%Y-%m-%d"
                }
            }

            config_path = os.path.join(config_dir, f"{dataset_name}_config.json")
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

            print(f"Config generated for: {dataset_name} → {config_path}")

if __name__ == "__main__":
    get_config()
