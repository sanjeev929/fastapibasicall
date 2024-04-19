from fastapi import FastAPI,HTTPException
import uvicorn
import models
from motor.motor_asyncio import AsyncIOMotorClient
app = FastAPI()

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["fatsapitest"]
collection = db["test"]


@app.get("/")
async def userget():
    return {"message":"yes"}

@app.get("/users/{userid}")
async def userpost(userid:int):
    result = await collection.find_one({"id":userid})
    print(result)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    result["_id"] = str(result["_id"])
    return result

@app.post("/users/")
async def userpost(user:models.User):
    user_dict=user.dict()
    print(user_dict)
    result = await collection.insert_one(user_dict)
    return {"message":"successfull"}

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8001)