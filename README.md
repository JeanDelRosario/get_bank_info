# Purpose

Simple python > 3.7 program to get transaction information out of Banreservas, join all the information in a single dataset and save it into database/bank_transactions.csv. Also, if configured, it uploads the information to a Google Sheet.


## Usage

First install necessary requirements using `pip`.

```python
pip3 install -r requirements.txt
```

After that, there are two main files that need to be configured/personalized:

### Config.yml

After installing the required dependencies use the file `config.yml` to set up the script with necessary credentials and other required information needed.

If `enabled` inside `Gsheet` is set to `True`, `Gsheet_credentials_file` and `Gsheet_Id` will both need to be provided.

### Rules.txt

This file is in charge of classifying bank transactions. 

For this purpose, 4 flags have been created:

- **-s** [column_name] | [value]:

  Creates a new column in the final dataset with a default value that is provided.

  Example:

  `-s category | others`

  Creates a `category` column and assigns the default value to be `others`.
  
-  **-a** [array] | [column_name] | [column_to_modify] | [new_value]

   Looks in `column_name` for any value inside `array`, if a match is found `column_to_modify` is changed to `new_value`.

   Example:

   `-a 123, 456 | Transaction id | category | Restaurant`

   Assigns to the `category` column the value of `Restaurant` for all transactions that have a `Transaction id` equal to 123 or 456.

- **-l** [string] | [column_name] | [column_to_modify] | [new_value]
 
  Looks in `column_name` for all the values that contain `string` and then modify their `column_to_modify` to be `new_value`. Is case insensitive.

  Example:

  `-l WENDY | Description | category | Fast food`

  Assigns to the `category` column the value `Fast food` for all the transactions with a `Description` that contains the word `WENDY`.

- **-r** [query] | [column_to_modify] | [new_value]
 
  Filter the final transaction pandas dataset using the [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) method with `engine=python`. The query being provided by `query` finds the matching transactions and modifies `column_to_modify` to be `new_value`.

  This flag provides more flexibility for the matching of transactions.

  Example:

  `-r Concept.str.upper().str.contains("TRANSFERENCIA TERCERO") and Debit == 1000 | is_weekly_spend | True`

  Assigns the `is_weekly_spend` column the value `True` for all transactions that matches:
  
  ```python
  df.query('Concept.str.upper().str.contains("TRANSFERENCIA TERCERO") and Debit == 1000', engine='python')
  ```

Before using the **-a**, **-l** or **-r** flags make sure that `[column_to_modify]` and/or `[column_name]` exist in the CSV that is downloaded from Banreservas. If it doesn't make sure to create the columns using the **-s** flag as indicated above.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
