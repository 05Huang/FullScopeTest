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
    stage('Build Frontend (Local)') {
      steps {
        dir('web') {
          script {
            if (isUnix()) {
              sh 'npm ci && npm run build'
            } else {
              bat 'npm ci && npm run build'
            }
          }
        }
      }
    }
    stage('Deploy') {
      steps {
        withCredentials([sshUserPrivateKey(
          credentialsId: "${SSH_CREDENTIALS_ID}",
          keyFileVariable: 'SSH_KEY',
          usernameVariable: 'SSH_USER'
        )]) {
          script {
            if (isUnix()) {
              sh """
                ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOY_HOST} \\
                "mkdir -p ${DEPLOY_PATH}/web/dist"
              """
              sh """
                scp -i "${SSH_KEY}" -o StrictHostKeyChecking=no -r web/dist/* \\
                ${SSH_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/web/dist/
              """
              sh """
                ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOY_HOST} \\
                "cd ${DEPLOY_PATH} && SKIP_WEB_BUILD=1 BRANCH=${DEPLOY_BRANCH} ./deploy.sh"
              """
            } else {
              bat """
                ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no %SSH_USER%@%DEPLOY_HOST% ^
                "mkdir -p %DEPLOY_PATH%/web/dist"
              """
              bat """
                scp -i "%SSH_KEY%" -o StrictHostKeyChecking=no -r web/dist/* ^
                %SSH_USER%@%DEPLOY_HOST%:%DEPLOY_PATH%/web/dist/
              """
              bat """
                ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no %SSH_USER%@%DEPLOY_HOST% ^
                "cd %DEPLOY_PATH% && SKIP_WEB_BUILD=1 BRANCH=%DEPLOY_BRANCH% ./deploy.sh"
              """
            }
          }
        }
      }
    }
  }
}
