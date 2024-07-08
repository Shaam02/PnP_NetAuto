from netmiko import ConnectHandler
from datetime import datetime 
import getpass


# Prompt for credentials
# this is a change from the master branch
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
enable_password = getpass.getpass("Enter your enable password: ")

# Define your device
device = {
    'device_type': 'cisco_ios',
    'username': username,
    'password': password,
    'secret': enable_password,
}

# Get the start time
print ("") 
print ("") 
print ("------------Time At Start Of Script------------")
start_time = datetime.now()
print (start_time)
print ("") 

# Read the IP addresses from hosts.txt
with open('hosts.txt', 'r') as file:
    hosts = file.read().splitlines()

# Loop over each host
for pnp_host_ip in hosts:
    device['ip'] = pnp_host_ip  # Set the IP address for this iteration

    # Establish the connection
    shaam_connection = ConnectHandler(**device)
    output1 = shaam_connection.find_prompt()
    print (output1)
    shaam_connection.enable()
    output2 = shaam_connection.find_prompt()
    print (output2)

    print ("") 
    
    print ("------------Config Before------------")    
    # Execute the command
    output3 = shaam_connection.send_command('show inter status')
    print (output3)
    
    # Configure the interface
    config_commands = [
        'interface GigabitEthernet1/0/27',
        'switchport mode access',
        'switchport access vlan 100',
        'interface GigabitEthernet1/0/28',
        'switchport mode access',
        'switchport access vlan 200',
    ]
    shaam_connection.send_config_set(config_commands)   
    
    print ("")    
    print ("------------Config------------")
    print (config_commands)
    print ("------------------------------")
    print ("")       
    
    
    print ("------------Config After------------") 
    
    # Execute the command
    output4 = shaam_connection.send_command('show inter status')
    print (output4)
    print ("") 
    print ("") 
    output5 = shaam_connection.send_command('show tcp brief')
    print (output5)
    print ("") 
    print ("") 

print ("------------Time At End Of Script------------")
end_time = datetime.now()
print (end_time)  

print ("------------Time_It_Took_To_Run_Script H:MM:SS:MS------------")
total_time = end_time - start_time  
print (total_time) 

    
    # Write the output to a file
with open(f'{pnp_host_ip}_output.txt', 'w') as file:
        file.write(f'Start_Time: {start_time}\n\n')
        file.write(f'Device Name: {output2}\n\n')
        file.write(f'Device IP: {pnp_host_ip}\n\n')
        file.write('Config_Before\n\n')
        file.write(f'Device Name: {output3}\n\n')
        file.write(f'Config_Commands: {config_commands}\n\n')
        file.write('Config_After\n\n')
        file.write(f'Device Name: {output4}\n\n')
        file.write(f'Device Name: {output5}\n\n')
        file.write(f'End_Time: {end_time}\n\n')
        file.write(f'Total_Time: {total_time}\n\n')
        


    # Close the connection
shaam_connection.disconnect()


