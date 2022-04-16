# File encryption using GnuPG

The repository contains the python code for csv file encryption using GnuPG utility. Cloud function reads Input message published to push-based subscription. The source file will be read from the source cloud storage path and encrypted using the public PGP key fingerprint defined in the google secret manager, The encrypted fill will be uploaded at target bucket filepath defined in the input message. Output message will be sent in response to suuccess or failure execution of the program


**Following error handling has been implemented in the cloud function**

|Error code	|Error description       |Description					        	| 
|---------------|:-----------------------|:--------------------------| 
|5001		| File Not Found	 |Raise error if the source file is missing from gs path	|
|5002		| Empty File		 |Raise error if the source file is empty			|
|5003		| key not found		 |Raise error if the secret key name is missing or invalid	|
|5004		| File not created	 |Raise error if the error appear while creating the target file|

**Sample Input message publish to push-based subscription**
```json
{
	"actionType": "fileEncryption", 
	"status": "INITIATED", 
	"interfaceName": "ADPTOTACK", 
	"countryCode": "AT",
	"transactionId": 4536844066750464, 
	"retryCount": 0, 
	"sourcefilepath": "incoming/files/persons.csv",
	"targetfilepath": "incoming/files/persons.csv.enc",
	"sourcebucketname": "demofiles001-source", 
	"targetbucketname": "demofiles001-target", 
	"secretKeyForEncryption": "pgp_encryption_public_key",
}
```

**Sample output message will be published to topic**

```json
{
	"actionType": "fileEncryption", 
	"status": "COMPLETED", 
	"interfaceName": "ADPTOTACK", 
	"countryCode": "AT",
	"transactionId": 4536844066750464, 
	"retryCount": 0, 
	"sourcefilepath": "incoming/files/persons.csv",
	"targetfilepath": "incoming/files/persons.csv.enc",
	"sourcebucketname": "demofiles001-source", 
	"targetbucketname": "demofiles001-target", 
	"secretKeyForEncryption": "pgp_encryption_public_key",
	"completionTimestamp": "2022-04-14 17:52:11 PM"
}
```

**Sample error message will be published to topic**

```json
{
	"actionType": "fileEncryption", 
	"status": "FAILED", 
	"interfaceName": "ADPTOTACK", 
	"countryCode": "AT",
	"transactionId": 4536844066750464, 
	"retryCount": 0, 
	"sourcefilepath": "incoming/files/persons.csv",
	"targetfilepath": "incoming/files/persons.csv.enc",
	"sourcebucketname": "demofiles001-source", 
	"targetbucketname": "demofiles001-target", 
	"secretKeyForEncryption": "pgp_encryption_public_key",
	"ERROR_MESSAGE": "404 File Not Found",
	"completionTimestamp": "2022-04-14 17:52:11 PM"
}
```
## Roles required for the service account 
* Secret manager secret accessor 
* Storage Object Admin
* Pub/Sub publisher

## Environment variable for the cloud function

* project_id   ---google cloud project name 
* topic_id     --- topic id to publish message

The public key shall be configured in the secret manager. The same public key will be used for encryption. The encrypted csv file can be decrypted by the end user 
using the private key pair and the passphrase.

## File Decryption using private key


Run the folllowing command in the specified order
- **gpg -import private-key.asc** - and provide a passphrase once opted. This passphrase will be later used while decryption of the file
- **gpg -list-secret-keys** - to displays the imported private key, it will display the fingerprint and expiry date of the key.
- **gpg -d paom.csv.enc** - to decrypt the encrypted file and enter the same passphrase given in step1. 

