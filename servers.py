import csv
import ipaddress
import paramiko
import time as time
import signal


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
is_connected_to_server = False
number_of_servers = 0


def handler(signum, frame):
    client.close()

def is_valid_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_login(server_ip, username, password):

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(3)  # Set the parameter to the amount of seconds you want to wait

    try:
        client.connect(server_ip, username=username, password=password)

        for i in range(0, 3):
            time.sleep(1)

        client.close()
        return True
    except:
        return False

def get_servers_data():
    global number_of_servers
    servers = []
    with open('servers.txt') as csv_file:
        print(f'>>Getting server list from {csv_file.name}')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            current_server = []
            if line_count > 0:
                print(f' \t{row[0]}, {row[1]}, {row[2]}')
                current_server.append(row[0])
                current_server.append(row[1])
                current_server.append(row[2])
                current_server.append(row[3])
                current_server.append(row[4])
                servers.append(current_server)
            line_count += 1
        print(f'\t-Processed {line_count - 1} servers.')
        number_of_servers = line_count - 1
    return servers

def add_server(server_ip, username, password, sender , time):
    global number_of_servers
    number_of_servers += 1
    server = [server_ip, username, password, sender, time]
    with open('servers.txt', 'a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(server)


def del_server(server_number):
    global number_of_servers
    number_of_servers -= 1
    counter = 0
    with open("servers.txt", "r") as f:
        lines = f.readlines()
    with open("servers.txt", "w") as f:
        for line in lines:
            if counter != int(server_number):
                f.write(line)
            counter += 1
