from flask import Flask, render_template, request,send_from_directory
import env
import json
import os,sys,csv
from datetime import datetime
from sys import platform
from datetime import date


app = Flask(__name__)
myData = env.header()

# the following should give Service the Query App
DataCashe = []
usrInput = []

# the following should give Service to the Service App
ServiceDataCashe = []
firstCunck = []
secondCunck = []


@app.route("/",methods=['GET','POST'])

def home():
    if platform == "darwin":
        style = 50
    elif platform == "win32":
        style = 18
    elif platform == "linux":
        style = 19

    # 1- response from main home page
    if request.method == 'POST' and request.form.get('Srv') != None:
        return render_template("SrvHome.html",s=style)


    # 2 - respose from service home
    elif request.method == 'POST' and request.form.get('GoingTo')!= None:
        while len(ServiceDataCashe) != 0:
            ServiceDataCashe.pop()
        while len(firstCunck) != 0:
            firstCunck.pop()
        while len(secondCunck) != 0:
            secondCunck.pop()

        if request.form.get('GoingTo') == "":
            b=0
        else:
            b = int(request.form.get('GoingTo'))
        print('check this')
        print(type(b))
        print(request.form.get('GoingTo'))
        print("end test")
        if request.form.get('end') == "":
            a = 0
            print(type(a))
            print("i entered the if")
        else:
            print("i'm in else")
            print(request.form.get('end'))
            # insert how many days After
            a = int(request.form.get('end'))
            a *= -1

        now = datetime.now()
        dt_string = now.strftime("%d %b %y")
        # data_format_str= "%d %b %Y"
        # %y 2 digit year
        # data_format_str= "%d %m %y"
        #in google datetime strptime
        data_format_str= "%d %b %y"
        print(f' this is a - > {a} this is b {b}')
        print(f'see this format: {data_format_str}')
        # print(dt_string)
        dn = datetime.strptime(dt_string, data_format_str)
        print(type(dn))
        print(f'see this format2: {dn}')
        today = date.today()
        #today = datetime.date.today()
        # print(today.strftime("%m/%d/%y"))
        print(today.strftime("%d %m %y"))

        # formatting the year adding 2 digit number        
        #if dn.year > 2001:
        #    dn = dn.replace(year=dn.year-2000)
        CasesGoingToEnd = []
        CasesEnded = []
        # check if i'm in the correct folder after case of donload
        inner_path = 'data'
        Dirname = os.path.join(app.root_path, inner_path)
        print(Dirname)
        os.chdir(Dirname)
        with open('13_03_2023-15_28_59.json', 'r') as f:
            data = json.load(f)
        for sub in data:
            if sub['Valid Until'] != "":
                try:
                   #print(sub['Valid Until'])
                   datetime.strptime(sub['Valid Until'], data_format_str)
                except:
                    print(sub['Valid Until'])
                    print('!!!!!!')
                    #exit(0)
                else:
                    dbDate = datetime.strptime(sub['Valid Until'], data_format_str)
                    test = dn-dbDate
                    if test.days<b and test.days>=0: # days before
                        CasesEnded.append(sub)
                        ServiceDataCashe.append(sub)
                        firstCunck.append(sub)
                    elif test.days>a and test.days<0:
                        CasesGoingToEnd.append(sub)
                        ServiceDataCashe.append(sub)
                        secondCunck.append(sub)
        return render_template("resSrv.html",res = CasesEnded,
                               l1 = len(CasesEnded),
                               res2 = CasesGoingToEnd,
                               l2 = len(CasesGoingToEnd),
                               t= len(CasesGoingToEnd)+len(CasesEnded))
    
    
    # 3 - response from main home page
    elif request.method == 'POST' and request.form.get('Qry')!= None:
        return render_template("QHome.html",titles=myData)
    
    
    # 4 - response from the Qeury home page
    elif request.method == 'POST' and request.form.get('serchName') != None:
        # the following should be a function i'm repeating myself
        inner_path = 'data'
        Dirname = os.path.join(app.root_path, inner_path)
        print(Dirname)
        os.chdir(Dirname)
        with open('13_03_2023-15_28_59.json', 'r') as f:
            ArrOfDic = json.load(f)
        print('search name result: ->')
        print(request.form.get('serchName'))
        print(request.form.get('selName'))
        key = request.form.get('selName')
        match = request.form.get('serchName')
        usrInput.append({"data":[key,match]})
        print(f'this is my user input {usrInput}')
        try:
            filteredData = [d[key] for d in ArrOfDic]
        except:
            return render_template("QHome.html",titles=myData,res="no match")
        Ulist = set(list(map(lambda x: x.upper(),filteredData)))

        if any(match.upper() in s for s in Ulist):
            print("found")
            res2send = []
            for sub in ArrOfDic:
                #for debug
                #print(f'-->{sub[key].upper()}   ===> {match.upper()}')
                if match.upper() in sub[key].upper():
                    res2send.append(sub)
            #print(res2send) # for debug
            DataCashe.append(res2send)
            return render_template("QeuryRes.html",titles=myData,
                                   RowsCount=len(res2send),
                                   category=key,
                                   type=match,
                                   res=res2send)
        else:
            print("look again")
            return render_template("QHome.html",titles=myData,res="no match")


    # 5 - response from service results page
    elif request.method == 'POST' and request.form.get('backFromResSrv') != None:
        print("in main retun from Service results page")
        return render_template("SrvHome.html",s=style)
    
    # 6 - response from query results page
    elif request.method == 'POST' and request.form.get('backHome') != None:
        print("checking state of..")
        # print(DataCache)
        
        print(usrInput)   
        return render_template("QHome.html",titles=myData)

    return render_template("mainHome.html",s=style)


