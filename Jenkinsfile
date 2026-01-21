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
        sshagent(credentials: ["${SSH_CREDENTIALS_ID}"]) {
          script {
            if (isUnix()) {
              sh """
                ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} \\
                "mkdir -p ${DEPLOY_PATH}/web/dist"
              """
              sh """
                scp -o StrictHostKeyChecking=no -r web/dist/* \\
                ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/web/dist/
              """
              sh """
                ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} \\
                "cd ${DEPLOY_PATH} && SKIP_WEB_BUILD=1 BRANCH=${DEPLOY_BRANCH} ./deploy.sh"
              """
            } else {
              bat """
                ssh -o StrictHostKeyChecking=no %DEPLOY_USER%@%DEPLOY_HOST% ^
                "mkdir -p %DEPLOY_PATH%/web/dist"
              """
              bat """
                scp -o StrictHostKeyChecking=no -r web/dist/* ^
                %DEPLOY_USER%@%DEPLOY_HOST%:%DEPLOY_PATH%/web/dist/
              """
              bat """
                ssh -o StrictHostKeyChecking=no %DEPLOY_USER%@%DEPLOY_HOST% ^
                "cd %DEPLOY_PATH% && SKIP_WEB_BUILD=1 BRANCH=%DEPLOY_BRANCH% ./deploy.sh"
              """
            }
          }
        }
      }
    }
  }
}
