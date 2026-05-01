pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\csha0\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/csha01/RAGAs_handson.git'
            }
        }

        stage('Install') {
            steps {
                bat '%PYTHON% -m pip install -r requirements.txt --no-build-isolation --ignore-requires-python || echo "Some packages failed, continuing..."'
            }
        }

        stage('Test') {
            steps {
                bat '%PYTHON% -m pytest'
            }
        }

        stage('Run') {
            steps {
                bat '%PYTHON% app.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS!'
        }
        failure {
            echo 'Pipeline FAILED!'
        }
    }
}