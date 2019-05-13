import subprocess
import datetime 
import csv

now = datetime.datetime.now()

def runCommand(commandStr):
    #os.system(commandStr)
    commandOutput =  subprocess.Popen(commandStr, shell=True, stdout=subprocess.PIPE).stdout
    output =  commandOutput.read()
    return output

def readURLList(fileName):
    fHandle = open(fileName,"r")
    urlList = fHandle.readlines()
    return urlList


urlList = readURLList("ServerList.csv")
writeReport = open('CerficateReport.csv','w')
writer = csv.writer(writeReport)

rows = []
rows.append(["URL","Connection Status","Expiry Date","Validity"])

for url in urlList:
    command = "echo | openssl s_client -connect "+url.splitlines()[0]+":443 -servername "+url.splitlines()[0]+" 2>/dev/null | openssl x509 -noout -dates"
    print("\n")
    print("***************************************************************************************")
    print(url.splitlines()[0])
    errorString = ""
    output = ""
    output = runCommand(command)
    expiryDate = output.splitlines()[1].replace("notAfter=","")
    print("\nCertificate expires on : "+ expiryDate +"\n")
    date_time_expiry = datetime.datetime.strptime(expiryDate, '%b %d %H:%M:%S %Y %Z')
    
    connected = ""
    validity = ""
    
    if(date_time_expiry < now):
        validity = "Expired"
        print(validity)
    elif((int(date_time_expiry.strftime("%Y"),10) - int(now.strftime("%Y"),10))==0): 
        if((int(date_time_expiry.strftime("%m"),10) - int(now.strftime("%m"),10))==0):      
            validity = "Expires this month"
            print(validity)     
        else:
            validity = "Expires this year"
            print(validity)
    else : 
        validity = "Valid"
        print(validity)

    output = runCommand("curl https://"+url.splitlines()[0]+"/wwwcheck.html")

    if(output.find("{\"status\":\"OK\",\"result\":\"pong\"}")>-1):
        print("Connected successfully.")
        connected="Connection Successful."
    else:
        print("Connection failed.")
        connected="Connection Failed."
    
    rows.append([url, connected, expiryDate, validity])

print(rows)
writer.writerows(rows)
writeReport.close()