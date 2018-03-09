pipeline {
    agent any
    stages {
        stage('Build All') {
            steps {
                cleanWs()
                checkout scm
                script {
                    sh "python build.py"
                }
            }
        }
    }
}
