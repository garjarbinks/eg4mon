# EG4 Inverter Monitor

## Overview
This script logs into the EG4 inverter monitoring system and retrieves real-time inverter and battery data using the web API-like responses.

## Features
- Authenticates with the EG4 monitoring system.
- Retrieves inverter runtime and energy information.
- Fetches battery status, including SOC, voltage, current, and cycle count.
- Displays a summary of inverter and battery data.

## Requirements
- Python 3.7+
- Internet connection
- An EG4 account with credentials

## Installation
### **1. Clone the Repository**
```sh
git clone https://github.com/garjarbinks/eg4mon.git
cd eg4mon
```

### **2. Set Up Virtual Environment (Optional but Recommended)**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Configure Environment Variables**
Create a `.env` file in the root directory:
```sh
touch .env
```
Edit `.env` and add your EG4 credentials:
```
EG4_ACCOUNT=your_username
EG4_PASSWORD=your_password
EG4_SERIAL_NUM=your_serial_number
```

## Usage
Run the script to retrieve and display inverter and battery data:
```sh
python src/eg4mon.py
```

## Expected Output
The script will display a summary similar to:
```
Inverter Summary:
Status: Normal
Battery Type: LITHIUM
SOC: 94%
Battery Power: -593W
Power to User: 0W
Power to Grid: 0W

Inverter Energy Summary:
Today's Yield: 9.9 kWh
Total Yield: 268.1 kWh
Today's Charging: 25.1 kWh
Total Charging: 748.5 kWh

Battery Summary:
Total Batteries: 2
Current Type: Discharge
Total Voltage: 53V
Battery 1:
  Serial: Battery_ID_01
  SOC: 94%
  Voltage: 53.06V
  Current: -6.0A
  SOH: 100%
  Cycle Count: 11
Battery 2:
  Serial: Battery_ID_02
  SOC: 94%
  Voltage: 53.07V
  Current: -5.7A
  SOH: 100%
  Cycle Count: 10
```

## Troubleshooting
### **Login Fails**
- Ensure your `.env` file is correctly set up.
- Try running:
  ```sh
  export $(grep -v '^#' .env | xargs) && python src/eg4mon.py
  ```
- Check for any network restrictions blocking access to `monitor.eg4electronics.com`.

### **No Data Returned**
- Verify that the serial number in `.env` is correct.
- Check if your inverter is online.

## Contributing
Feel free to submit issues or pull requests to improve the script.

## License
This project is licensed under the MIT License.

