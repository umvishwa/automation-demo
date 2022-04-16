import helpers as helper
import json
import base64
import datetime
import os
import os.path
import logging

logging.basicConfig(level=logging.INFO)

project_id= os.environ.get('project_id')
topic_id= os.environ.get('topic_id')


def fileEncryption0(request): 
 
    try:
        # Reading the attributes from input message
        request_json = request.get_json()
        data = request_json['message']['data']
        jsontext = base64.b64decode(data).decode('utf-8')
        jsondata = json.loads(jsontext)
        secretname = jsondata['secretKeyForEncryption']
        sourcebucketname = jsondata['sourcebucketname']
        sourcefilepath = jsondata['sourcefilepath']
        targetfilepath = jsondata['targetfilepath']
        targetbucketname = jsondata['targetbucketname']
        interfaceName = jsondata['interfaceName']
        transactionId = jsondata['transactionId']
        
        # Reading the source file content
        blob_size,file_Content =  helper.readfilefrombucket(sourcefilepath, sourcebucketname)
        logging.info('Message : Reading the source file path: gs://{}/{} for interface {} and transactionid {}' .format(sourcebucketname,sourcefilepath,interfaceName,transactionId))
        logging.info('Message : filesize {} Bytes '.format(blob_size))
        if('No such object' in str(file_Content)):
            logging.info('ERROR: Source file {} does not exist in the bucket {}'.format(sourcefilepath, sourcebucketname))
            errormessage ={"ERROR_MESSAGE":"5001 File Not Found "}
            publish_message = helper.publish_message_failed(jsondata, errormessage,project_id, topic_id)
                    
        elif(str(blob_size)=='0'):
            logging.info('ERROR: Empty file : gs://{}/{}' .format(sourcebucketname,sourcefilepath))
            errormessage ={"ERROR_MESSAGE":"5002 Empty File"}
            publish_message = helper.publish_message_failed(jsondata, errormessage,project_id, topic_id)
            
        else:
            logging.info('Message : Reading Fingerprint from secret ')
            # Access the public key from secret manager and return the fingerprint
            finger_print = helper.readfingerprint(project_id,secretname)
            if (str(finger_print)=='key not found'):
                errormessage={"ERROR_MESSAGE":"5003 key not found "}
                publish_message = helper.publish_message_failed(jsondata, errormessage,project_id, topic_id)       
            
            else:
                logging.info('Message : Encryption in progress..')
            
                #Encrypt the content of the source file
                encdata = helper.encryptfile(file_Content, finger_print)
                        
                #Push encrypted content in the file and upload in the bucket
                createFile, targetfilename, createFilemessage = helper.writefile(encdata, targetbucketname, targetfilepath, jsondata)
                if((str(createFile)).strip()=='True'):
                    logging.info('Message : Encrypted file created: gs://{}/{} '.format(targetbucketname,targetfilename))
                    publish_message = helper.publish_message_success(jsondata, project_id, topic_id)
                    
                else:
                    errormessage={"ERROR_MESSAGE":"5004 File not created "}
                    publish_message = helper.publish_message_failed(jsondata, errormessage,project_id, topic_id)
        return publish_message   
    except Exception as ex: 
        logging.error('Function returned an error ' + str(ex))
        errormessage={"ERROR_MESSAGE": str(ex)}
        publish_message = helper.publish_message_failed(jsondata, errormessage,project_id, topic_id)
        return publish_message
