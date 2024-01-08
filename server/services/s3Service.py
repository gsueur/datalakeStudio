import boto3
import json
import time

index = None
indexBuildingTime = 0
previousBucket = None

def buildIndex(bucket_name):
    print ("Building index...")
    global index
    s3 = boto3.client("s3")
    indice = []

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get("Contents", []):
            indice.append("s3://" + bucket_name + "/" + obj["Key"])

    return indice

############################################################################################################

def s3Search(bucket, fileName):
    global index
    global indexBuildingTime
    global previousBucket

    if (bucket!=previousBucket):
        index = None
        previousBucket = bucket
    
    if (index == None) or time.time() - indexBuildingTime > 600:
        index = buildIndex(bucket)
        indexBuildingTime = time.time()

    results = []

    for file in index:
        if fileName in file:
            results.append(file)

    return results

############################################################################################################
def getContent(bucket, path):
    s3 = boto3.client("s3")
    results = []

    
    respuesta = s3.list_objects_v2(Bucket=bucket, Prefix=path, Delimiter='/')

    for objeto in respuesta.get('Contents', []):
        print("Obj:" + objeto['Key'])
        results.append(objeto['Key'])

    for prefijo in respuesta.get('CommonPrefixes', []):
        print("Pref:" + prefijo['Prefix'])
        results.append(prefijo['Prefix'])

    return results