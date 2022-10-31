## Requirement
- **Hardware**
  - Raspberry Pi 4 x 1
    - OS
      - Raspberry Pi OS (32bit) A port of Debian Bullseye with the Raspberry Pi Desktop(Recommended)
  - Ultrasonic Sensor ( HC-SR04 x 1 )
    - Refer to the URL below for connection instructions
      - https://docs.google.com/presentation/d/1Yl0rTtObqlFzNm60XbpwrSdwZb74A1tI1dZzBSoTG1E/edit#slide=id.g122536f94d7_0_0
  - Night Vision Camera ( UC026-U-AA-11 x 1 )
- **Software**
  - Python 3.7
  - PyTorch 1.4.0
    - torchvision 0.5.0
  - Model
    - model_0511.pth (original model)
    - [https://drive.google.com/file/d/1JbS-nyGOKk4umhQXYYAxgmwlNZcoopTk/view?usp=sharing](https://drive.google.com/file/d/1JbS-nyGOKk4umhQXYYAxgmwlNZcoopTk/view?usp=sharing)
  - Other
    - Libraries for Python
       
### File
- Type1
  - inference0511.py
  - Image recognition to determine if it is a plastic bottle
- Type2
  - upto5DWM.py
  - In addition to Type1, upload files to the specified GoogleDrive

---
## Type1
### Function
1. Detects that something(garbage) has been thrown into the trash
2. Measure the amount of garbage
3. Camera shooting & Recognizes if it is a plastic bottle or not

### Install


**Step 1**. Installation of Raspi libraries
```
$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install libffi-dev libssl-dev openssl -y
$ sudo apt install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev -y
$ sudo apt install libatlas-base-dev libjasper-dev libavutil-dev libavcodec-dev libavformat-dev libswscale-dev -y
```

**Step 2**. Installation for using Python 3.7
```
$ wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
$ tar zxvf Python-3.7.3.tgz
$ cd Python-3.7.3
$ ./configure
$ make
$ sudo make install
```

**Step 3**. Installation for using PyTorch
```
$ git clone https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B.git
$ cd PyTorch-and-Vision-for-Raspberry-Pi-4B
$ sudo pip3 install torch-1.4.0a0+f43194e-cp37-cp37m-linux_armv7l.whl
$ sudo pip3 install torchvision-0.5.0a0+9cdc814-cp37-cp37m-linux_armv7l.whl
```

**Step 4**. Installation for ultrasonic sensors and cameras
```
$ sudo pip3 install RPi.GPIO opencv-python picamera
```

**Step 5**.
Enable Raspberry pi Camera 
```
$ sudo raspi-camera
```
Select "Interface Options" -> "I1 Legacy Camera Enable"

**Step 6**. Download Files
- inference0511.py
- model_0511.pth

**Step 7**. Execution check
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

**Step 1 〜 Step 4** : Same as Type1

**Step 5**. Download Files
- upto5DWM0511.py
- client_secrets.json
- credentials.json

**Step 6**. 
- PyDrive2 is a wrapper library of google-api-python-client that simplifies many common Google Drive API V2 tasks. 
```
$ sudo pip3 install PyDrive2
```

**Step 7**.
- make settings.yaml
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

**Step 8**.
<span style="color: red; ">Not required if you download and try my client_secrets.json and credentials.json files</span>
1. Access to cloud.google.com/developers
2. Follow the web page at the URL below.
   https://docs.logicaldoc.com/en/google-drive/configuring-google-drive-api
4. Download client_secrets.json


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

4. Verify Authentication
```
$ python3 auth.py
```
A web browser will open and GoogleDrive settings screen appears and check the box.

**Step9**. Execution check
```
$ python3 upto5DWM0511.py
```
