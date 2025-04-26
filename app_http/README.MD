# App Http Client

A command line application that can communicate with an HTTP application representing an online store.
WebServer - UtmShop

## Features

- The application can list all categories
- The application can display details about a category
- The application can create a new category
- The application can delete a category
- The application can modify the title of a category
- The application can create new products in a category
- The application can view the list of products in a category

## Requirements

- Python 3.x
- Docker Desktop
- Required packages: 
```bash
pip install -r requirements.txt
```


### Starting the console app

1. Install requirements
```bash
pip install -r requirements.txt
```

2. Build and start the Docker container:
```bash
docker-compose up --build
```

### Run the app

1. Navigate to app_http/ forlder and use the commandd
```bash
python3 ./app.py
```



## Project Structure

```bash
app_http/
├── UtmShop/
├── Dockerfile
├── docker-compose.yml
├── app.py             
├── api_client.py      
├── requirements.txt    
└── README.md                
```