pipeline{
    agent any
    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }
    environment{
        
        image_tag='docker.pkg.github.com/mayuri-dhote/cockpit-backend/cockpitapp:${GIT_COMMIT}'
        cred=credentials('cockpit')
        
    }
    
    stages{
        
       
        stage("building docker image")
        {
            steps{
                sh "docker build -t $image_tag ."
            }
        }
    }  
}