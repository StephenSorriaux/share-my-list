IMAGE_NAME = 'ssorriaux/share-my-list'

node {
    stage('Checkout') {
        cleanWs()
        git url: 'https://github.com/StephenSorriaux/share-my-list.git'
    }
    docker.image('python:3.6-alpine3.8').inside {
        stage('Install') {
            sh 'pip install -r requirements.txt'
            VERSION = sh(script:'python -c "import xmas_list; print(xmas_list.VERSION)"', returnStdout: true).trim()
        }
        stage('Tests') {
            sh 'python manage.py test lists'
        }
    }
    stage('Build image') {
        withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
            sh "docker login -u ${USER} -p ${PASSWORD}"
        }
        sh "docker build -t ${IMAGE_NAME}:${VERSION} ."
        sh "docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:latest"
        sh "docker push ${IMAGE_NAME}:${VERSION}"
        sh "docker push ${IMAGE_NAME}:latest"
    }
    stage('Deploy') {
        withPythonEnv('python') {
            sh 'pip install ansible==2.7.1'
            withCredentials([
                usernamePassword(credentialsId: 'stephen-noel', usernameVariable: 'stephen_noel_ADMIN_USERNAME', passwordVariable: 'stephen_noel_ADMIN_PASSWORD'),
                usernamePassword(credentialsId: 'tiphany-noel', usernameVariable: 'tiphany_noel_ADMIN_USERNAME', passwordVariable: 'tiphany_noel_ADMIN_PASSWORD')]){
                    sshagent(credentials: ['github-ssh']) {
                        sh "ansible-playbook -i deploy/inventory.yml -e image_name='${IMAGE_NAME}:${VERSION}' deploy/playbook.yml -vv"
                }
            }
        }
    }
}