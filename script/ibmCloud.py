# -*- coding: utf-8 -*-
#
# @Author: https://mecantronic.com.ar/
# @Version: 1.0
# @Date: sep2021
# @Status: developing


from logging import exception
import os
import sys
from botocore.config import Config
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from dotenv import load_dotenv
from tqdm import tqdm

def getEnv (path):
    """ Returns environment variables 

    Arg: 
        path (string) : path of enviroment '.env' file.

    Returns: 
        None
    """

    try:
        if not os.path.exists(path):
            raise NameError (path + " or .env not found") # Exceptions: https://docs.python.org/3/library/exceptions.html
        else:
            load_dotenv(path)
            global COS_ENDPOINT 
            global COS_API_KEY_ID 
            global COS_INSTANCE_CRN
            global COS_STORAGE_CLASS 
            global COS_AUTH_ENDPOINT 
            global SERVICE_INTANCE_ID 

            COS_ENDPOINT = os.getenv("COS_ENDPOINT")
            COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
            COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")
            COS_STORAGE_CLASS = os.getenv("COS_STORAGE_CLASS")
            COS_AUTH_ENDPOINT = os.getenv("COS_AUTH_ENDPOINT")
            SERVICE_INTANCE_ID = os.getenv("SERVICE_INTANCE_ID")
    
    except Exception as error:
        print("[ERROR] "+ repr(error))


def progress(count, total, status=''):
    """ Show progress bar

    Arg: 
        count (int) : loop index.
        total (int) : total index.
        status (string): message on the terminal.

    Returns: 
        None
    """

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


def configInstance():
    """ Returns an ibm_boto3 instance with credentials to the cloud storage

    Arg: 
        None

    Returns:
        None 
    """

    return ibm_boto3.client(
        "s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=SERVICE_INTANCE_ID,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )


def getBuckets(cos):
    """ Returns an array of buckets in cloud 
    
    Arg: 
        cos (ibm class): Client instance.
    
    Return:
        res (list) : list of buckets.
    """

    res = []
    print("* Retrieving list of buckets")

    try:
        buckets = cos.list_buckets()
        
        for b in buckets['Buckets']:
            res.append(b['Name'])

        return res
        
    except ClientError as err:
        print("[ERROR] Client error: {0}\n".format(err))
    
    except Exception as err:
        print("[ERROR] Unable to retrieve list buckets: {0}".format(err))


def getObjectsNames(cos, bucketName, prefix):
    """ Returns an array of objects in bucket

    Arg:
        cos (ibm class): client instance.
        bucketName (string): name of bucket. 
        prefix (string): object name.
    
    Return:
        res (list) : specified bucket.
    """

    res = []
    print("* Retrieving objects in specified bucket")

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


def downloadFiles(cos, bucketName, keys, path, progress_show):
    """ Download Files in determined path

    Arg:
        cos (ibm class): client instance.
        bucketName (string): name of bucket.
        keys (array): to download. 
        path (string): path for download image.
        progress_show (string): "full" or "resume"
    
    Returns:
        None 
    """
   
    print('* Downloading files')

    try:
        dir = path
        if not os.path.exists(dir):
            os.makedirs(dir)
        i = 0

        if progress_show == 'full':
            for k in keys:
                progress(i, len(keys), status='Download in progress')
                print("Starting download of file {0}".format(k))
                cos.download_file(bucketName, k, os.path.join(dir, k))
                print("{0} donwloaded".format(k))
                i += 1
        else:
            for k in tqdm(keys, desc="Download in progress"):
                cos.download_file(bucketName, k, os.path.join(dir, k))
                i += 1
            
        print('* All files downloaded.')
    except KeyboardInterrupt:
        print('Interrupted!')
        try:
            os.system.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":

    env_path = 'script/.env'

    prefix = '22062021'
    
    download_path = 'script/descargas/' +  prefix

    progress_show = 'resume' # resume or full

    getEnv(env_path)
    cos = configInstance()
    buckets = getBuckets(cos)
    keys = getObjectsNames(cos, buckets[0], prefix)
    downloadFiles(cos, buckets[0], keys, download_path, progress_show)

