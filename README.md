# Data Readiness RSI module 
This module aims to perform end-to-end data readiness tasks using __recurssively self-improving (RSI)__ AI agents. The module consists of various independently running AI agents that will accelerate the data readiness tasks for a given source data system.

#### 1- Data Quality Agent
-   Tasks: Completeness, Uniqueness, Accuracy, Validity, Consistency, Timeliness
#### 2- Data Transformation Agent
-   Tasks: Enriching, Normalising, Joining, Aggeregating, Filtering, Cleaning
#### 3- Data Conversion Agent
-   Tasks: Assess, Format, Mapping, Load Test, Testing, Validating
#### 4- Data Preparation Agent
-   Tasks: Reports, Uploads

---
### Current Progress:
-   __Data Quality Agent__: 
    -   __Raw Data Ingestion__: From external sources, APIs, manual load
    -   __Building Metadata__: Understanding the source schema, building ```.json``` style config. for various datasets.
    -   __DQI checks__: Data Completeness, Data Uniqueness, Data Accuracy, Data Consitency, Data Timeliness
    -   __DQI reports__: store ```.json``` style metadata report on the processed data.

---

### Documentation:

- __Setup__:
    - download the repo: ```git clone https://github.com/himmng/DRSI.git```
-   __Loading the Data__: 
    - __using API__: 
        ```python
        API_CONFIG="api_key"
        data_path = "path_to_dataset"
        ```

    - __manual data load/upload method__: set the path to the data 
    `path = "path_to_dataset"` or put data into `\data` as `default_path`
        ```python
        data_path = "path_to_dataset"
        ```
-   __Metadata Builder (understanding the source schema)__:
    ```python 
    from DQRI.DQA import config
    data_path = "path_to_dataset"
    config_path = "path_to_save_config_files"
    config = config(path='default', data_path=None, config_path=None) # by default
    config.get_config(rules='default')
    ```
    Read the header files from all datasets and create `.json` configuration files for the underline datasets. 
    
    ```python
    output:

    config file/s successfully generated!
    ```

    An example `.json` file of a sample `employee` data looks like this:

    ```python
    {
    "employees": {
        "Employee_ID": ["not_null", "unique"]
        "Name": ["not_null"],
        "Gender": ["not_null"],
        "Age":["ranges"],
        "Email": ["not_null", "regex"]
        },
    "rules_config": {
        "regex_patterns": {
        "Email": "[^@]+@[^@]+\\.[^@]+"
        },
        "ranges": {
        "Age": [14, 100]
        }
        }
    }
    ```

    The rules for the data columns are defined automatically by `default`, however, they can be modified manually for the case:

    ```python 
    #list config files

    list(config.list_config)
    ```
    example:

    ```python
    output:

    employees.json
    sales.json
    product.json
    ...
- __generate DQI report__:

    Once loading `data` and generating `config` complete, one can finally generate a first-order report of the underlying data in a `.json` format. The code can perform the `uniqueness, consitstancy, accuracy, completeness, validity and timeliness` checks on the dataset.
    -   __individual report__:

        ```python
        from DQI.src import validate
        from DQI.src import config
        
        path = "path_to_dataset"
        config = config(path=path)
        config.get_config(rules='default')

        checks = validate(config=config, path=path)
        iter = 1 # for the first iteration
        uniq = checks.uniqueness(iter=iter)

        ```
        example:
    
        ```python
        output: 

        coverage: 98%

        report check_uniqueness_%iter.json saved!

        ```
        Other examples of checks are `completeness(), validity(), accuracy(), timeliness(), consistancy()`.

    -   __comprehensive report__:

        Based upon different dataset we might require to perform only specific checks on the data. Comprehensive check enables to perform a list of `["completeness", "validity", "accuracy", "timeliness", "consistancy"]` or additional custom checks.

        ```python
        checks = validate(config=config, path=path)
        iter = 1
        checks_list = ["completeness", "accuracy"]

        # case 1: from generic checks_list
        comp_check = checks(iter=iter, checks_list=checks_list)

        # case 2: from custom/external check function/class

        def custom_check():
            ...
            # define the functions

            return 

        comp_check = checks(iter=iter, checks_list=None,ext_check_func=custom_check)

        # case 3: combined generic+custom checks

        comp_check = checks(iter=iter, checks_list=checks_list,ext_check_func=custom_check)
        ```

        ```python
        output:

        comprehensive report generated!

        coverage 98%

        report check_comprehensvie_%iter.json saved!
        ```
        example DQI report `.json` file:
        ```python
        
        {
        "dataset": "sales_NRI",
        "date": "2025-10-13",
        "results": {
            "completeness": 0.99,
            "uniqueness": 1.00,
            "accuracy": 0.97,
            "consistency": 0.98,
            "timeliness": "Pass"
        },
        "remarks": [
            "2 rows with negative amount found",
            "Customer_id mismatch with master data: 12 cases"
        ]
        }
        ```


