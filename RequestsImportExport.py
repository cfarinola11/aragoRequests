import requests
import json
import datetime
import urllib3


print("Import or Export HIRO Requests.")
print("---------------------------------------------------------------------")

#disables insecure warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#today's date
today = datetime.date.today()
today = today.strftime('%m.%d.%Y')

def findEnv():
   findToken = input("Do you have a token? (y) (n)")
   type(findToken)
   findToken = findToken.lower()
   if findToken == "y":
        parsedToken = input("Please enter the token.")
        findGraph = input("What is the IP of your Graph node?")
        type(findGraph)
        findStyle(findGraph,parsedToken)
        return
   findWS02 = input("What is the IP of your WSO2 node?")
   type(findWS02)
   findGraph = input("What is the IP of your Graph node?")
   type(findGraph)
   findKey = input("What is the client_key for the account you will be using to upload?")
   type(findKey)
   findSecret = input("What is the client_secret for the account you will be using to upload?")
   type(findSecret)
   iamurl = "https://{0}:9443/oauth2/token".format(findWS02)
   data = {}
   data["grant_type"] = "client_credentials"
   data["scope"] = "batchjob"
   data["client_id"] = findKey
   data["client_secret"] = findSecret
   headers = {'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}
   token = requests.post(iamurl, params=data, headers=headers, verify=False)
   parsedToken = json.loads(token.text)
   parsedToken = parsedToken['access_token']
   print("Your token is: " + parsedToken)
   findStyle(findGraph,parsedToken)
   return

def importRequests(graph, parsedToken):
    print("You chose to import requests.")
    findJSON = input("Where are the requests stored? ie. /tmp/RequestsBackup.json")
    type(findJSON)
    readJSON = open(findJSON).read()
    readJSON = json.loads(readJSON)
    headers = {'Content-Type': 'application/json', '_TOKEN': parsedToken}
    graphurl = "https://{0}:8443/new/ogit%2FTask".format(graph)
    myCounter = 0
    for item in readJSON["items"]:
        myCounter += 1
        upload = requests.post(graphurl, data=json.dumps(item), headers=headers, verify=False)
        print(upload.text)
        if "error" in upload.text:
            myCounter -= 1
    print("Upload finished! " + str(myCounter) + " requests imported.")
    return

def exportRequests(graph, parsedToken):
    print("You chose to export requests.")
    headers = {'Content-Type': 'application/json', '_TOKEN': parsedToken}
    graphurl = "https://{0}:8443/query/vertices?query=%2B(ogit%5C%2F_type%3A%20ogit%5C%2FTask)%20%2B(ogit%5C%2Fstatus%3A%20TEMPLATE)".format(graph)
    export = requests.get(graphurl, headers=headers, verify=False)
    print(export.text)
    while True:
        path = input("Where would you like to store the file? ie. /tmp")
        print("Storing requests to " + path + "/RequestsBackup."+ today +".json")
        try:
            file = open(path + "/RequestsBackup."+ today +".json", "w")
            file.write(export.text)
            file.close()
        except FileNotFoundError:
            print("Invalid path. Try again.")
        else:
            break
    return

def checkInput(str, graph, parsedToken):
    if str == "i" or str == "import":
        importRequests(graph, parsedToken)
    elif str == "e" or str == "export":
        exportRequests(graph, parsedToken)
    return

def findStyle(graph,parsedToken):
    style = input("Will you be importing or exporting existing requests? (i)mport (e)xport")
    type(style)
    style = style.lower()
    print(style)
    if style == "i" or style == "import" or style == "e" or style == "export":
        checkInput(style,graph,parsedToken)
    else:
        print(r'You must enter either "import" or "export".')
        findStyle()
    return

findEnv()
