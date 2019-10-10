# Movie Ratings

Service allowing to get IMDB ratings for a batch of movies you are considering to watch.

# Deployment to Google Cloud

## Create VM

1. Create new project in GCP.
1. Enable Google Sheets API.
1. Create a small (f1-mini) Virtual Machine installing the latest stable Container OS.
1. Before starting VM add sheets scope running in Cloud Shell: 

```shell
gcloud beta compute instances set-scopes <instance-name> --scopes=default,https://www.googleapis.com/auth/spreadsheets --zone=<instance-zone>
```

## Create Google Sheet

1. Create a new Google Sheet to use as input and output.
1. Give GCP service account (compute) to the sheet.

## Run container

1. SSH into the VM.
2. Clone this repository and cd into it:
```shell
git clone https://github.com/INRokh/movies.git

cd movies
```
3. Modify Docker file overriding existing flags (you at least will need to set your sheet ID).
4. Build the image: 
```shell
docker build --tag=movies .
```
5. Run the container as a daemon:
```shell
docker run -d --restart unless-stopped movies
```
