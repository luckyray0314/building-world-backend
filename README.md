# R&I Software



### Installing Dependencies for the Backend

1. **Python 3.9** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3.9/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the project directory and running:
```bash
# On Windows:
py -m pip install -r requirements.txt
# On Linux:
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


<!-- 4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.  -->


## Database Setup
Set database url as an environment variable:
```bash
# On Windows:
set DATABASE_URL=dialect+driver://username:password@host:port/database;
# On Linux:
export DATABASE_URL=dialect+driver://username:password@host:port/database;
```
or insert database url to `config.cfg` file. If none of them is provided, SQLite will be applied.


### Database Recreate (Drop all and create)
```bash
# On Windows:
set DB_RESTART=true
# On Linux:
export DB_RESTART=true
```
> Set it empty or any string to skip.

## Running the server

First of all, activate venv by running this command in the project directory:

```bash
# On Windows:
venv\Scripts\activate
# On Linux:
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```


### Run APP API:
```bash
# On Windows:
py manage.py
# On Linux:
python3 manage.py
```

You can see app running on http://127.0.0.1:5000.

#### **WARNING!!!** The React project can be configured to redirect any requests it receives on its port 3000 that it does not understand into another server. This is configured simply by adding a proxy key at the bottom `package.json`:
```json
{

  /* ... leave all other configuration options alone ... */

  "proxy": "http://localhost:5000"
}
```


# Rest API
## Getting started
* All the documentations for Rest API are seperated and can be found in `server\docs` and select one related to.
* There is a sample Postman test collection `server\tests\risoftware.postman_collection.json` so you can try your first requests.
## Endpoints
See Postman collection.


## APP Resources:
* APP on webserver: https://

