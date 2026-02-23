pipeline {
  agent any
  options { timestamps() }

  environment {
    DEPLOY_HOST = "104.236.22.107"
    DEPLOY_USER = "root"
    DEPLOY_PATH = "/opt/easytest/repo/AutoTestingPlatform"
    FRONTEND_SITE_PATH = "/opt/1panel/apps/openresty/openresty/www/sites/easytest/index"
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
                "cd ${DEPLOY_PATH} && SKIP_WEB_BUILD=1 BRANCH=${DEPLOY_BRANCH} ./deploy.sh"
              """
              sh """
                ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOY_HOST} \\
                "mkdir -p ${FRONTEND_SITE_PATH}"
              """
              sh """
                ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOY_HOST} \\
                "if [ -n '${FRONTEND_SITE_PATH}' ] && [ '${FRONTEND_SITE_PATH}' != '/' ]; then rm -rf '${FRONTEND_SITE_PATH}'/*; fi"
              """
              sh """
                scp -i "${SSH_KEY}" -o StrictHostKeyChecking=no -r web/dist/. \\
                ${SSH_USER}@${DEPLOY_HOST}:${FRONTEND_SITE_PATH}/
              """
              sh """
                ssh -i "${SSH_KEY}" -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOY_HOST} \\
                "cd ${FRONTEND_SITE_PATH} && test -f index.html && ls -lah assets && ls assets/index-*.js >/dev/null 2>&1"
              """
            } else {
              bat """
                icacls "%SSH_KEY%" /inheritance:r /grant:r "SYSTEM:R" /grant:r "Administrators:R"
                ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no %SSH_USER%@%DEPLOY_HOST% ^
                "cd %DEPLOY_PATH% && SKIP_WEB_BUILD=1 BRANCH=%DEPLOY_BRANCH% ./deploy.sh"
              """
              bat """
                icacls "%SSH_KEY%" /inheritance:r /grant:r "SYSTEM:R" /grant:r "Administrators:R"
                ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no %SSH_USER%@%DEPLOY_HOST% ^
                "mkdir -p %FRONTEND_SITE_PATH%"
              """
              bat """
                icacls "%SSH_KEY%" /inheritance:r /grant:r "SYSTEM:R" /grant:r "Administrators:R"
                ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no %SSH_USER%@%DEPLOY_HOST% ^
                "rm -rf %FRONTEND_SITE_PATH%/*"
              """
              bat """
                icacls "%SSH_KEY%" /inheritance:r /grant:r "SYSTEM:R" /grant:r "Administrators:R"
                scp -i "%SSH_KEY%" -o StrictHostKeyChecking=no -r web/dist/. ^
                %SSH_USER%@%DEPLOY_HOST%:%FRONTEND_SITE_PATH%/
              """
              bat """
                icacls "%SSH_KEY%" /inheritance:r /grant:r "SYSTEM:R" /grant:r "Administrators:R"
                ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no %SSH_USER%@%DEPLOY_HOST% ^
                "cd %FRONTEND_SITE_PATH% && test -f index.html && ls -lah assets && ls assets/index-*.js >/dev/null 2>&1"
              """
            }
          }
        }
      }
    }
  }
}
