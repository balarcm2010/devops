pipeline {
    agent any
    environment{
        today = sh(returnStdout:true, script: 'date +%Y-%m-%d').trim()
        currentYear = sh(returnStdout:true, script: 'date +%Y').trim()
        holiday = false
    }
    stages {
        stage('Git Pull') {
            steps {
                echo 'GIT Pull'
            }
        }
        stage('Is the run required?'){
            steps{
                sh 'rm -rf build.json'
                httpRequest outputFile: 'build.json', quiet: true, responseHandle: 'NONE', url: 'https://calendarific.com/api/v2/holidays?&api_key=d20d05ccb411d9ce3b56b654971e17a29b0aa1ed&country=IN&year='+currentYear, wrapAsMultipart: false
                script{
                def jsonData = readJSON(text: readFile("./build.json").trim())
                def dateArray = jsonData.response.holidays.date.iso
               dateArray.each{ date ->
               if("${date}".contains('T')){
                   println today
                   println "${date.split('T')[0]}"
                   if("${today}".equals("${date.split('T')[0]}"))
                   holiday = true
               }else if("${today}".equals("${date}"))
                   holiday = true
               }
               println holiday
                }
            }
        }
        stage('Build'){
            when {
                expression { holiday == true }
            }
            steps{
                
            }
    }
    }
}
