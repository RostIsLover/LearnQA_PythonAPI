import json

import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
success = '{"success": "!"}'

def getReq(par):
    response = requests.get(url, params=par)
    if ("success" in response.text and par["method"] != "GET") or (
            "success" not in response.text and par["method"] == "GET"):
        print("Метод работает неверно!")
        print("Тип запроса: GET")
        print(f"Параметр: '{par}'")
        print(response.text)
        print("\n")


def postReq(par):
    response = requests.post(url, data=par)
    if ("success" in response.text and par["method"] != "POST") or (
            "success" not in response.text and par["method"] == "POST"):
        print("Метод работает неверно!")
        print("Тип запроса: POST")
        print(f"Параметр: '{par}'")
        print(response.text)
        print("\n")


def putReq(par):
    response = requests.put(url, data=par)
    if ("success" in response.text and par["method"] != "PUT") or (
    "success" not in response.text and par["method"] == "PUT"):
        print("Метод работает неверно!")
        print("Тип запроса: PUT")
        print(f"Параметр: '{par}'")
        print(response.text)
        print("\n")

def deleteReq(par):
    response = requests.delete(url, data=par)
    if ("success" in response.text and par["method"] != "DELETE") or (
            "success" not in response.text and par["method"] == "DELETE"):
        print("Метод работает неверно!")
        print("Тип запроса: DELETE")
        print(f"Параметр: '{par}'")
        print(response.text)
        print("\n")


funDict = {
    "GET": getReq,
    "POST": postReq,
    "PUT": putReq,
    "DELETE": deleteReq,
}


paramsDict = {
    "paramGET": {"method": "GET"},
    "paramPOST": {"method": "POST"},
    "paramPUT": {"method": "PUT"},
    "paramDELETE": {"method": "DELETE"},
    "paramHEAD": {"method": "HEAD"},
    "paramPATCH": {"method": "PATCH"},
}

# 1
responsePOST = requests.post(url)
print("#1 responsePOST:")
print(responsePOST.status_code)
print(f"Если отправить запрос без параметра method, то будет выводиться сообщение: '{responsePOST.text}'")
print("\n")

# 2
responseHEAD = requests.head(url, data=paramsDict["paramHEAD"])
print("#2 responseHEAD:")
print(responseHEAD.status_code)
print(f"Если отправить запрос не из списка, то будет получен код ответа: '{responseHEAD.status_code}' с пустым сообщением")
print("\n")

# 3
responseGET = requests.get(url, params=paramsDict["paramGET"])
print("#3 responseGET:")
print(responseGET.status_code)
print(f"Если запрос составлен верно, то будет выводиться код ответа '{responseGET.status_code}' и сообщение '{responseGET.text}'")
print("\n")

# 4
for fun in funDict:
    for param in paramsDict:
        funDict[fun](paramsDict[param])








