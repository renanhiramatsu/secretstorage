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


def addPassword(service, adminPassword):
    secret_key = getHexKey(adminPassword, service)

    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' % (
        '"' + secret_key + '"')
    conn.execute(command)
    conn.commit()
    return createPassword(secret_key, service, adminPassword)


if connect == PASSWORD:
    try:
        conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")

    while True:
        print("\n" + "*"*15)
        print("Commands:")
        print("q = quit program")
        print("gp = get password")
        print("sp = store password")
        print("*"*15)
        input_ = input(":")

        if input_ == "q":
            break
        if input_ == "sp":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() +
                  " password created:\n" + addPassword(service, PASSWORD))
        if input_ == "gp":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() +
                  " password:\n"+getPassword(PASSWORD, service))
