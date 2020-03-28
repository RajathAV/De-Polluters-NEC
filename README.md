# De-Polluters-NEC
This repository is for NEC Hackathon purpose. 

Instructions to use this Repository:

## Step 1: Initializing DB. 

```
export USER=<username>
export PASS=<password>
export DB=<dbname>
export HOST=<hostname>
```
## Step 2: Starting the server

#### To run as container(to build image using docker file)
docker-compose up -d 

#### To run as a non containerized application
python3 app.py
###### This would render the reporting dashboard
