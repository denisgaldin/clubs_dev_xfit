pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url')  // добавь переменную в Jenkins > Credentials
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Получаем код из репозитория'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Установка зависимостей'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🚀 Запуск тестов'
                sh 'pytest tests/ --tb=short -v'
            }
        }
    }
}
