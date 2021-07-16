pipeline {
    agent any
    environment{
        today = sh(returnStdout:true, script: 'date +%Y-%m-%d').trim()
        //today = '2021-01-01'
        currentYear = sh(returnStdout:true, script: 'date +%Y').trim()
        holiday = false
        jsonData = ""
    }
    stages {
        stage('Git Pull') {
            steps {
               git credentialsId: 'github token', branch: 'main', url: 'https://github.com/Lokesh99623/devops.git'
            }
        }
        stage('Is the run required?'){
            steps{
                httpRequest outputFile: 'build.json', quiet: true, responseHandle: 'NONE', url: 'https://calendarific.com/api/v2/holidays?&api_key=d20d05ccb411d9ce3b56b654971e17a29b0aa1ed&country=IN&year='+currentYear, wrapAsMultipart: false
                script{
                jsonData = readJSON(text: readFile("./build.json").trim())
                def dateArray = jsonData.response.holidays.date.iso
               dateArray.each{ date ->
               if("${date}".contains('T')){
                   if("${today}".equals("${date.split('T')[0]}"))
                   holiday = true
               }else if("${today}".equals("${date}"))
                   holiday = true
               }
                }
            }
        }
        stage('Build'){
            when {
                expression { holiday == true }
            }
            steps{
                script{
                      dir('build'){
                def nameArray = jsonData.response.holidays.name
                nameArray.each { name ->
                //replacing name containing / with _
                    filename = name.replace('/','_')
                    jsonData.response.holidays.each { 
                    if(it.name.equals(name))
                    writeFile file: filename+'.txt', text: "${it}"
                    }
                }
                }
                }
                zip dir: 'build', exclude: '', glob: '', overwrite: true, zipFile: 'build.zip'
            }
    }
    stage('Test'){
        parallel {
         stage('Quality'){
        stages{
        stage('Static check'){
        when{
            allOf{
                expression { holiday == true }
                expression { env.STATIC_CHECK == "Enable" }
            }
        }
        steps{
               unzip dir: 'Static_check', glob: '*.txt', quiet: true, zipFile: 'build.zip'
        }
    }
    stage('QA'){
        when{
            allOf{
                expression { holiday == true }
                expression { env.QA == "Enable" }
            }
        }
        steps{
                unzip dir: 'QA', glob: '*.txt', quiet: true, zipFile: 'build.zip'
        }
    
    }
    }
    }
       stage('Unit Test'){
        when{
            allOf{
                expression { holiday == true }
                expression { env.Unit_Test == "Enable" }
            }
        }
        steps{
                unzip dir: 'Unit_Test', glob: '*.txt', quiet: true, zipFile: 'build.zip'
        }
    }
        }
    }
    stage('Summary'){
        steps{
            script{
                if(holiday == true){
                print "Build Stage is executed and below files are copied"
                dir('build'){
                    sh 'ls -1'
                }
                }
                if(holiday == true && env.STATIC_CHECK == "Enable"){
                    print "STATIC CHECK Stage is executed and below files are copied"
                    dir('Static_check'){
                        sh 'ls -1'
                    }
                }
                 if(holiday == true && env.QA == "Enable"){
                    print "QA Stage is executed and below files are copied"
                    dir('QA'){
                        sh 'ls -1'
                    }
                }
                 if(holiday == true && env.Unit_Test == "Enable"){
                    print "Unit Test Stage is executed and below files are copied"
                    dir('Unit_Test'){
                        sh 'ls -1'
                    }
                }
            }
        }
    }
    }
     post { 
        always { 
            cleanWs()
        }
        success {
                    emailext body: 'Jenkins Job ${JOB_NAME} executed Successfully', subject: 'Jenkins Success Notification', to: env.Success_Email
        }
        failure {
                    emailext body: 'Jenkins Job ${JOB_NAME} was failed. Please review the Configuration and retrigger the Job', subject: 'Jenkins Failure Notification', to: env.Failure_Email
        }
    }
}
