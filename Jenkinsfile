@Library("elise-jenkins-scripts") _

pipeline {
    agent {
        docker {
            label "docker-host && linux"
            image "registry.devsec.sg/niktay/cs2102-builder:3.6-jessie"
            registryUrl "https://registry.devsec.sg"
            registryCredentialsId "devsecsg-docker-registry"
            args "-u root -v /var/run/docker.sock:/var/run/docker.sock:ro"
            alwaysPull true
        }
    }
    stages {
        stage("Install Dependencies") {
            failFast true
            parallel {
                stage("Install dependencies") {
                    steps {
                        sh "pip install -r requirements.txt"
                    }
                }
            }
        }
        stage("Unit Tests") {
            failFast true
            parallel {
                stage("Build repo difference for nightly release on master") {
                    steps {
                        sh "tox"
                    }
                }
            }
        }
    }
    post {
        always {
            sh "docker-compose down --remove-orphans"
        }
    }
}
