from logging import exception
import os
from botocore.config import Config
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "iXZodzfjKg0tjpEBKXgkIEr4SdSU6JCpotFkHpAkCSdf"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/84c0cb9f8c5348c7955d1cd9631ec63b::serviceid:ServiceId-e6be485f-2205-482b-964d-fd03c810945a"
COS_STORAGE_CLASS = "us-south"
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
SERVICE_INTANCE_ID = "crn:v1:bluemix:public:cloud-object-storage:global:a/84c0cb9f8c5348c7955d1cd9631ec63b:16623d92-4943-4b41-af8a-e4b1d4c4132f::"


def configInstance():
    """
    Returns an ibm_boto3 instance with credentials to the cloud storage
    """
    return ibm_boto3.client(
        "s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=SERVICE_INTANCE_ID,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )

def getBuckets(cos):
    """
    Returns an array of buckets in cloud 

    cos: Client instance
    """
    res = []
    print("Retrieving list of buckets")
    try:
        buckets = cos.list_buckets()
        for b in buckets['Buckets']:
            res.append(b['Name'])

        return res

    except ClientError as err:
        print("CLIENT ERROR: {0}\n".format(err))
    except Exception as err:
        print("Unable to retrieve list buckets: {0}".format(err))


def getObjectsNames(cos, bucketName, prefix):
    """
    Returns an array of objects in bucket

    cos: Client instance
    bucketName: string
    prefix: string
    """
    res = []
    print("Retrieving objects in specified bucket")

    try:
        keys = cos.list_objects_v2(
            Bucket = bucketName,
            EncodingType = 'url',
            Prefix = prefix
        )

        for k in keys['Contents']:
            res.append(k['Key'])

        return res

    except Exception as err:
        print("Unable to retrieve obejcts: {0}".format(err))


def downloadFiles(cos, bucketName, keys, path):
    """
    Download Files in determined path

    cos: Client Instance
    bucketName: String
    objects: Array 
    path: String
    """
    print('Downloading files')

    try:
        dir = os.path.join(os.getcwd(), path)
        print(dir)
        if not os.path.exists(os.path.dirname(dir)):
            os.makedirs(dir)

        for k in keys:
            print("Starting download of file {0}".format(k))
            cos.download_file(bucketName, k, os.path.join(dir, k))
            print("{0} donwloaded".format(k))

        print('All files downloaded.')
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            os.system.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    cos = configInstance()

    buckets = getBuckets(cos)
    
    keys = getObjectsNames(cos, buckets[0], '22062021')

    downloadFiles(cos, buckets[0], keys, 'descargas')

