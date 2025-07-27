import datetime
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import json

def serialize(record):
    return json.dumps(record)

def archive_old_records(cosmos_url, db_key, db_name, container_name, blob_conn_str, cutoff_days=90):
    cosmos = CosmosClient(cosmos_url, credential=db_key)
    container = cosmos.get_database_client(db_name).get_container_client(container_name)
    blob_service = BlobServiceClient.from_connection_string(blob_conn_str)
    container_client = blob_service.get_container_client("billing-archive")
    
    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=cutoff_days)
    query = "SELECT * FROM c WHERE c.record_date < @cutoff"
    for item in container.query_items(query, parameters=[{"name": "@cutoff", "value": cutoff_date.isoformat()}], enable_cross_partition_query=True):
        blob_name = f"{item['id']}.json"
        container_client.upload_blob(blob_name, serialize(item))
        container.delete_item(item, partition_key=item['id'])

# Example: call archive_old_records() with your credentials in a scheduled Azure Function

