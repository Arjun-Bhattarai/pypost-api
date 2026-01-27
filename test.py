import requests
import json
url="https://jsonplaceholder.typicode.com/users"

print("search the user name ")
user=input(" ")
queryURL=url+f"?username={user}"
response=requests.get(queryURL)
userdata=json.loads(response.text)[0]

#print (response.text) 
name=userdata["name"]
email=userdata["email"]
phone=userdata["phone"]
print(f"{name}the data that you have provided cannot be reached")
print(f"email:{email}")
print(f"phone:{phone}")
