#put and delete --HTTP Verbs
## working with api's API's--JSON


from flask import Flask,jsonify,request

#initalization
app=Flask(__name__)

#initalize data in my to do list
items=[
    {"id":1, "name":"Item1", "description":"This is Item 1"},
    {"id":2, "name":"item2", "descirption":"This is item 2"}
]

@app.route('/')
def home():
    return "Welcome To Sample Tp Do List App"


#get: retrive all the items from ths item list
@app.route('/items',methods=['GET'])
def get_times():
    return jsonify(items)



#get :retrive specific items by id->variable rule
@app.route('/items/<int:item_id>',methods=['GET'])
def get_item(item_id):
    item=next((item for item in items if item["id"]==item_id),None)
    if item is None:
        return jsonify({"error":"item not found"})
    return jsonify(item)


#post :create n new task-->createing a task
@app.route('/items',methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        return jsonify({"error"+"items not found"}),400
    new_item={
        "id":items[-1]["id"]+1 if items else 1,
        "name":request.json['name'],
        "descirption":request.json.get("description","")
    }

    items.append(new_item)
    return jsonify(new_item),201


#put: updates an existing items-->updating task
@app.route('/items/<int:item_id>',methods=['PUT'])
def update_item(item_id):
    item=next((item for item in items if item["id"]==item_id))
    if item is None:
        return jsonify({"error": "item not found"})
    item['name']=request.json.get('name',item['name'])
    item['descirption']=request.json.get('description',item.get('descirption',""))
    return jsonify(item)


#Delete: delete the item
@app.route('/items/<int:item_id>',methods=['DELETE'])
def delete_item(item_id):
    global items
    items=[item for item in items if item["id"]!=item_id]
    return jsonify({"result":"Item deleted"}),200
     


if __name__ == "__main__":
    app.run(debug=True)
