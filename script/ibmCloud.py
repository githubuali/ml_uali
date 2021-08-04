from logging import exception
import os
import sys
from botocore.config import Config
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/ml_uali/script')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

COS_ENDPOINT = os.getenv("COS_ENDPOINT")
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")
COS_STORAGE_CLASS = os.getenv("COS_STORAGE_CLASS")
COS_AUTH_ENDPOINT = os.getenv("COS_AUTH_ENDPOINT")
SERVICE_INTANCE_ID = os.getenv("SERVICE_INTANCE_ID")


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)

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
        dir = path
        if not os.path.exists(dir):
            os.makedirs(dir)
        i = 0
        for k in keys:
            progress(i, len(keys), status='Descarga en progreso')
            print("Starting download of file {0}".format(k))
            cos.download_file(bucketName, k, os.path.join(dir, k))
            print("{0} donwloaded".format(k))
            i += 1
            
        print('All files downloaded.')
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            os.system.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    
    prefix = '22062021'
    
    download_path = '/home/maximiliano/ml_uali/inference/eventos/' +  prefix
    
    cos = configInstance()

    buckets = getBuckets(cos)
    
    keys = getObjectsNames(cos, buckets[0], prefix)
    
    downloadFiles(cos, buckets[0], keys, download_path)

