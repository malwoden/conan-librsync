pipeline {
    agent any
    stages {
        stage('Build All') {
            steps {
                cleanWs()
                checkout scm
                scripts {
                    sh "python build.py"
                }
            }
        }
    }
}
