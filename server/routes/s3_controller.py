from fastapi import APIRouter
from services import duckDbService
from fastapi import Response
from fastapi.responses import JSONResponse
import services.s3IndexService as s3Service

router = APIRouter()




############################################################################################################
# S3
############################################################################################################

@router.get("/s3Search")
def s3Search(bucket: str, fileName: str):
    print("Searching for '" + fileName + "' in bucket '" + bucket + "'")
    if (bucket is None or fileName is None):
        response = {"status": "error", "message": "bucket and fileName are required"}
        return JSONResponse(content=response, status_code=400)
    
    results = []
    if (len(fileName) >= 3):
        results = s3Service.s3Search(bucket, fileName)

    # If  results array is greter than 100 items, return first 10
    if (len(results) > 10):
        results = results[:10]
    
    return {"results": results}