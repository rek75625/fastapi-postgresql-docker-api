from fastapi import FastAPI
import json

app = FastAPI()

# Helper Function
def loadData():
    with open("students.json","r") as file:
        return json.load(file)
    
@app.get('/jsonfile')
def students():
    return loadData()