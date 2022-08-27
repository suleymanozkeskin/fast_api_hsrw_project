
from fastapi import FastAPI , Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    
    
 

## how to create an end-point ? see below:

@app.get("/")
def home():
    return{"Data" :  "Test"}


@app.get("/about")
def about():
    return{"Data": "About"}


## we define an inventory

# inventory =  {
#     1: {                              ##         <-- item with id Number 1 
#         "name": "Milk",
#         "price": 0.99, 
#         "brand": "Gut&Günstig"
#     }
# }

inventory = {}


## PATH PARAMETHERS

@app.get("/get-item/{item_id}")  ## based on what this {item_id} is ,
    # we are gonna return something different from this end-point
 
def get_item(item_id: int = Path(None,description="The id of the item you'd like to view: ")): 
    ## here we tell fast-api to expect an integer for item_id 
    ## by doing so in case users give anything else than an integer, fastapi will raise an error message for us.
    ## Path function will allow us add more details to parameter                         
    return inventory[item_id]
    
# with the following end-point /get-item/1  , we will have  the following as response on the page:
# {"name":"Milk","price":0.99,"brand":"Gut&Günstig"} 


@app.get("/get_by_name")
def get_item(name: Optional[str] = None): # we are going to accept one query parameter which is "name" and its a string
    for item_id in inventory:
        if inventory[item_id].name == name: 
            return inventory[item_id]
        else:
            return {"data": "Not found"}

# http://127.0.0.1:8000/get_by_name?name=Milk 
# if we type the query above we will get data for "Milk" because it exists 
# but if we type something else instead of name?name=Milk , we will get the 
# "data not found" warning because the data does not exist.


@app.post("/create_item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists."}
    else:
        inventory[item_id] = item  ## or {"name": item.name , "brand": item.brand , "price": item.price}
        return inventory[item_id]
    

    
## how to update an item ? 

@app.put("/update_item/{item_id}") 
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        return{"Error": "Item ID does not exist."}
    
    if item.name != None:
        inventory[item_id].name = item.name  
    
    if item.price != None:
        inventory[item_id].price = item.price  
    
    if item.brand != None:
            inventory[item_id].brand = item.brand  
        
    return inventory[item_id]
    
  
## to be able to update only desired combinations of a class we will create the following class with Optinal tags

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None 
    brand: Optional[str] = None  
     