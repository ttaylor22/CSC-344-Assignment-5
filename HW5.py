import gzip
import os
import re
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Read in the files to parse
src = "C:\\Users\\dt817\\Desktop\\SUNY Oswego Spring 2017\\CSC 344\\assignments\\"
file1 = open(src + "HW1.c",'r')
file2 = open(src + "core.clj",'r')
file3 = open(src + "Lib.hs",'r')
file4 = open(src + "prolog.txt",'r')
files = [file1,file2,file3,file4]
filesstr = [src + "HW1.c",src + "core.clj",src + "Lib.hs",src + "prolog.txt"]
outfile = open(src + "symbols.txt",'w')
outfilestr = src + "out.txt"

# Parse each file by line and write out to text file
for file in files:
    fname2 = re.split("\\\\", file.name)
    fname = fname2[fname2.__len__()-1]
    outfile.write('\n')
    outfile.write("=======" + fname2[fname2.__len__()-1] + "=======")
    outfile.write('\n')

    for line in file:
        towrite = fname2[fname2.__len__()-1] + ": "
        ln = line
        if re.search("::", ln, re.I) is not None and fname == "Lib.hs":
            firstSplit = re.split("::", ln)[0]
            secondSplit = re.split(' ', firstSplit)
            towrite = towrite + secondSplit[secondSplit.__len__()-2].rstrip()
            outfile.write(towrite)
            outfile.write('\n')
        if re.search("let", ln, re.I) is not None and fname == "Lib.hs":
            firstSplit = re.split("let",ln)[1]
            secondSplit = re.split(' ',firstSplit)
            if secondSplit.__contains__("(Right"):
                towrite = towrite + secondSplit[2].replace(")","").rstrip()
            else:
                towrite = towrite + secondSplit[1].rstrip()
            outfile.write(towrite)
            outfile.write('\n')

        if re.search("struct", ln) is not None and fname == "HW1.c":
            firstSplit = ln.split("struct")[1]
            secondSplit = firstSplit.split(' ')[2].replace("*","").replace(";","").rstrip()
            if re.search('[a-zA-Z]', secondSplit):
                towrite = towrite + secondSplit
            else:
                towrite = towrite + firstSplit.split(' ')[1].replace("*","").replace(";","").rstrip()
            outfile.write(towrite)
            outfile.write('\n')
        if (re.search("char ", ln) is not None) and (fname == "HW1.c"):
            firstSplit = ln.split("char ")[1]
            secondSplit = firstSplit.split(' ')
            towrite = towrite + secondSplit[0].replace("*", "").replace(";", "").replace("(","").rstrip()
            outfile.write(towrite)
            outfile.write('\n')
        if re.search("int ", ln) is not None and fname == "HW1.c":
            firstSplit = ln.split("int ")[1]
            towrite = towrite + firstSplit.split(' ')[0].replace("*", "").replace(";", "").replace("(","").rstrip()
            outfile.write(towrite)
            outfile.write('\n')
        if re.search("DIR", ln) is not None and fname == "HW1.c":
            firstSplit = ln.split("DIR")[1]
            towrite = towrite + firstSplit.split(' ')[1].replace("*", "").replace(";", "").rstrip()
            outfile.write(towrite)
            outfile.write('\n')

        if re.search("defn", ln, re.I) is not None:
            towrite = towrite + re.split(' ', ln)[1].rstrip()
            outfile.write(towrite)
            outfile.write('\n')
        if re.search("def ", ln, re.I) is not None:
            firstSplit = re.split("def", ln)[1]
            secondSplit = re.split(' ', firstSplit)[1]
            if secondSplit.__contains__(")"):
                towrite = towrite + re.split(' ', firstSplit)[1].replace(")","").rstrip()
            else:
                towrite = towrite + re.split(' ', firstSplit)[1].rstrip()
            outfile.write(towrite)
            outfile.write('\n')

        if re.search(":-", ln) is not None:
            firstSplit = ln.split("(")[0]
            if not firstSplit.__contains__(":-"):
                towrite1 = towrite + firstSplit
                outfile.write(towrite1)
                outfile.write('\n')
                firstSplit = ln.split("(")[1:firstSplit.__len__()-1]
                for ele in firstSplit:
                    secondSplit = ele.split(",")
                    for element in secondSplit:
                        if re.search('[a-zA-Z]', element):
                            towrite2 = towrite + element.replace(")","").replace(":-","").replace("[","").replace("]","").replace("_","").replace("|","").rstrip().lstrip()
                            outfile.write(towrite2)
                            outfile.write('\n')


# Create html file
f = open('CSC344HW5.html', 'w')
message = """<html>
<head></head>
<body><p>CSC344 HW5</p></body>
<a href="https://csc344bt.000webhostapp.com/HW1.c">HW1</a>
<a href="https://csc344bt.000webhostapp.com/core.clj">HW2</a>
<a href="https://csc344bt.000webhostapp.com/Lib.hs">HW3</a>
<a href="https://csc344bt.000webhostapp.com/prolog.txt">HW4</a>
<a href="https://csc344bt.000webhostapp.com/symbols.txt">Symbols</a>
</html>"""
f.write(message)
f.close()


# Zip files contained in hw directory
outzip = zipfile.ZipFile(src + "outzip.zip","w")
workingpath = os.getcwd()
os.chdir(src)
for file in files:
    fname2 = re.split("\\\\", file.name)
    fname = fname2[fname2.__len__() - 1]
    outzip.write(fname)
outfilestr = re.split("\\\\", outfile.name)
outfilestr = outfilestr[fname2.__len__() - 1]
outzip.write(outfilestr)
outzip.write("CSC344HW5.html")
outzip.close()


# Prompt user for email address
email = input("Enter email address: ")


# Create email message
msg = MIMEMultipart()
msg['From'] = "ttaylor6@oswego.edu"
msg['To'] = email
msg['Subject'] = "CSC344 HW5"
msg.attach(MIMEText("Hello, Have a good day!"))

# Open zip file and attach it to the message
myzip = open('outzip.zip','rb')
toattach = MIMEBase('application', 'zip')
toattach.set_payload(myzip.read())
encoders.encode_base64(toattach)
toattach['Content-Disposition'] = 'attachment; filename = outzip.zip'
msg.attach(toattach)


# Send the email to the user provided email address
server = smtplib.SMTP()
server.connect('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()
server.login('ttaylor6@oswego.edu','Enter Password Here')
server.sendmail("ttaylor6@oswego.edu",email,msg.as_string())
server.quit()

os.chdir(workingpath)

