import requests
import pickle
import time
from selenium import webdriver

cookie_file = "session_cookies.pkl"
msisdn_file = "msisdn.txt"

try:
    with open(cookie_file, "rb") as file:
        stored_cookie = pickle.load(file)
except FileNotFoundError:
    stored_cookie = None
    
try:
    with open(msisdn_file, "r") as file:
        msisdn = file.read()
except FileNotFoundError:
    msisdn = None

balance_url = "https://dlg.dialog.lk/selfcare-proxy?r=usage/get"
response = requests.post(balance_url, cookies=stored_cookie, headers={"Msisdn": msisdn})

if response.status_code == 200:
    balance_data = response.json()
    # print("Your remaining data balance is:", balance_data["data"]["usage_types"][0]["usages"][0]["remaining_amount"])
    print("Your remaining data balance is:", balance_data["data"])
else:
    driver = webdriver.Chrome()
    homepage_url = "https://dlg.dialog.lk/sso-login?language=en&destination=L215ZGlhbG9nLXdlYj9sYW5ndWFnZT1lbg=="
    
    driver.get(homepage_url)
    
    while True:
        time.sleep(1)
        current_url = driver.current_url
        if current_url == "https://dlg.dialog.lk/mydialog-web/account-summary?language=en":
            break

    cookies = driver.get_cookies()
    
    new_cookie = {cookie['name']: cookie['value'] for cookie in cookies}
 
    driver.quit()

    # Save the session cookies to the file
    with open(cookie_file, "wb") as file:
        pickle.dump(new_cookie, file)

    stored_cookie = new_cookie

    response = requests.post(balance_url, cookies=stored_cookie, headers={"Msisdn": msisdn})

    if response.status_code != 200:
        print("Failed to retrieve data balance.")
        exit()

    balance_data = response.json()

    remaining_amount = balance_data["data"]["usage_types"][0]["usages"][0]["remaining_amount"]
    print("Your remaining data amount is:", remaining_amount)
