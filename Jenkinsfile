pipeline{
    agent any

    environment {
        DOCKER_IMAGE = 'eshop-recommender'
        TAG = "${GIT_BRANCH.split("/")[1]}-${GIT_COMMIT.substring(0, 6)}-${BUILD_NUMBER}"
    }

    options {
        ansiColor('xterm')
    }

    stages{
        stage("build image docker"){
            steps {
                echo '****** Build and tag image ******'
                script {
                    docker.build DOCKER_IMAGE + ":$TAG"
                }
            }
        }

        stage("Deploy image docker"){
            steps {
                echo '****** Deploy image ******'

                sh './jenkins/deploy.sh'
            }
        }
    }
}
