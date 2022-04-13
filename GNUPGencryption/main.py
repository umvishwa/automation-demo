import helpers as helper
import json
import base64
import datetime
import os
import os.path
import logging
import datetime

#path='/tmp/'
now = datetime.datetime.now()
project_id= os.environ.get('project_id')
topic_id= os.environ.get('topic_id')
timestampjson = {"completionTimestamp" : now.strftime("%Y%m%d %H:%M:%S %p")}
            
def fileEncryption(request): 
 
    try:
        request_json = request.get_json()
        data = request_json['message']['data']
        jsontext = base64.b64decode(data).decode('utf-8')
        jsondata = json.loads(jsontext)
        secretname = jsondata['secretKeyForEncryption']
        bucketname = jsondata['bucketname']
        filepath = jsondata['filepath']
        jsondata.update(timestampjson)
        blobsize, file_Content =  helper.readfilefrombucket(filepath, bucketname)
        print('Message : Reading the source file path: gs://{}/{}' .format(bucketname,filepath))
        print('Message : filecontent = {}'.format(file_Content))
        if('No such object' in str(file_Content)):
            print('ERROR: Source file {} does not exist in the bucket {}'.format(filepath, bucketname))
            jsondata['status'] = 'FAILED'
            errormessage ={"ERROR_MESSAGE":"Error : 404 File Not Found"}
            jsondata.update(errormessage)
            publish_message = helper.publishmessage(jsondata, project_id, topic_id)
            return publish_message
        
        elif(str(blobsize)=='None'):
            print('ERROR: Empty file : gs://{}/{}' .format(bucketname,filepath))
            jsondata['status'] = 'FAILED'
            errormessage ={"ERROR_MESSAGE":"Error : 403 Empty File"}
            jsondata.update(errormessage)
            publish_message = helper.publishmessage(jsondata, project_id, topic_id)
            return publish_message

        else:
            print('Message : Reading Fingerprint from secret : {}..'.format(secretname))
        # Access the public key from secret manager and return the fingerprint
        finger_print = helper.readfingerprint(project_id,secretname)
        print('Message : Public key fingerprint {}'.format(finger_print))
        
        # Encrypt the content of the source file
        encdata = helper.encryptfile(file_Content, finger_print)
        if (encdata.status =='encryption ok'):
            print('Message : File content encrypted using key fingerprint. Encrypted PGP Messsage :')
            print(str(encdata))
        else:
            print('File encryption error, please verify the public key: {}'.format(secretname))
            jsondata['status'] = 'FAILED'
            errormessage={"ERROR_MESSAGE":"Error : 402 encryption error "}
            jsondata.update(errormessage)
            publish_message = helper.publishmessage(jsondata, project_id, topic_id)
            return publish_message
            raise ex
                
        #Push encrypted content in the file and upload in the bucket
        createFile, targetfilename, createFilemessage = helper.writefile(encdata, bucketname, filepath, jsondata)
        if((str(createFile)).strip()=='True'):
            print('Message : Encrypted file created: gs://{}/{} '.format(bucketname,targetfilename))
            jsondata['status'] = 'COMPLETED'
            publish_message = helper.publishmessage(jsondata, project_id, topic_id)
            return publish_message
        else:
            jsondata['status'] = 'FAILED'
            errormessage={"ERROR_MESSAGE":"Error : 401 File can not be created "}
            jsondata.update(errormessage)
            publish_message = helper.publishmessage(jsondata, project_id, topic_id)
            return publish_message
    except Exception as ex:
        return str(ex)
