# Azure Blob Storage Demo
By: Christian Kasih Pratama Setiawan

## Setup
1. Clone the Repository
2. Create a Python Virtual Environment
   > python -m venv .venv
3. Activate the Virtual Environment
   > pip install -r requirements.txt
4. Install the Python Packages
5. Create a Storage Account in an Azure Subscription
6. Create an App Regitration in the Entra ID Tenant
7. Create a Client Secret
8. Assign the Azure RBAC Role Assignment on the Storage Account (**Blob Storage Data Contributor**) to the Service Principal of the App Registration
9. Create a .env File with the following content:
    > STORAGE_ACCOUNT_NAME=<storage-account-name (from Step 5)>
    > 
    > PUBLIC_CONTAINER_NAME=public
    > 
    > PRIVATE_CONTAINER_NAME=private
    > 
    > AZURE_CLIENT_ID=<client-id (from Step 6)>
    > 
    > AZURE_TENANT_ID=<tenant-id (from Step 6)>
    > 
    > AZURE_CLIENT_SECRET=<client-secret (From Step 7)>
    > 
10. Run the Application
    > python app.py
