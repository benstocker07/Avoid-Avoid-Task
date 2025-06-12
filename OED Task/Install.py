import paramiko
import base64
import os
import subprocess
'''
with open('spwf.txt', 'r') as file:
    read = file.read().strip()

encoded_password = read
password = base64.b64decode(encoded_password.encode('utf-8')).decode('utf-8')'''

password = 'Boeing20201-'
hostname = 'benstocker07.ddns.net'
username = 'ben'

SSH_Client = paramiko.SSHClient()
SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

port = 22

files = [
    '/home/ben/ftp/OED Task.py',
    '/home/ben/ftp/spwf.txt',
    '/home/ben/ftp/OED Dependencies.bat',
    '/home/ben/ftp/task.ps1',
    '/home/ben/ftp/Stimuli'
]

def install():
    try:
        SSH_Client.connect(hostname=hostname,
                           port=port,
                           username=username,
                           password=password,
                           look_for_keys=False)

        sftp_client = SSH_Client.open_sftp()

        print(sftp_client.listdir('/home/ben/ftp/'))

        for file in files:
            if sftp_client.stat(file).st_mode & 0o40000: 
                local_dir = os.path.basename(file)
                os.makedirs(local_dir, exist_ok=True)  
                copy_directory(sftp_client, file, local_dir)
            else:
                local_file_path = os.path.basename(file)
                try:
                    sftp_client.get(file, local_file_path)
                    print(f"File: {file} migrated")
                except FileNotFoundError as e:
                    print(e)
                    print(f"File: {file} was not found on the SFTP server")

    finally:
        if 'sftp_client' in locals():
            sftp_client.close()
        SSH_Client.close()

def copy_directory(sftp_client, remote_dir, local_dir):
    os.makedirs(local_dir, exist_ok=True)
    for item in sftp_client.listdir(remote_dir):
        remote_item = os.path.join(remote_dir, item)
        local_item = os.path.join(local_dir, item)

        if sftp_client.stat(remote_item).st_mode & 0o40000:
            copy_directory(sftp_client, remote_item, local_item)
        else:
            try:
                sftp_client.get(remote_item, local_item)
            except FileNotFoundError:
                print(f"File: {remote_item} was not found on the SFTP server")

install()

try:
    subprocess.check_call(["OED Dependencies.bat"])
except FileNotFoundError as e:
    print(e)
