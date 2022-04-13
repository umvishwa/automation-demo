import logging


def readfingerprint(project_id,secretname):
    try :
        import os
        import os.path
        import gnupg
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()
        request0 = {"name": f"projects/{project_id}/secrets/{secretname}/versions/latest"}
        response = client.access_secret_version(request0)
        key= response.payload.data.decode('UTF-8')
        path='/tmp/'
        os.chdir(path)
        gpg = gnupg.GPG(gnupghome=path)
        import_result = gpg.import_keys(key)
        fingerprint=import_result.fingerprints[0]
        return fingerprint
    except Exception as ex:
        raise str(ex)

def readfilefrombucket(filepath, bucketname):
    try:
        from google.cloud import storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketname)
        blob = bucket.get_blob(filepath)
        fileContent = blob.download_as_string()
        return blob.size, fileContent 
    except Exception as ex:
        raise str(ex)


def encryptfile(fileContent, fingerprint):
    try:
        import os
        import gnupg
        os.chdir('/tmp/')
        gpg = gnupg.GPG(gnupghome='/tmp/')
        enc_data = gpg.encrypt(fileContent, fingerprint, always_trust=True) 
        return enc_data
    except Exception as ex:
        raise ex

def writefile(enc_data, bucketname, filepath , jsondata):
    try:
        blob_text = str(enc_data)
        target_file_name = filepath + '.enc'
        from google.cloud import storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketname)
        blob = bucket.blob(target_file_name)
        blob.upload_from_string(blob_text,content_type='application/text')
        return blob.exists(),target_file_name,('File  {} uploaded to Bucket  {}.'.format(target_file_name,bucketname))
    except Exception as ex:
        raise ex

def publishmessage(jsontext, project_id, topic_id):    
    try:
        from google.cloud import pubsub_v1
        import json
        jsontext = json.dumps(jsontext)
        data = jsontext.encode('utf-8')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        publisher.publish(topic_path, data)
        return data
    except Exception as ex:
        raise ex
