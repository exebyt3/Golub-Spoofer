import os
import time
import requests
import zipfile
import random
import ctypes
import subprocess
import shutil
import winreg
import re

def activate_windows():
    print("Activating Windows..")

    activate = [
        "slmgr.vbs /upk",
        "slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "slmgr /skms kms8.msguides.com",
        "slmgr /ato"    
    ]

    for cmd in activate:
        os.system(cmd)

    print("Done!")
    time.sleep(5)
    
def reset_network_vpn_cache():
    network = [
        "netsh winsock reset",
        "netsh winsock reset catalog",
        "netsh int ip reset",
        "netsh advfirewall reset",
        "netsh int reset all",
        "netsh int ipv4 reset",
        "netsh int ipv6 reset",
        "ipconfig /release",
        "ipconfig /renew"
    ]

    for cmd in network:
        os.system(cmd)

    os.system('cls')

    print(f"All commands have been executed ...")
    time.sleep(5)

def spoof_hdd():
    def generate_random_numbers():
        return f"{random.randint(0, 15):X}{random.randint(0, 15):X}{random.randint(0, 15):X}{random.randint(0, 15):X}-{random.randint(0, 15):X}{random.randint(0, 15):X}{random.randint(0, 15):X}{random.randint(0, 15):X}"

    url = "https://download.sysinternals.com/files/VolumeId.zip"
    destination_folder = "C:/Windows"
    zip_filename = "VolumeId.zip"

    # Delete the zip file from the script's working directory
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    if not os.path.exists(os.path.join(destination_folder, zip_filename)):
        response = requests.get(url)
        if response.status_code == 200:
            with open(zip_filename, "wb") as file:
                file.write(response.content)

            # Use shutil.copy to move the file to the destination folder
            shutil.copy(zip_filename, os.path.join(destination_folder, zip_filename))

            with zipfile.ZipFile(os.path.join(destination_folder, zip_filename), "r") as zip_ref:
                zip_ref.extractall(destination_folder)

            available_drives = []
            for drive in range(65, 91):
                drive_letter = chr(drive) + ":"
                if os.path.exists(drive_letter):
                    available_drives.append(drive_letter)

            print("Available hardware:")
            for i, drive in enumerate(available_drives, 1):
                print(f"{i}. {drive}")

            while True:
                choice = input("Enter a number of hardware for which you want to change a Serial number: ")
                try:
                    choice_index = int(choice) - 1
                    selected_drive = available_drives[choice_index]
                    break
                except (ValueError, IndexError):
                    print("Invalid input. Try again.")

            generated_numbers = generate_random_numbers()
            new_volume_id = f"volumeid {selected_drive} {generated_numbers}"

            os.system(new_volume_id)
        else:
            print("Error downloading archive")
    else:
        print("Archive has already been downloaded.\n")
        available_drives = []
        for drive in range(65, 91):
            drive_letter = chr(drive) + ":"
            if os.path.exists(drive_letter):
                available_drives.append(drive_letter)

        print("Available hardware:")
        for i, drive in enumerate(available_drives, 1):
            print(f"{i}. {drive}")

        while True:
            choice = input("Enter a number of hardware for which you want to change a Serial number: ")
            try:
                choice_index = int(choice) - 1
                selected_drive = available_drives[choice_index]
                break
            except (ValueError, IndexError):
                print("Invalid input. Try again.")

        generated_numbers = generate_random_numbers()
        new_volume_id = f"volumeid {selected_drive} {generated_numbers}"

        os.system(new_volume_id)

    os.system('cls')

    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print("[1] Cleaning up..")

    if os.path.exists(os.path.join(destination_folder, zip_filename)):
        os.remove(os.path.join(destination_folder, zip_filename))
        print("[2] Cleaning up..")

    print(f"\nSpoof Hardware was successfully completed!\nDisk {selected_drive} now with {generated_numbers}")
    ctypes.windll.user32.MessageBoxW(0, f"Disk {selected_drive} now with {generated_numbers}", "Hardware Spoof", 32)
    print(f"Restart your PC!")

    # Delete the extracted directory and files
    extracted_dir = os.path.join(destination_folder, "VolumeId")
    if os.path.exists(extracted_dir):
        shutil.rmtree(extracted_dir)

    files_to_delete = [
        os.path.join(destination_folder, "Volumeid.exe"),
        os.path.join(destination_folder, "Volumeid64.exe")
    ]

    for file_to_delete in files_to_delete:
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)

    time.sleep(3)

def spoof_macid():
    macshift_path = "C:/Windows/macshift.exe"

    url = "https://s3.aeza.cloud/potent-sheet/macshift.exe"
    response = requests.get(url)

    if response.status_code == 200:
        with open(macshift_path, "wb") as file:
            file.write(response.content)
        print("File macshift.exe downloaded and copied to C:/Windows.")
    else:
        print(f"Error {response.status_code}: Can't download the file.")

    netsh_command = "netsh interface show interface"
    print(f"Getting interfaces...\n")
    output = subprocess.check_output(netsh_command, shell=True, text=True)

    lines = output.split("\n")
    for line in lines:
        if "Enabled" in line:
            interface_name = line.strip().split()[-1]
            if interface_name and not any(char in interface_name for char in ('/', '\\', '"', '|')):
                macshift_command = f"macshift \"{interface_name}\" -r"
                print(f"{macshift_command}")
                subprocess.run(macshift_command, shell=True, cwd="C:/Windows")
        
    if os.path.exists(macshift_path):
        os.remove(macshift_path)
        time.sleep(3)
        os.system('cls')
        print("[1] Cleaning up..")

    print("Done!")

    time.sleep(3)

