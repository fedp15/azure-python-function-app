# azure-python-function-app
template and documentation to build an Azure function app in python.

## Requirements
Locally:
1. Python 3.*
2. [Azure Functions Core Tools and Visual Studio Code](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-01#configure-your-environment)

In Azure:
1. A resource group for linux resources (BEST PRACTISE: make a new resource group for each project)
2. The role of "Contributor" in that resource group (ask Maarten)

## Steps
1. [create a python function with Visual Data Studio](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-02)
2. Copy-paste your script into `__init__.py`
3. Copy-paste the requirements of your python script into `requirements.txt`. RECOMMENDED: add only what is needed. If in doubt, start a new virtual env for your project, install only what is needed and then get requirements with
```sh 
$ pip freeze > requirements.txt
```
4. Configure how often your function will run in `function.json`: edit the [cron expression](https://crontab.guru/) in the field `schedule`
5. Debug locally using Visual Studio Code, e.g. via the terminal execute this command from the root folder
```sh 
$ func start --functions <my-function> --python --verbose --build remote
```
6. [Deploy to Azure using Visual Studio Code](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-05)

You will now be able to monitor your function in the [Azure portal](https://portal.azure.com/). A new resource of type "Application Insights" will be created, where you can monitor runs, errors, etc. Good to know: you can also check the logs in the Function App under `Functions > <my-function> > Code + Test > Logs`

## Data
If your function takes data as input/output, the recommended workflow is to store the data in an Azure storage and download/upload it from/to there.

When you create a new function with Visual Data Studio a new storage account will be created automatically in the same resource group; you can use this one or an existing one. Good to know: individual files in Azure storage are called 'blobs' and directories 'containers'.
1. Create a container within the storage via the Azure portal
2. Upload your data in the container
They way your function exchange data with the storage is via [azure-storage-blob](https://pypi.org/project/azure-storage-blob/), which needs the rights credentials. If you are using the default storage that is created with the function, the credentials are already stored in an environmental variable named `AzureWebJobsStorage`; you can get it with
```
credentials = os.environ['AzureWebJobsStorage']
```
and then get your data with e.g.
```
blob_service_client = BlobServiceClient.from_connection_string(credentials)
blob_client = blob_service_client.get_blob_client(container='<my-container>', blob='<my-data-file>')
data = pickle.loads(blob_client.download_blob().readall())
```
3. [OPTIONAL] If you are using a different storage, [copy the credentials from the Azure portal](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#copy-your-credentials-from-the-azure-portal) and [add it in the function settings](https://docs.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-azure-function-app-settings#settings) (so that they will be callable within the function as environmental variables)

## Credentials, keys and secrets
If your function needs to use an API (e.g. Google Maps) and requires credentials, **do NOT store them in `__init__.py`**, since this will expose them to whoever has access to the resource group. The recommended workflow is to store them in an Azure key vault.
1. Create an Azure Key Vault in the same resource group
2. Ask to be given the role of "Key Vault Secrets Officer" in the vault (ask the admin of the resource group)
3. Add your credentials in the vault under `Secrets`, via the Azure portal
4. [Integrate the credentials in your function app](https://daniel-krzyczkowski.github.io/Integrate-Key-Vault-Secrets-With-Azure-Functions/)
