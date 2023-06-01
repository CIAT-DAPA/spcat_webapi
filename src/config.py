import os 

config = {}

if os.getenv('DEBUG', "true").lower() == "true":
    config['DEBUG'] = True
    config['HOST'] = 'localhost'
    config['PORT'] = 5000
    config['CONNECTION_DB']='mongodb://localhost:27017/dbgap'
else:
    config['DEBUG'] = False
    config['HOST'] = '0.0.0.0'
    config['PORT'] = os.getenv('API_SPCAT_PORT')
    config['CONNECTION_DB']=os.getenv('CONNECTION_DB')