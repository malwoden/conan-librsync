pipeline {
    agent any
    stages {
        stage('Build All') {
            steps {
                cleanWs
                checout scm
                scripts {
                    sh "python build.py"
                }
            }
        }
    }
}
