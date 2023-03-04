from flask import Flask, render_template, request,send_from_directory
import env
import json
import os,sys,csv
from datetime import datetime


app = Flask(__name__)
myData = env.header()

DataCache = []
usrInput = []

@app.route("/",methods=['GET','POST'])
def home():
    os.chdir(app.root_path)
    f = open('data.json', encoding='utf-8')
    ArrOfDic = json.load(f)
    print(type(ArrOfDic))
    if request.method == 'POST' and request.form.get('serchName') != None:
        print(request.form.get('serchName'))
        print(request.form.get('selName'))
        key = request.form.get('selName')
        match = request.form.get('serchName')
        usrInput.append({"data":[key,match]})
        print(f'this is my user input {usrInput}')
        try:
            filteredData = [d[key] for d in ArrOfDic]
        except:
            return render_template("home.html",titles=myData,res="no match")
        Ulist = set(list(map(lambda x: x.upper(),filteredData)))
        # print(Ulist)
        # in the following i send a set of the filter
        # not going over duplicate cases
        if any(match.upper() in s for s in Ulist):
            print("found")
            #python filter dict in list with value of key
            #python get all dict in list with value matching key
            # res2send = [ sub[match.upper()] for sub in ArrOfDic ]
            res2send = []
            for sub in ArrOfDic:
                # print(f'-->{sub}')
                print(f'-->{sub[key].upper()}   ===> {match.upper()}')
                if match.upper() in sub[key].upper():
                    res2send.append(sub)
            # res2send = list(filter(lambda d: d[key] in match, ArrOfDic))
            print(res2send)
            DataCache.append(res2send)
            # render_template( to results page)
            return render_template("res.html",titles=myData,
                                   RowsCount=len(res2send),
                                   category=key,
                                   type=match,
                                   res=res2send)
        else:
            print("look again")
            # send to the user a string or alert that 
            # there was no match for him and he should
            # sbmit again
            return render_template("home.html",titles=myData,res="no match")
    elif request.method == 'POST' and request.form.get('backHome') != None:
        print("checking state of..")
        print(DataCache)
        print(usrInput)   
        return render_template("home.html",titles=myData)
    return render_template("home.html",titles=myData)


@app.route("/res",methods=['GET','POST'])
def res():
    t = request.form.get('backHome')
    print(f'back home ==> {t}')
    if request.method == 'POST' and request.form.get('dwnld') != None:
        print("in results")
        extract = DataCache.pop()
        allVal = [d.values() for d in extract]
        r = usrInput.pop()
        [[k,v]] = r.values()
        inner_path = 'static'
        Dirname = os.path.join(app.root_path, inner_path)
        print(Dirname)
        os.chdir(Dirname)


        # dateVal = datetime.now().strftime("%d/%m/%Y-%I:%M")
        dateVal = datetime.now().strftime("%d_%m_%Y-%H_%M")
        print(dateVal)
        csvFileName = f'{k}-{v}-{dateVal}.csv'
        print(csvFileName)
        with open(csvFileName, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(myData)

            writer.writerows(allVal)
        return send_from_directory(directory=Dirname,path=csvFileName,as_attachment=True)
    render_template("home.html",titles=myData)

if __name__ == "__main__":
    #app.run(host='localhost',port=7070,debug=True) # for debug
    app.run(host='0.0.0.0',port=7070) # for production
