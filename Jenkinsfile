pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USER = 'sarimali17'
        EC2_IP = '3.106.156.32'
    }

    stages {
        stage('Fetch') {
            steps {
                checkout scm
            }
        }

        stage('Build and Run') {
            steps {
                sh '''
                    docker stop sentiment-test || true
                    docker rm sentiment-test || true
                    docker build -t sentiment-api:test .
                    docker run -d --name sentiment-test -p 5000:5000 sentiment-api:test
                    sleep 20
                '''
            }
        }

        stage('Unit Test') {
            steps {
                sh '''
                    docker run --rm \
                        --network host \
                        -v $(pwd)/tests:/tests \
                        sentiment-api:test \
                        sh -c "pip install pytest requests --quiet && BASE_URL=http://127.0.0.1:5000 python -m pytest /tests/test_api.py -v"
                '''
            }
        }

        stage('UI Test') {
            steps {
                sh '''
            # Run selenium test using a container that has Chrome built in
            docker run --rm \
                --network host \
                -v $(pwd)/tests:/tests \
                -e BASE_URL=http://127.0.0.1:5000 \
                selenium/standalone-chrome:latest \
                bash -c "pip install pytest selenium requests --quiet && python -m pytest /tests/test_ui.py -v"
        '''
            }
        }

        stage('Build and Push') {
            steps {
                sh '''
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker build -t $DOCKERHUB_USER/sentiment-api:unstable .
                    docker push $DOCKERHUB_USER/sentiment-api:unstable
                    git fetch origin stable-fallback
                    git checkout origin/stable-fallback -- app.py
                    docker build -t $DOCKERHUB_USER/sentiment-api:stable .
                    docker push $DOCKERHUB_USER/sentiment-api:stable
                    git checkout HEAD -- app.py
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
            kubectl apply -f k8s/pvc.yaml --validate=false
            kubectl apply -f k8s/blue-deployment.yaml --validate=false
            kubectl apply -f k8s/green-deployment.yaml --validate=false
            kubectl apply -f k8s/service.yaml --validate=false
            kubectl rollout status deployment/sentiment-blue-deployment --timeout=300s
        '''
            }
        }
    }

    post {
        always {
            sh '''
                docker stop sentiment-test || true
                docker rm sentiment-test || true
            '''
        }
    }
}
