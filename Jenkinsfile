pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url')  //
    }

    tools {
        allure 'Allure'  //
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Клонируем репозиторий'
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                echo '📦 Установка зависимостей'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                echo '🚀 Запуск pytest с Allure'
                sh '''
                    echo "BASE_URL=$BASE_URL" > .env
                    pytest tests/ --alluredir=allure-results --tb=short -v
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'allure-results']]
            }
        }
    }

    post {
        failure {
            echo '❌ Тесты упали'
        }
        success {
            echo '✅ Все тесты прошли успешно'
        }
    }
}
