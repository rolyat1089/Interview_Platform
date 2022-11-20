# Scaler Interview Platform 
Scaler Interview Platform for internship


## Tech Stack Used:
1. Python Django Framework with sqlite database


## Installation
1. Clone this repository on local machine
```
git clone https://github.com/as'dlfka'sd
```
2. Create and activate a python virtual environment
```
python3 -m venv venv
source ./venv/bin/activate
```
3. Install the required packages from the requirements.txt file
```
pip install -r requirements.txt
```
4. Initializing the proejct
```
python3 manage.py makemigrations
python3 manage.py migrate
```
5. Create SuperUser 
```
python3 manage.py createsuperuser
```
6. Run the server
```
python3 manage.py runserver
```

## Note: 
I have only used python django framework becuse it provies a GUI-based admin panel, with all the required functionalities for this project. 
No Front-end has been built. 