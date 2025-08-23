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
                // Create venv only if it doesn't exist
                sh '[ -d venv ] || python3 -m venv venv'
                // Install pip dependencies only if not already installed
                sh '. venv/bin/activate && python -c "import playwright" 2>/dev/null || pip install playwright'
                // Install Playwright browsers only if not already installed
                sh '. venv/bin/activate && [ -d venv/playwright-browsers ] || playwright install chromium'
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
