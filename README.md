# Web API gap analysis  

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/spcat_webapi) ![](https://img.shields.io/github/v/tag/CIAT-DAPA/spcat_webapi)

This repository is a web API developed in Python which is responsible for collecting information from the gap database. It contains the endpoints that will be in charge of obtaining the data of countries, crops and accessions, the get crops endpoint is in charge of obtaining the information of crops, the get countries endpoint is in charge of obtaining the information of countries and the get accessions endpoint is in charge of obtaining all the information of accessions.

**Important notes**

This web api must be used in conjunction with the ORM that was developed for the project, which you can find in this [repository](https://github.com/CIAT-DAPA/spcat_orm).

## Getting Started

To use the wep api, it is necessary to have an instance of MongoDB running, either locally or on a server that is accessible from the internet.

### Prerequisites

- Python 3.x
- MongoDB

## Installation

To use the wep api, it is necessary to have an instance of MongoDB running. It is also recommended to create a virtual environment to work with this project and make sure that the dependencies are installed in the virtual environment instead of the global system.

1. Clone the repository
````sh
git clone https://github.com/CIAT-DAPA/spcat_webapi.git
````

2. Create a virtual environment
````sh
python -m venv env
````

3. Activate the virtual environment
- Linux
````sh
source env/bin/activate
````
- windows
````sh
env\Scripts\activate.bat
````

4. Install the required packages

````sh
pip install -r requirements.txt
````

5. Running api

````sh
python api.py
````

## Usage

### Configuration

The parameters to be configured are found in the `config.py` file. This file has information on how to connect to the database, when deploying the web api on a production server these data must be configured as environment variables. Let's see what it has:

| Parameter     |type   | Description|
|---------------|-------|------------|
|DEBUG          |boolean|boolean that defines whether you are in a test environment or in production.|
|HOST           |string |IP or hostname of the server in which is the wep api. By default is: 0.0.0.0|
|PORT           |string |Port in which is available the wep api in the server. By default is: 5000   |
|CONNECTION_DB  |string |utl for connection to the database                                          |

