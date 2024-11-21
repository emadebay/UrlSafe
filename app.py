from fastapi import FastAPI, Request, HTTPException, Depends, Header
from pymongo import MongoClient
from pydantic import BaseModel
from functools import wraps
from lru import LRUCache  # Import your LRUCache class
# from safeNet import predict_url_label

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection setup
mongo_url = "mongodb://mongo:ffWdtbFwpvsUjRryieJCxHCIOOuOHNOk@autorack.proxy.rlwy.net:34033"
client = MongoClient(mongo_url)
db = client["url_mappings"]
collection = db["urls"]

# Hidden admin key for authorization
ADMIN_KEY = "d74hKz9w8Bn9A6l2QxZTgP4mWs7fG5yDkU0H1jvF9RgJ6zX9u2s5Yl8NwEjQkzM3T0vFsE"

# Initialize the LRU Cache with capacity 100
cache = LRUCache(100)

# Pydantic model for URL data
class URLData(BaseModel):
    url: str
    type: str

# Decorator for admin authorization
def require_admin(authorization: str = Header(...)):
    if authorization != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return True

@app.get("/predict_url")
async def predict_url(url: str):
    # Check cache first
    cached_data = cache.get(url)
    if cached_data:
        # Return the cached label
        return {"url": url, "label": cached_data}
    
    # If not in cache, query the database
    url_data = collection.find_one({"url": url})
    if url_data:
        # Return the label from the database
        return {"url": url_data["url"], "label": url_data["type"]}
    
    # If not found in cache or database, predict the label
    # predicted_label = predict_url_label(url)
    predicted_label = "benign"
    # Save the predicted label to the database and cache
    collection.insert_one({"url": url, "type": predicted_label})
    cache.put(url, predicted_label)
    
    return {"url": url, "label": predicted_label}


# Add new URL
@app.post("/add_url")
async def add_url(url_data: URLData, is_admin: bool = Depends(require_admin)):
    # Insert the new URL into the database
    collection.insert_one(url_data.dict())

    # Update the cache
    cache.put(url_data.url, url_data.type)
    return {"message": "URL added successfully"}

# Update URL
@app.put("/update_url")
async def update_url(url_data: URLData, is_admin: bool = Depends(require_admin)):
    # Update the URL in the database
    result = collection.update_one({"url": url_data.url}, {"$set": {"type": url_data.type}})
    if result.modified_count > 0:
        # Update the cache
        cache.put(url_data.url, url_data.type)
        return {"message": "URL updated successfully"}
    
    raise HTTPException(status_code=404, detail="URL not found")

@app.delete("/delete_url")
async def delete_url(url_data: URLData, is_admin: bool = Depends(require_admin)):
    # Delete the URL from the database
    result = collection.delete_one({"url": url_data.url})
    
    if result.deleted_count > 0:
        # Remove the URL from the cache if it exists
        cache_value = cache.get(url_data.url)
        if cache_value != -1:
            cache.remove(cache.cache[url_data.url])  # Remove node from the cache
        return {"message": "URL deleted successfully"}
    
    raise HTTPException(status_code=404, detail="URL not found")

# To run the app, use the command:
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
