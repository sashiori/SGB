from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
 
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)
 
# https://drive.google.com/drive/u/0/folders/#################################
folder_id = '14RUXCD8xSkvUFMYu37YQopmda7vZSTbx'
#folder_id = '1HpUBDPAVqvnOlFUxFwU-u3OjFdoxYO0_'
file_name = '13cm_OK_2022-05-11_16-22-43_35.6311_139.7877.jpg'
 

file = drive.CreateFile({
    'title': file_name,
    'mimeType': 'image/jpeg', 
    'parents': [
        {'id': folder_id}
        ]
    })
 
## Upload
file.SetContentFile(file_name)
file.Upload()
print('Complete Upload')