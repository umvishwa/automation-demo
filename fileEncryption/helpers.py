import logging

# a function to read the fingerprint using the secret key provided
def readfingerprint(project_id,secretname):
    try :
        import os
        import os.path
        import gnupg
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()
        try:
            request0 = {"name": f"projects/{project_id}/secrets/{secretname}/versions/latest"}
            response = client.access_secret_version(request0)
            key= response.payload.data.decode('UTF-8')
            path='/tmp/'
            os.chdir(path)
            gpg = gnupg.GPG(gnupghome=path)
            import_result = gpg.import_keys(key)
            fingerprint=import_result.fingerprints[0]
            return fingerprint
        except:
            fingerprint='key not found'    
            return fingerprint
    except Exception as ex:
        print(str(ex))

# a function to read the source file from given bucket filepath
def readfilefrombucket(filepath, bucketname):
    try:
        from google.cloud import storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketname)
        try:
            blob = bucket.get_blob(filepath)
            blobsize = blob.size
            fileContent = blob.download_as_string()
        except:
            blobsize=None
            fileContent= 'No such object'
        return blobsize, fileContent 
    except Exception as ex:
        print(str(ex))

# a function to encrypt the file content using the PGP key fingerprint
def encryptfile(fileContent, fingerprint):
    try:
        import os
        import gnupg
        os.chdir('/tmp/')
        gpg = gnupg.GPG(gnupghome='/tmp/')
        enc_data = gpg.encrypt(fileContent, fingerprint, always_trust=True) 
        return enc_data
    except Exception as ex:
        print(str(ex))

# a function to write the encrypted file in the cloud storage filepath
def writefile(enc_data, bucketname, filepath , jsondata):
    try:
        blob_text = str(enc_data)
        target_file_name = filepath
        from google.cloud import storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketname)
        blob = bucket.blob(target_file_name)
        blob.upload_from_string(blob_text,content_type='application/text')
        return blob.exists(),target_file_name,('File  {} uploaded to Bucket  {}.'.format(target_file_name,bucketname))
    except Exception as ex:
        print(str(ex))
"""
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
        print(str(ex))
"""
# a function to publish success messsage to cloud pbsub topic
def publish_message_success(jsontext, project_id, topic_id):    
    try:
        from google.cloud import pubsub_v1
        import json
        from datetime import datetime
        from pytz import timezone
        timestampjson = {"completionTimestamp" : datetime.now(timezone('Europe/Stockholm')).strftime("%Y-%m-%d %H:%M:%S %p")}
        jsontext['status'] = 'COMPLETED'
        jsontext.update(timestampjson)
        jsontext = json.dumps(jsontext)
        data = jsontext.encode('utf-8')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        publisher.publish(topic_path, data)
        return data
    except Exception as ex:
        print(str(ex))
        
# a function to publish failed messsage to cloud pbsub topic
def publish_message_failed(jsontext, errormessage,project_id, topic_id):    
    try:
        from google.cloud import pubsub_v1
        import json
        from datetime import datetime
        from pytz import timezone
        timestampjson = {"completionTimestamp" :datetime.now(timezone('Europe/Stockholm')).strftime("%Y-%m-%d %H:%M:%S %p")}
        jsontext['status'] = 'FAILED'
        jsontext.update(timestampjson)
        jsontext.update(errormessage)
        jsontext = json.dumps(jsontext)
        data = jsontext.encode('utf-8')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        publisher.publish(topic_path, data)
        return data
    except Exception as ex:
        print(str(ex))
