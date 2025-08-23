pipeline {
    agent any
    environment {
        // If you use Jenkins credentials, you can bind them here
        // CREDENTIALS_B64 = credentials('jenkins-credentials-id')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Set up Python') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install playwright'
                sh '. venv/bin/activate && playwright install chromium'
            }
        }
        stage('Restore credentials file') {
            steps {
                // If using Jenkins secret text (base64), decode it to credentials.csv
                // sh 'echo "$CREDENTIALS_B64" | base64 -d > credentials.csv'
                // Or, if you upload credentials.csv directly, copy it here
                // sh 'cp /path/to/secure/credentials.csv credentials.csv'
            }
        }
        stage('Run reviver script') {
            steps {
                sh '. venv/bin/activate && python reviver.py'
            }
        }
    }
    triggers {
        cron('30 18 1 * *') // Monthly at midnight IST (18:30 UTC on the 1st)
    }
}
