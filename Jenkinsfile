pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url')  //
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Получаем код из репозитория'
                checkout scm
            }
        }

        stage('Setup Virtualenv & Install Dependencies') {
            steps {
                echo '📦 Создание виртуального окружения и установка зависимостей'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🚀 Запуск автотестов'
                sh '''
                    . venv/bin/activate
                    pytest tests/ --tb=short -v
                '''
            }
        }
    }
}
