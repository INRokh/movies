# movies
To create a VM do the following:
1. Create new project in GCP.
2. Enable Google Sheets API.
3. Create a small (f1-mini) Virtual Machine.
4. Create or use existing service account and download secret.json (APIs & Services - Credentials)

To deploy the service to a Ubuntu VM do the following:
Download movie files:
```
$ wget https://datasets.imdbws.com/title.basics.tsv.gz
$ wget https://datasets.imdbws.com/title.ratings.tsv.gz
```
Unzip the files:
```
$ ungzip *.gz
```
Update available Linux packages:
```
$ sudo apt update
```
Install pip for python3 using sudo:
```
$ sudo apt install python3-pip
```
Upload script files to the VM using Google Cloud Console UI or `scp`
Install Google Sheets dependencies:
```
$ pip3 install -r requirements.txt --upgrade 
```
Start service:
```
python3 service.py
```

Use command `top` to monitor CPU and memory usage. Press `q` to quit.
Use command `exit` to close the session to VM. This will stop the
service as well. If you want to keep service running start it like this:
```
$ nohup python3 service.py &
```
Use kill PID to exit gracefully.
