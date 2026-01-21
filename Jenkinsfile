pipeline {
  agent any
  options { timestamps() }

  environment {
    DEPLOY_HOST = "104.236.22.107"
    DEPLOY_USER = "root"
    DEPLOY_PATH = "/opt/apps/easytest/repo/AutoTestingPlatform"
    SSH_CREDENTIALS_ID = "easytest-ssh"
    DEPLOY_BRANCH = "main"
  }

  stages {
    stage('Deploy') {
      steps {
        sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
          sh """
            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} \\
            "cd ${DEPLOY_PATH} && BRANCH=${DEPLOY_BRANCH} ./deploy.sh"
          """
        }
      }
    }
  }
}
