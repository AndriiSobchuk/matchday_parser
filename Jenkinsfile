pipeline {
    agent any
    environment {
        PROJECT_ID = 'our-axon-367118'
        CLUSTER_NAME = 'cluster-1'
        LOCATION = 'us-west1'
        CREDENTIALS_ID = 'My First Project'
    }
    stages {
        stage('Deploy to GKE') {
            steps{
                
                step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'deployment.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
            }
        }
    }    
}