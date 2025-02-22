import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

# Load .env from either current working directory or script directory
cwd_env = os.path.join(os.getcwd(), ".env")
script_env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(cwd_env):
    load_dotenv(dotenv_path=cwd_env)
elif os.path.exists(script_env):
    load_dotenv(dotenv_path=script_env)
else:
    print("Warning: No .env file found")

base_url="https://monitor.eg4electronics.com/WManage"

def login_eg4(account: str, password: str):
    session = requests.Session()
    login_url = f"{base_url}/web/login"
    
    # Step 1: Initialize session and get JSESSIONID
    response = session.get(base_url, allow_redirects=False)
    if 'Set-Cookie' in response.headers:
        print("JSESSIONID Acquired")
    
    # Step 2: Follow redirects to login page
    response = session.get(response.headers.get('Location', ''), allow_redirects=False)
    if response.status_code == 302:
        response = session.get(response.headers.get('Location', ''), allow_redirects=False)
    
    # Step 3: Perform login
    login_payload = {"account": account, "password": password}
    response = session.post(login_url, data=login_payload, allow_redirects=False)
    if response.status_code == 302:
        print("Login Successful")
        session.get(response.headers.get('Location', ''))
    else:
        print("Login Failed")
        return None
    
    return session

def get_inverter_data(session, serial_num):
    inverter_info_url = f"{base_url}/api/inverter/getInverterRuntime"
    payload = {"serialNum": serial_num}
    
    response = session.post(inverter_info_url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get inverter info")
        return None

def get_inverter_energy_info(session, serial_num):
    inverter_info_url = f"{base_url}/api/inverter/getInverterEnergyInfo"
    payload = {"serialNum": serial_num}
    
    response = session.post(inverter_info_url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get inverter energy info")
        return None

def get_battery_data(session, serial_num):
    battery_info_url = f"{base_url}/api/battery/getBatteryInfo"
    payload = {"serialNum": serial_num}
    
    response = session.post(battery_info_url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get battery info")
        return None

def print_summary(inverter_data, inverter_energy_data, battery_data):
    if inverter_data:
        print("\nInverter Summary:")
        print(f"\tStatus: {inverter_data.get('statusText', 'Unknown')}")
        print(f"\tBattery Type: {inverter_data.get('batteryType', 'Unknown')}")
        print(f"\tSOC: {inverter_data.get('soc', 'N/A')}%")
        print(f"\tBattery Power: {inverter_data.get('batPower', 'N/A')}W")
        print(f"\tPower to User: {inverter_data.get('pToUser', 'N/A')}W")
        print(f"\tPower to Grid: {inverter_data.get('pToGrid', 'N/A')}W")
    
    if inverter_energy_data:
        print("\nInverter Energy Summary:")
        print(f"\tToday's Yield: {inverter_energy_data.get('todayYieldingText', 'N/A')} kWh")
        print(f"\tTotal Yield: {inverter_energy_data.get('totalYieldingText', 'N/A')} kWh")
        print(f"\tToday's Charging: {inverter_energy_data.get('todayChargingText', 'N/A')} kWh")
        print(f"\tTotal Charging: {inverter_energy_data.get('totalChargingText', 'N/A')} kWh")
        print(f"\tToday's Discharging: {inverter_energy_data.get('todayDischargingText', 'N/A')} kWh")
        print(f"\tTotal Discharging: {inverter_energy_data.get('totalDischargingText', 'N/A')} kWh")
    
    if battery_data:
        print("\nBattery Summary:")
        print(f"\tTotal Batteries: {battery_data.get('totalNumber', 'N/A')}")
        print(f"\tCurrent Type: {battery_data.get('currentType', 'N/A')}")
        print(f"\tTotal Voltage: {battery_data.get('totalVoltageText', 'N/A')}V")
        for i, battery in enumerate(battery_data.get('batteryArray', []), start=1):
            print(f"\tBattery {i}:")
            print(f"\t\tSerial: {battery.get('batterySn', 'Unknown')}")
            print(f"\t\tSOC: {battery.get('soc', 'N/A')}%")
            print(f"\t\tVoltage: {battery.get('totalVoltage', 'N/A') / 100}V")
            print(f"\t\tCurrent: {battery.get('current', 'N/A') / 10}A")
            print(f"\t\tSOH: {battery.get('soh', 'N/A')}%")
            print(f"\t\tCycle Count: {battery.get('cycleCnt', 'N/A')}")

account = os.getenv("EG4_ACCOUNT", "your_login_name")
password = os.getenv("EG4_PASSWORD", "your_password")
serial_num = os.getenv("EG4_SERIAL_NUM", "your_inverter_serial")

print(f"Account: {account}, Password: {'***' if password else 'MISSING'}, Serial: {serial_num}")

session = login_eg4(account, password)
if session:
    inverter_data = get_inverter_data(session, serial_num)
    inverter_energy_data = get_inverter_energy_info(session, serial_num)
    battery_data = get_battery_data(session, serial_num)
    
    print_summary(inverter_data, inverter_energy_data, battery_data)
