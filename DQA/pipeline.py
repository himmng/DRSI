import json
from extract import load_data_from_csv
from validate import run_validations
from report import generate_report

def main():
    # Load configuration
    with open("config/rules.json") as f:
        config = json.load(f)

    for table_name, table_rules in config.items():
        if table_name == "rules_config":
            continue

        # Extract data
        file_path = f"data/{table_name}.csv"
        ddf = load_data_from_csv(file_path)  # For Oracle: load_data_from_sql(...)
        
        # Validate
        results = run_validations(ddf, table_name, table_rules, config["rules_config"])
        
        # Generate report
        generate_report(results, table_name)

if __name__ == "__main__":
    main()
