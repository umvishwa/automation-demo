from google.cloud import secretmanager
from google.cloud import datastore
from google.cloud import storage
import os
import os.path
import gnupg
#Function to fetch keys from Secret and generate Fingerprint for Encryption 
path='/tmp/'

project_id= os.environ.get('project_id')
secretname= os.environ.get('secretname')
kind0= os.environ.get('kind0')
namespace0= os.environ.get('namespace0')

def encrypt(request): 
    datastore_client = datastore.Client()
    query = datastore_client.query(kind=kind0, namespace=namespace0)
    transactionid =  request.data
    query.add_filter('Transid','=', transactionid)
    data_list = list(query.fetch())
    data_dict = data_list[0]
    bucketname = data_dict['bucketname']
    out_bucketname =data_dict['targetbucketname']
    client = secretmanager.SecretManagerServiceClient()
    request0 = {"name": f"projects/{project_id}/secrets/{secretname}/versions/latest"}
    response = client.access_secret_version(request0)
    key= response.payload.data.decode('UTF-8')
    os.chdir(path)
    gpg = gnupg.GPG(gnupghome=path)
    import_result = gpg.import_keys(key)
    fingerprint=import_result.fingerprints[0]
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucketname)
    for blob in blobs:
        source_file_name = (str(blob.name))
        if (str(source_file_name.endswith('.csv')).lower() == 'true'): 
            bucket = storage_client.bucket(bucketname)
            blob = bucket.blob(source_file_name)
            fileContent = blob.download_as_string()
            os.chdir(path)
            gpg = gnupg.GPG(gnupghome=path)
            enc_data = gpg.encrypt(fileContent, fingerprint, always_trust=True) 
            blob_text = str(enc_data)
            target_file_name = source_file_name + '.enc'
            storage_client = storage.Client()
            bucket = storage_client.bucket(out_bucketname)
            blob = bucket.blob(target_file_name)
            blob.upload_from_string(blob_text,content_type='application/text')
            print(f'file encrypted: {target_file_name} success')
        else:
            print(f'File skipped condition not matched : {source_file_name}') 
    return 'Function Ended OK'
