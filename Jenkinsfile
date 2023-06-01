// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {
    agent any

    environment {
        server_name = credentials('name_spcat')
        server_host = credentials('host_spcat')
        ssh_key = credentials('spcat_key')
    }

    stages {
        stage('Connection to AWS server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = ssh_key_USR
                    remote.name = server_name
                    remote.host = server_host
                    
                }
            }
        }

        stage('Verify Api folder and environment') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Verify and create the api_SPCAT folder if it does not exist and the virtual environment
                        if [ ! -d api_SPCAT ]; then
                            mkdir ./api_SPCAT
                            cd ./api_SPCAT
                            python3 -m venv env
                        fi
                    '''
                    
                }
            }
        }
        
        stage('Stop previous API') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Stop the API if it is running
                        
                        cd ./api_SPCAT

                        if [ -f pid.txt ]; then
                            PID_API_SPCAT=$(cat pid.txt)
                            if kill -0 "$PID_API_SPCAT" 2>/dev/null; then
                                echo "The process exists, stopping it..."
                                kill "$PID_API_SPCAT"
                            fi
                        fi
                    '''
                }
            }
        }
        
        stage('Backup previous files') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Saving old API files
                        cd ./api_SPCAT
                        rm -rf api_antiguo
                        if [ -d api_actual ]; then
                            mv api_actual api_antiguo
                        fi
                    '''
                }
            }
        }
        
        stage('Download latest release') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Download the latest release from GitHub
                        cd ./api_SPCAT
                        rm -rf releaseApi.zip
                        curl -LOk https://github.com/CIAT-DAPA/spcat_webapi/releases/latest/download/releaseApi.zip
                        rm -rf api_actual
                        unzip releaseApi.zip -d api_actual
                    '''
                }
            }
        }
        
        stage('Update dependencies') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        cd ./api_SPCAT
                        # Activate the virtual environment
                        source env/bin/activate
                        
                        # Updating the dependencies
                        pip install --upgrade setuptools wheel
                        pip install -r api_actual/requirements.txt
                    '''
                }
            }
        }
        
        stage('Start API') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Configure variables for deployment
                        while IFS= read -r line; do
                            export "$line"
                        done < variables.txt

                        
                        # Activate the virtual environment
                        cd ./api_SPCAT
                        source env/bin/activate

                        

                        # Start API
                        cd ./api_actual
                        nohup python3 api.py > api_spcat.log 2>&1 &
                        
                        # Get the new PID and save it to a file
                        PID_API_SPCAT=$!
                        echo $PID_API_SPCAT > ../pid.txt
                    '''
                }
            }
        }

        stage('Verify API') {
            steps {
                script {
                    def apiUrl = "http://127.0.0.1:5000"

                    //def response = sh(script: "curl -sL -w \"%{http_code}\" -o /dev/null ${apiUrl}", returnStdout: true)

                    def response = sshCommand remote: remote, command: "curl -sL -w \"%{http_code}\" -o /dev/null ${apiUrl}"

                    if (response.trim() == '200') {
                        echo "API is running correctly."
                    } else {
                        error "API is not running correctly. Rolling back..."
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                sshCommand remote: remote, command: '''
                    # Configure variables for deployment
                    while IFS= read -r line; do
                        export "$line"
                    done < variables.txt

                    # Rollback to the previous API if any step fails
                    cd ./api_SPCAT
                    rm -rf api_actual
                    mv api_antiguo api_actual

                    # Activate the virtual environment
                    source env/bin/activate

                    # Start API
                    cd ./api_actual
                    nohup python3 api.py > api_spcat.log 2>&1 &
                    
                    # Get the new PID and save it to a file
                    PID_API_SPCAT=$!
                    echo $PID_API_SPCAT > ../pid.txt
                '''
            }
        }
    }
}