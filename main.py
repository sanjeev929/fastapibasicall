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

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: models.User):
    # Check if the user exists
    existing_user = await collection.find_one({"id": user_id})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User1 not found")

    # Update the user information
    result = await collection.update_one({"id": user_id}, {"$set": user.dict()})
    if not result.modified_count:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Check if the user exists
    existing_user = await collection.find_one({"id": user_id})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    result = await collection.delete_one({"id": user_id})
    if not result.deleted_count:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8001)