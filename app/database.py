from motor.motor_asyncio import AsyncIOMotorClient

# Replace with your actual MongoDB connection string
MONGO_DETAILS = "mongodb://localhost:27017"

# Create an async MongoDB client
client = AsyncIOMotorClient(MONGO_DETAILS)

# Select your database
database = client.image_processing_db

# Define collections
jobs_collection = database.get_collection("jobs")
images_collection = database.get_collection("images")
