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
                    # Stop and remove existing container if running
                    docker stop sentiment-test || true
                    docker rm sentiment-test || true

                    # Build the unstable image
                    docker build -t sentiment-api:test .

                    # Run container for testing
                    docker run -d --name sentiment-test -p 5000:5000 sentiment-api:test

                    # Wait for app to be ready
                    sleep 15
                '''
            }
        }

        stage('Unit Test') {
            steps {
                sh '''
                    # Run pytest in a container against the running app
                    docker run --rm \
                        --network host \
                        -v $(pwd)/tests:/tests \
                        -e BASE_URL=http://127.0.0.1:5000 \
                        sentiment-api:test \
                        python -m pytest /tests/test_api.py -v \
                        --override-ini="base_url=http://127.0.0.1:5000"
                '''
            }
        }

        stage('UI Test') {
            steps {
                sh '''
                    # Run Selenium UI test using host Chrome
                    docker run --rm \
                        --network host \
                        -v $(pwd)/tests:/tests \
                        sentiment-api:test \
                        python -m pytest /tests/test_ui.py -v
                '''
            }
        }

        stage('Build and Push') {
            steps {
                sh '''
                    # Login to DockerHub
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin

                    # Build and push unstable image
                    docker build -t $DOCKERHUB_USER/sentiment-api:unstable .
                    docker push $DOCKERHUB_USER/sentiment-api:unstable

                    # Build and push stable image from stable-fallback branch
                    git fetch origin stable-fallback
                    git checkout origin/stable-fallback -- app.py
                    docker build -t $DOCKERHUB_USER/sentiment-api:stable .
                    docker push $DOCKERHUB_USER/sentiment-api:stable

                    # Restore main branch app.py
                    git checkout HEAD -- app.py
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    # Apply Kubernetes manifests
                    kubectl apply -f k8s/pvc.yaml
                    kubectl apply -f k8s/blue-deployment.yaml
                    kubectl apply -f k8s/green-deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    # Wait for blue deployment to be ready
                    kubectl rollout status deployment/sentiment-blue-deployment --timeout=300s
                '''
            }
        }

    }

    post {
        always {
            sh '''
                # Cleanup test container
                docker stop sentiment-test || true
                docker rm sentiment-test || true
            '''
        }
    }
}