def spoof_winname(win_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "ComputerName", 0, winreg.REG_SZ, win_name)
        winreg.CloseKey(key)

        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\services\\Tcpip\\Parameters", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "Hostname", 0, winreg.REG_SZ, win_name)
        winreg.SetValueEx(key, "NV Hostname", 0, winreg.REG_SZ, win_name)
        winreg.CloseKey(key)

        print(f"Succesfully spoofed to {win_name}.\nRestart your PC!")
    except Exception as e:
        print(f"Error when edit pc name: {e}")

    time.sleep(5)
    
def spoof_pcname(pc_name):
    com = f'wmic ComputerSystem where "name=\'%ComputerName%\'" call rename name="{pc_name}"'

    try:
        result = subprocess.run(com, shell=True, capture_output=True, text=True)
        os.system('cls')
        if result.returncode == 0:
            print("Done!\nRestart your PC!")
        else:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)

def spoof_uuidserial():
    def change_id(original_id):
        new_id = ''.join(random.choice("0123456789ABCDEF") for _ in range(len(original_id)))
        return new_id

    try:
        print("Downloading assets...")
        zip_url = "https://s3.aeza.cloud/potent-sheet/AMIDEWIN.zip"
        zip_filename = "AMIDEWIN.zip"
        response = requests.get(zip_url)

        if response.status_code == 200:
            with open(zip_filename, "wb") as file:
                file.write(response.content)

            with zipfile.ZipFile(zip_filename, "r") as zip_ref:
                zip_ref.extractall(".")

            print("Assets downloaded and extracted.")

            print("Getting original UUID...")
            output = subprocess.check_output("AMIDEWINx64.EXE /SU", shell=True, universal_newlines=True)

            uuid_match = re.search(r"System UUID\s+R\s+Done\s+\"([\w\d]+)h\"", output)

            if uuid_match:
                original_uuid = uuid_match.group(1)
                new_uuid = change_id(original_uuid)

                print(f"Original UUID: {original_uuid}")
                print(f"Edited UUID: {new_uuid}\n")

                # Spoof UUID
                print("Spoofing UUID...\n")
                subprocess.run(f"AMIDEWINx64.EXE /SU {new_uuid}")

                print("Getting original serial...")
                output = subprocess.check_output("AMIDEWINx64.EXE /BS", shell=True, universal_newlines=True)

                serial_match = re.search(r"Baseboard Serial number\s+R\s+Done\s+\"([\w\d]+)\"", output)

                if serial_match:
                    original_serial = serial_match.group(1)
                    new_serial = change_id(original_serial)

                    print(f"Original serial: {original_serial}")
                    print(f"Edited serial: {new_serial}\n")

                    print("Spoofing serial...")
                    subprocess.run(f"AMIDEWINx64.EXE /BS {new_serial}")

                    print("\nDone!")

                else:
                    print("Serial not found.")
            else:
                print("UUID not found.")
        else:
            print("Error downloading archive")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(zip_filename):
            os.remove(zip_filename)

        files_to_delete = [
            "AMIDEWIN.exe",
            "AMIDEWINx64.exe",
            "AMIFLDRV32.sys",
            "AMIFLDRV64.sys"
        ]

        for file_to_delete in files_to_delete:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)
    time.sleep(5)

def title():
    print('''
   ______      __      __       _____                   ____         
  / ____/___  / /_  __/ /_     / ___/____  ____  ____  / __/__  _____
 / / __/ __ \/ / / / / __ \    \__ \/ __ \/ __ \/ __ \/ /_/ _ \/ ___/
/ /_/ / /_/ / / /_/ / /_/ /   ___/ / /_/ / /_/ / /_/ / __/  __/ /    
\____/\____/_/\__,_/_.___/   /____/ .___/\____/\____/_/  \___/_/     
                                 /_/                                 
''')

def main():
    while True:
        os.system('cls')
        
        title()
        print("1) Activation Windows / Product ID")
        print("2) Reset network / VPN cache")
        print("3) Volume ID *Restart PC")
        print("4) Mac ID")
        print("5) PC name *Restart PC")
        print("6) Windows name *Restart PC")
        print("7) UUID and Serial")
        print("0) Exit")

        choice = input("\n[+]Please select one options: ")

        if choice == "1":
            os.system('cls')
            activate_windows()
        elif choice == "2":
            os.system('cls')
            reset_network_vpn_cache()
        elif choice == "3":
            os.system('cls')
            spoof_hdd()
        elif choice == "4":
            os.system('cls')
            spoof_macid()
        elif choice == "5":
            os.system('cls')
            win_name = input("Enter new windows name: ")
            spoof_winname(win_name)
        elif choice == "6":
            os.system('cls')
            pc_name = input("Enter new pc name: ")
            spoof_pcname(pc_name)
        elif choice == "7":
            os.system('cls')
            spoof_uuidserial()
        elif choice == "0":
            print("Exiting the program..")

            time.sleep(0.4)
            break
        else:
            print("Invalid input. Please choose an option from the menu.")
            time.sleep(0.3)

if __name__ == "__main__":
    main()
