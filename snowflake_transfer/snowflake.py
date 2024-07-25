import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from pathlib import Path

# Load environment variables
load_dotenv()

# Establish a connection to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse='SF_WH_CASE1',  # Adjusted as per your working setup
    database='SF_DB_CASE1',   # Adjusted as per your working setup
    schema='SF_CASE1',        # Adjusted as per your working setup
    role='SYSADMIN'           # Adjusted as per your working setup
)

# Function to map pandas data types to Snowflake SQL types, slightly simplified
def pandas_dtype_to_snowflake_sql_type(dtype):
    mapping = {
        'int64': 'NUMBER',
        'float64': 'FLOAT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP_NTZ',
        'object': 'VARCHAR'
    }
    return mapping.get(str(dtype), 'VARCHAR')

# Function to dynamically create tables based on DataFrame's structure
def create_table_from_df(df, table_name, conn):
    if not table_name[0].isalpha() or not table_name.isidentifier():
        table_name = f'"{table_name}"'

    # Adjust column definitions, quoting column names as necessary
    column_definitions = ', '.join([f'"{col.upper()}" {pandas_dtype_to_snowflake_sql_type(str(dtype))}' for col, dtype in df.dtypes.items()])

    # Assuming database and schema are set in the connection or environment variables
    create_table_sql = f"CREATE OR REPLACE TABLE {table_name} ({column_definitions})"

    # Execute the SQL command
    conn.cursor().execute(create_table_sql)

# Function to upload a CSV file to Snowflake, using the relative paths
def upload_csv_to_snowflake(csv_path, table_name, conn):
    df = pd.read_csv(csv_path)
    # Ensuring column names are uppercase for Snowflake compatibility
    df.columns = [col.upper() for col in df.columns]
    create_table_from_df(df, table_name, conn)
    write_pandas(conn, df, table_name.upper())
    print("Data Transfer Completed!!")

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent

    # Relative paths to CSV files, assuming this script is located correctly in your project structure
    csv_files = {
        'cleaned_extracted': project_root/ 'Updated_CSV'/ 'cleaned_extracted.csv',
        'grobid_content_2024_l1_topics_combined_2': project_root/ 'grobid_step/parsed_into_schema/content/csv' / 'grobid_content_2024_l1_topics_combined_2.csv',
        'grobid_content_2024_l2_topics_combined_2': project_root/ 'grobid_step/parsed_into_schema/content/csv' / 'grobid_content_2024_l2_topics_combined_2.csv',
        'grobid_content_2024_l3_topics_combined_2': project_root/ 'grobid_step/parsed_into_schema/content/csv' / 'grobid_content_2024_l3_topics_combined_2.csv',
        'grobid_metadata_2024_l1_topics_combined_2': project_root/ 'grobid_step/parsed_into_schema/metadata/csv' / 'grobid_metadata_2024_l1_topics_combined_2.csv',
        'grobid_metadata_2024_l2_topics_combined_2': project_root/ 'grobid_step/parsed_into_schema/metadata/csv' / 'grobid_metadata_2024_l2_topics_combined_2.csv',
        'grobid_metadata_2024_l3_topics_combined_2': project_root/ 'grobid_step/parsed_into_schema/metadata/csv' / 'grobid_metadata_2024_l3_topics_combined_2.csv',
    }

    # Process each CSV file
    for table_name, csv_file_path in csv_files.items():
            if os.path.exists(csv_file_path):
                upload_csv_to_snowflake(csv_file_path, table_name, conn)
            else:
                print(f"File not found: {csv_file_path}")

        # Close the Snowflake connection
    conn.close()
