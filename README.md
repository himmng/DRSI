# Data Readiness RSI module 
This module aims to acceralate the end-to-end data integration tasks for the target system with the help of recurssively self-improving (RSI) AI agents. The module consists of agents that will perform various data readiness tasks for a given source data system.

#### 1- Data Quality Agent
-   Tasks: Completeness, Uniqueness, Accuracy, Validity, Consistency, Timeliness
#### 2- Data Transformation Agent
-   Tasks: Enriching, Normalising, Joining, Aggeregating, Filtering, Cleaning
#### 3- Data Conversion Agent
-   Tasks: Assess, Format, Mapping, Load Test, Testing, Validating
#### 4- Data Preparation Agent
-   Tasks: Reports, Uploads

---

#### Download Repo:

- Setting Up:

    - load/upload data: set the path to the data 
    `path = "path_to_dataset"` or put data into `\data\` as `default_path`
    
        inside a python invironment run 
        ```
        #python 

        from DQRI.DQA import config
        
        data_path = "path_to_dataset"
        config_path = "path_to_save_config_files"
        config = config(path='default', data_path=None, config_path=None) # by default
        config.get_config(rules='default')
        ```

        It will read the header files from all datasets and create `.json` configuration files for the underline datasets. 
        ```
        output:

        config file/s successfully generated!
        ```
        An example `.json` file of a sample `employee` data looks like this:
        ```
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
        ```
        #python 
        #list config files

        list(config.list_config)
        ```
        example:
        ```
        output:

        employees.json
        sales.json
        product.json
        ...
        ```
    - generate DQI report:

        Once loading `data` and generating `config` complete, one can finally generate a first-order report of the underlying data. The code can perform the `uniqueness, consitstancy, accuracy, completeness, validity and timeliness` checks on the dataset.
        -   generate individual reports:

            ```
            from DQI.src import validate
            from DQI.src import config
            
            path = "path_to_dataset"
            config = config(path=path)
            config.get_config(rules='default')

            checks = validate(config=config, path=path)
            iter = 1 # for the first iteration
            uniq = checks.uniqueness(iter=iter)
            ```
            It will generate a uniqueness report for the data.

            example:
        
            ```
            output: 

            coverage: 98%

            report check_uniqueness_%iter.txt saved!

            ```

            Other examples of checks are `completeness(), validity(), accuracy(), timeliness(), consistancy()`.

        -   Generate a comprehensive check:

            Based upon different dataset we might require to perform only specific checks on the data. Comprehensive check enables to perform a list of `["completeness", "validity", "accuracy", "timeliness", "consistancy"]` or additional custom checks.

            ```
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

            ```
            output:

            comprehensive report generated!

            coverage 98%

            report check_comprehensvie_%iter.txt saved!
            ```
