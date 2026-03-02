import os, uuid
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# helper that centralizes account lookup and credential creation so callers
# don’t have to duplicate the same setup logic in every operation.
def _get_blob_service_client():
    account = os.getenv("STORAGE_ACCOUNT_NAME")
    if not account:
        raise ValueError("STORAGE_ACCOUNT_NAME environment variable is not set")

    account_url = f"https://{account}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url, credential=credential)




def create_container(container_name, public=False):
    """
    Create a Container on the Storage Account
    
    Args:
        container_name: Name of the container to create
        public: If True, creates container with public access. If False, creates private container.
    """

    blob_service_client = _get_blob_service_client()

    try:
        if public:
            container_client = blob_service_client.create_container(container_name, public_access="container")
        else:
            container_client = blob_service_client.create_container(container_name)
    except Exception as e:
        if "ContainerAlreadyExists" in str(e):
            container_client = blob_service_client.get_container_client(container_name)
        else:
            raise


def upload_blob(container_name, blob_name, data):
    """
    Upload a Blob to the Container
    """

    blob_service_client = _get_blob_service_client()

    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(data)
    except Exception as e:
        if "BlobAlreadyExists" in str(e):
            print(f"Blob '{blob_name}' already exists in container '{container_name}'. Skipping upload.")
        else:
            raise

def list_blobs(container_name):
    """
    List the Blobs on the Container
    """

    blob_service_client = _get_blob_service_client()


    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs()

    blobs = []
    for blob in blob_list:
        blobs.append({
            "name": blob.name,
            "size": blob.size,
            "lastModified": blob.last_modified
        })

    return blobs

def delete_blob(container_name, blob_name):
    """
    Delete a Blob from the Container
    """

    blob_service_client = _get_blob_service_client()

    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
    except Exception as e:
        if "BlobNotFound" in str(e):
            print(f"Blob '{blob_name}' not found in container '{container_name}'. Skipping deletion.")
        else:
            raise