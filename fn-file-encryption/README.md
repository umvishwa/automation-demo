# File encryption using gnupg utility.

The cloud function requires a transid from the datastore kind as the input. The datastore should have mapping between transid and bucketname this bucketname will be used to pick 
the source csv file for encryption, the file can sit in the recursive directories , once the function is run the source file will be picked up for encryption
and the encrypted file be saved in the target bucket with an extension filename.csv.enc

|transid  |  sourcebucketname |targetbucketname   |
|--------:|:-----------------:|:------------------|
|100	  |demofiles001-source|demofiles001-target|

## Environment variable for the cloud function:

* project_id   ---google cloud project name 
* secretname -- pgp public key secret name
* kind0 -- kind name from the datastore
* namespace0 -- namespace from the datastore

The public key shall be configured in the secret manager. The same public key will be used for encryption. The encrypted csv file can be decrypted by the end user 
using the private key pair and the passphrase.

## Decryption:
	1. Run the command gpg -import private-key.asc and provide a passphrase once opted. This passphrase will be later used while decryption of the file.
	2. Run the command gpg -list-secret-keys to displays the imported private key, it will display the fingerprint and expiry date of the key.
	3. Run the command gpg -d paom.csv.enc to decrypt the encrypted file and enter the same passphrase given in step1. 
