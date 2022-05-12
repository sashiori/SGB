## Smart Garbage Box
- Project Name：Plastic Garbage Reduction Project
- Project Member: AAII(Asia AI Institute), Musashino University
- Date: 2022/05/11
- File Name: inference0511.py

## File
- Type1 inference0511.py: Only inference: inference0511.py
- Type2 upto5DWM.py: inference & upload to google drive

---
## Type1
### Function
1. Detects that something(garbage) has been thrown into the trash
2. Measure the amount of garbage
3. Camera shooting & Recognizes if it is a plastic bottle or not

### Requirement
- Hardware
  - Raspberry Pi 4 x 1
    - Raspberry Pi OS (32bit) A port of Debian Bullseye with the Raspberry Pi Desktop(Recommended)
  - Ultrasonic Sensor: HC-SR04 x 1
  - Night Vision Camera: UC026-U-AA-11 x 1
- Software
  - Python 3.7.3
  - PyTorch 1.4.0
    - torchvision 0.5.0
  - File(https://drive.google.com/drive/folders/1iq7sFHaVGhaBasbLf_XBaMEz9bbkWS__?usp=sharing)
    - inference0511.py
    - model_0511.pth

Step 1. Installation of Raspi libraries
```
$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install libffi-dev libssl-dev openssl -y
$ sudo apt install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev -y
$ sudo apt install libatlas-base-dev libjasper-dev libavutil-dev libavcodec-dev libavformat-dev libswscale-dev -y
```

Step 2. Installation for using Python 3.7
```
$ wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
$ tar zxvf Python-3.7.3.tgz
$ cd Python-3.7.3
$ ./configure
$ make
$ sudo make install
```

Step 3. Installation for using PyTorch
```
$ git clone https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B.git
$ cd PyTorch-and-Vision-for-Raspberry-Pi-4B
$ sudo pip3 install torch-1.4.0a0+f43194e-cp37-cp37m-linux_armv7l.whl
$ sudo pip3 install torchvision-0.5.0a0+9cdc814-cp37-cp37m-linux_armv7l.whl
```

Step 4. Installation for ultrasonic sensors and cameras
```
$ sudo pip3 install RPi.GPIO opencv-python picamera
```

Step 5. Download Files
- inference0511.py
- model_0511.pth

Step 6. Execution check
```
$ python3 inference0511.py
```

### Execution example
```
aaii@raspberrypi:~ $ python3 inference20220426.py 
OK: preparation inference model
Measurement start...
Garbage has been put in.  2022-05-11 08:06:34
count_id           : 1
past_distance      : 34 [cm]
current_distance   : 22 [cm]
difference_distance: 12 [cm]
garbage            :OK (plastic_bottles)

Garbage has been put in.  2022-05-11 08:07:00
count_id           : 2
past_distance      : 25 [cm]
current_distance   : 18 [cm]
difference_distance: 7 [cm]
garbage            :OK (plastic_bottles)

Garbage has been put in.  2022-05-11 08:37:28
count_id           : 3
past_distance      : 18 [cm]
current_distance   : 10 [cm]
difference_distance: 8 [cm]
garbage            :NG (plastic_bottles)
```
---
## Type2
### Function
1. Same as Type1
2. Upload to 5D World Map Folder (=Google Drive)

### Requirement
- Same as Type1

Step 1 〜 Step 4 : Same as Type1

Step 5. Download Files
- upto5DWM0511.py

Step 6. 
```
$ sudo pip3 install PyDrive2
```
Step 7.
1. Access to cloud.google.com/developers
2. Login
3. Access to cloud.google.com/developers again
4. Follow the web page at the URL below.
   https://docs.logicaldoc.com/en/google-drive/configuring-google-drive-api
5. Copy Client ID & Client Secret

Step 8.
1. make settings.yaml
 ```
client_config_backend: settings
client_config:
  client_id: <Client ID>
  client_secret: <Client Secret>
 
save_credentials: True
save_credentials_backend: file
save_credentials_file: credentials.json

get_refresh_token: True
    - https://www.googleapis.com/auth/drive.file
    - https://www.googleapis.com/auth/drive.install
```

2. Sign in to Google with the account above.
- Download client_secrets.json from Google API Console
- OAuth2.0 is done in two lines. 
- You can customize behavior of OAuth2 in one settings file settings.yaml.
3. make auth.py
```
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
 
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)
```


4. $ python3 auth.py
   Web




Execution check
```
$ python3 upto5DWM0511.py
```