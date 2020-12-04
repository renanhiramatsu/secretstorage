import sqlite3
from hashlib import sha256

PASSWORD = "123$%^@"

connect = input("Type your password\n")

while connect != PASSWORD:
    connect = input("Type your password\n")
    if connect == "q":
        break


def createPassword(passKey, service, adminPassword):
    return sha256(adminPassword.encode('utf-8') + service.lower().encode('utf-8') + passKey.encode('utf-8')).hexdigest()[:10]


def getHexKey(adminPassword, service):
    return sha256(adminPassword.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()


conn = sqlite3.connect('passwordManager.db')


def getPassword(adminPassword, service):
    secretKey = getHexKey(adminPassword, service)
    cursor = conn.execute(
        "SELECT * FROM KEYS WHERE PASSKEY=" + '"' + secretKey + '"')

    passKey = ""
    for row in cursor:
        passKey = row[0]

    return createPassword(passKey, service, adminPassword)
