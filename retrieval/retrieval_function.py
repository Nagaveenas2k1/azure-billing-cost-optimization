import json
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

def deserialize(blob_data):
    return json.loads(blob_data.readall())

def get_billing_record(record_id, cosmos_url, db_key, db_name, container_name, blob_conn_str):
    cosmos = CosmosClient(cosmos_url, credential=db_key)
    container = cosmos.get_database_client(db_name).get_container_client(container_name)
    blob_service = BlobServiceClient.from_connection_string(blob_conn_str)
    blob_client = blob_service.get_container_client("billing-archive")

    try:
        record = container.read_item(record_id, partition_key=record_id)
        return record
    except:
        blob_data = blob_client.download_blob(f"{record_id}.json")
        return deserialize(blob_data)

