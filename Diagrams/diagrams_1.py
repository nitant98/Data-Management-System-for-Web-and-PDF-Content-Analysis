from diagrams import Diagram, Cluster
from diagrams.programming.flowchart import Action, Database, Document
from diagrams.onprem.workflow import Airflow
from diagrams.saas.analytics import Snowflake
from diagrams.programming.language import Python
from diagrams.generic.storage import Storage
from diagrams.custom import Custom
# from diagrams.generic.compute import Task

with Diagram("Updated Workflow Diagram", show=False, direction="TB"):
    with Cluster("Automation - Command Execution"):
        execute_commands = Python("execute_commands.py")
        
    with Cluster("Step 1 - Web Scraping"):
        webscrape = Python("Webscrape (Python)")
        csv_file_webscrape = Storage("CSV\n(Web Scraping Output)")

        execute_commands >> webscrape >> csv_file_webscrape

    with Cluster("Step 2 - PDF Parsing and CSV Generation"):
        grobid_parsing = Python("grobid_parsing.py")
        xml_files = Storage("XML Files")
        csv_files_content = Storage("CSV Files\n(Content)")
        csv_files_metadata = Storage("CSV Files\n(Metadata)")
        execute_commands >> grobid_parsing
        grobid_parsing >> xml_files >> [csv_files_content, csv_files_metadata]

    with Cluster("Step 3 - Data Transfer to Snowflake"):
        snowflake_script = Python("snowflake.py")
        snowflake_db = Snowflake("Snowflake Database")

        execute_commands >> snowflake_script
        [csv_files_content, csv_files_metadata] >> snowflake_script >> snowflake_db

    with Cluster("Step 4 - DBT Cloud Integration via Airflow"):
        airflow = Airflow("Airflow Scheduler")
        dbt_cloud = Custom("DBT Cloud","dbt.png")

        airflow >> dbt_cloud
