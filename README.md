# TechTrends Web Application

This is a Flask application that lists the latest articles within the cloud-native ecosystem.

## Run 

To run this application there are 2 steps required:

1. Initialize the database by using the `python init_db.py` command. This will create or overwrite the `database.db` file that is used by the web application.
2.  Run the TechTrends application by using the `python app.py` command. The application is running on port `3111` and you can access it by querying the `http://127.0.0.1:3111/` endpoint.


`http://192.168.1.137:3111/`
`python -m venv techtrend-env`
`source techtrend-env/bin/activate`
`pip install -r requirements.txt`

## Docker

### Build the Docker Image

```commandline
docker build -t techtrends -f Dockerfile .
```

### Run the Docker Container

```commandline
docker run -p 3111:3111 techtrends
docker run -d -p 7111:3111 techtrends
```

Access the application in the browser using the http://127.0.0.1:7111 endpoint and try to click on some of the available posts, 
create a new post, access the metrics endpoint, etc.