@app.route("/res",methods=['GET','POST'])
def res():
    if platform == "darwin":
        style = 50
    elif platform == "win32":

        style = 18
    elif platform == "linux":
        style = 19

    t = request.form.get('dwnldFromSrv')
    print(f'back home ==> {t}')

    if request.method == 'POST' and request.form.get('dwnldFromQry') != None and usrInput==[] and DataCashe==[]:
        print(request.form.get('dwnldFromQry'))
        print("line 169")
        return render_template("QHome.html",titles=myData,res=169)
    elif request.method == 'POST' and request.form.get('dwnldFromQry') != None:
        print("in download from query")
        #print(DataCashe)  # for debug
        extract = DataCashe.pop()
        allVal = [d.values() for d in extract]
        r = usrInput.pop()
        [[k,v]] = r.values()
        inner_path = 'static/Results'
        Dirname = os.path.join(app.root_path, inner_path)
        print(Dirname)
        os.chdir(Dirname)


        dateVal = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
        print(dateVal)
        csvFileName = f'{k}-{v}-{dateVal}.csv'
        print(csvFileName)
        with open(csvFileName, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(myData)

            writer.writerows(allVal)
        return send_from_directory(directory=Dirname,path=csvFileName,as_attachment=True)
    
    elif request.method == 'POST' and request.form.get('dwnldFromSrv') != None and ServiceDataCashe == []:
        print("line 198")
        return render_template("SrvHome.html",s=style,res=198)

    elif request.method == 'POST' and request.form.get('dwnldFromSrv') != None:
        print("in download from service")
        inner_path = 'static/Results'
        Dirname = os.path.join(app.root_path, inner_path)
        print(Dirname)
        os.chdir(Dirname)
        # dateVal = datetime.now().strftime("%d/%m/%Y-%I:%M")
        dateVal = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
        print(dateVal)
        # csvFileName = f'{k}-{v}-{dateVal}.csv'
        csvFileName = f'{dateVal}.csv'
        print(csvFileName)
        if len(firstCunck) != 0:
            # print(f'check this out ---> {extract}')
            print("in first a append to file")
            allVal = [d.values() for d in firstCunck]
            testHeader = firstCunck[0].keys()
            with open(csvFileName, 'a', newline='') as f:
                # f.write('\n\nthis is new data\n')
                f.write('\nEnded Cases\n')
                writer = csv.writer(f)
                writer.writerow(testHeader)

            with open(csvFileName, 'a', newline='') as f:
                writer = csv.writer(f)
                # writer.writerow(myData)#HEADERS
                writer.writerows(allVal)

        if len(secondCunck) != 0:
            allVal = [d.values() for d in secondCunck]
            testHeader = secondCunck[0].keys()
            print(testHeader)
            # r = usrInput.pop()
            # [[k,v]] = r.values()
            with open(csvFileName, 'a', newline='') as f:
                f.write('\nCases that are going to End\n')
                writer = csv.writer(f)
                writer.writerow(testHeader)
            with open(csvFileName, 'a', newline='') as f:
                writer = csv.writer(f)
                # writer.writerow(myData)#HEADERS
                writer.writerows(allVal)

        return send_from_directory(directory=Dirname,path=csvFileName,as_attachment=True)    
    return render_template("mainHome.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6060) # for production
    #app.run(host='localhost',port=6060,debug=True) # for debug


