pipeline {
    agent any

    environment {
        BASE_URL = credentials('xfit_base_url')
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Получаем код из репозитория'
                checkout scm
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Install & Run') {
            steps {
                echo '🐍 Установка зависимостей и запуск тестов'
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                    echo "BASE_URL=$BASE_URL" > .env
                    .venv/bin/pytest tests/ --alluredir=allure-results --maxfail=1 --disable-warnings -v
                '''
            }
        }

        stage('Allure Report') {
            steps {
                echo '📊 Генерация Allure отчета'
                allure([
                    includeProperties: false,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            echo '🧹 Очистка окружения'
            sh 'rm -rf .venv'
        }

        success {
            echo '✅ Все тесты прошли успешно!'
        }

        failure {
            echo '❌ Ошибка: Проверь отчёт и логи'
        }
    }
}
