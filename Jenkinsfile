pipeline {
    agent any
    environment{
        //Getting Current Date using Linux date command
        //today = sh(returnStdout:true, script: 'date +%Y-%m-%d').trim()
        today = '2021-01-01'
        //Getting Current year using Linux date command
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
                //using httprequest plugin to hit the http url with dynamic year and saving the response in build.json file
                httpRequest outputFile: 'build.json', quiet: true, responseHandle: 'NONE', url: 'https://calendarific.com/api/v2/holidays?&api_key=d20d05ccb411d9ce3b56b654971e17a29b0aa1ed&country=IN&year='+currentYear, wrapAsMultipart: false
                script{
                    //reading Json file and storing them in a variable
                jsonData = readJSON(text: readFile("./build.json").trim())
                    //fetching array of dates from Json Output
                def dateArray = jsonData.response.holidays.date.iso
                    //Iterating through list of dates to match each date with current date
               dateArray.each{ date ->
                   //Checking if date contains Timestamp along with date
               if("${date}".contains('T')){
                   //Removing timestamp if it is part of date
                   if("${today}".equals("${date.split('T')[0]}"))
                   //If current date equals an element in date array then today is considered as holiday
                   holiday = true
               }else if("${today}".equals("${date}"))
                   holiday = true
               }
                }
            }
        }
        stage('Build'){
            when {
                //Checking whether today is holiday or not
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
                        //Writing particular Json Object into a file based on the name
                    if(it.name.equals(name))
                    writeFile file: filename+'.txt', text: "${it}"
                    }
                }
                }
                }
                //Creating Zip file with text files created
                zip dir: 'build', exclude: '', glob: '', overwrite: true, zipFile: 'build.zip'
            }
    }
    stage('Test'){
        parallel {
         stage('Quality'){
        stages{
        stage('Static check'){
        when{
            //Checking if today is a holiday or not and whether STATIC_CHECK is selected or not
            allOf{
                expression { holiday == true }
                expression { env.STATIC_CHECK == "Enable" }
            }
        }
        steps{
            //Unzipping build.zip into Static_check folder
               unzip dir: 'Static_check', glob: '*.txt', quiet: true, zipFile: 'build.zip'
        }
    }
    stage('QA'){
        when{
            //Checking if today is a holiday or not and whether QA is selected or not
            allOf{
                expression { holiday == true }
                expression { env.QA == "Enable" }
            }
        }
        steps{
            //Unzipping build.zip into QA folder
                unzip dir: 'QA', glob: '*.txt', quiet: true, zipFile: 'build.zip'
        }
    
    }
    }
    }
       stage('Unit Test'){
        when{
            //Checking if today is a holiday or not and whether Unit_Test is selected or not
            allOf{
                expression { holiday == true }
                expression { env.Unit_Test == "Enable" }
            }
        }
        steps{
            //Unzipping build.zip into Unit_Test folder
                unzip dir: 'Unit_Test', glob: '*.txt', quiet: true, zipFile: 'build.zip'
        }
    }
        }
    }
    stage('Summary'){
        steps{
            script{
                //Printing the stages which got executed and the files which got copied into specific folder
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
            //Clearing out the workspace at the end of the pipeline
            cleanWs()
         } 
        success {
            //Sends email if the result of pipeline is succcesful
                    emailext body: 'Jenkins Job ${JOB_NAME} executed Successfully', subject: 'Jenkins Success Notification', to: env.Success_Email
        }
        failure {
            //Sends email if the pipeline breaks
                    emailext body: 'Jenkins Job ${JOB_NAME} was failed. Please review the Configuration and retrigger the Job', subject: 'Jenkins Failure Notification', to: env.Failure_Email
        }
    }
}
