from flask import Flask,render_template, request, jsonify
import os, uuid


import azure_utils as az

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

private_container_name = os.getenv("PRIVATE_CONTAINER_NAME")
public_container_name = os.getenv("PUBLIC_CONTAINER_NAME")

def initialize():
    """
    Initialize the Application
    """
    az.create_container(private_container_name, public=False)
    az.create_container(public_container_name, public=True)

    private_blob_data = open("to Upload/microsoft-azure-blob-storage-logo.png", "rb").read()
    az.upload_blob(public_container_name, "microsoft-azure-blob-storage-logo.png", private_blob_data)

initialize()

"""
Web Server Endpoints
"""
@app.route('/home', methods=['GET'])
def getHome():

    return render_template('home.html')

"""
API Server Endpoints
"""
@app.route('/api/blobs', methods=['GET'])
def getBlobs():

    """
    Get the Blobs on the Container
    """

    print("/api/blobs GET endpoint called")
    data = az.list_blobs(private_container_name)

    print(f"Data retrieved: {data}")

    return {
        "status": "success",
        "message": "Blobs listed successfully!",
        "data": data
    }

@app.route('/api/blobs/upload', methods=['POST'])
def uploadBlob():

    """
    Upload a Blob to the Container
    """

    file = request.files['file']
    filename = file.filename
    file_data = file.read()

    az.upload_blob(private_container_name, filename, file_data)

    return {
        "status": "success",
        "message": f"Blob {filename} uploaded successfully!",
        "data": []
    }

@app.route('/api/blob/<blob_name>/delete', methods=['DELETE'])
def deleteBlob(blob_name):

    az.delete_blob(private_container_name, blob_name)

    return {
        "status": "success",
        "message": f"Blob {blob_name} deleted successfully!",
        "data": []
    }

@app.route('/api/blob/<blob_name>/download', methods=['GET'])
def downloadBlob(blob_name):

    print(f"/api/blob/{blob_name}/download GET endpoint called")
    blob_service_client = az._get_blob_service_client()
    container_client = blob_service_client.get_container_client(private_container_name)
    blob_client = container_client.get_blob_client(blob_name)

    download_stream = blob_client.download_blob()

    return download_stream.readall()

app.run(host='0.0.0.0', port=80)