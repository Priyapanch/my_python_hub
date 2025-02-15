import great_expectations as gx
from great_expectations.data_context import DataContext
import pandas as pd
from sqlalchemy import create_engine
from confluent_kafka import Consumer
import json
import boto3
import smtplib

# Initialize Great Expectations Context
context = DataContext()

# ==========================
# 1. DB2 DATA VALIDATION
# ==========================
DB2_CONNECTION_STRING = "ibm_db_sa://user:password@host:port/dbname"
db_engine = create_engine(DB2_CONNECTION_STRING)

def validate_db2():
    expectation_suite = "db2_expectations"
    batch_request = {
        "datasource_name": "db2_datasource",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": "your_table",
        "limit": 100
    }
    
    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=expectation_suite)
    results = validator.validate()
    return results.success

# ==========================
# 2. KAFKA STREAM VALIDATION
# ==========================
consumer = Consumer({
    'bootstrap.servers': 'your_kafka_broker',
    'group.id': 'etl-test-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['your_kafka_topic'])

def validate_kafka():
    messages = []
    while len(messages) < 10:
        msg = consumer.poll(1.0)
        if msg is not None:
            messages.append(json.loads(msg.value()))
    
    df = pd.DataFrame(messages)
    validator = context.get_validator(batch=pd.DataFrame(df), expectation_suite_name="kafka_expectations")
    results = validator.validate()
    return results.success

# ==========================
# 3. AWS S3 DATA VALIDATION
# ==========================
s3_client = boto3.client("s3")
def validate_s3(bucket_name, file_key):
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(obj['Body'])
    
    validator = context.get_validator(batch=pd.DataFrame(df), expectation_suite_name="s3_expectations")
    results = validator.validate()
    return results.success

# ==========================
# 4. CI/CD AUTOMATION & ALERTS
# ==========================
def send_alert(message):
    with smtplib.SMTP("smtp.your-email.com") as server:
        server.sendmail("from@example.com", "to@example.com", message)

def run_etl_validation():
    db2_result = validate_db2()
    kafka_result = validate_kafka()
    s3_result = validate_s3("your-bucket", "data.csv")
    
    if not (db2_result and kafka_result and s3_result):
        send_alert("ETL validation failed!")
    
    return {"DB2": db2_result, "Kafka": kafka_result, "S3": s3_result}

# Execute ETL Validation
test_results = run_etl_validation()
print(test_results)
