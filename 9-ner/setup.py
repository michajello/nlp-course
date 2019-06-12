import json
from urllib.request import urlopen, Request
import glob
import os
import time
from multiprocessing import Pool

url = "http://ws.clarin-pl.eu/nlprest2/base"


def upload(file):
    with open(file, "rb") as myfile:
        doc = myfile.read()
    return urlopen(Request(url + '/upload/', doc, {'Content-Type': 'binary/octet-stream'})).read().decode("utf-8")

user = "any@email.com"
modeln82= "any2txt|wcrft2|liner2({\"model\":\"n82\"})"
modeltop9 = "any2txt|wcrft2|liner2({\"model\":\"top9\"})"



def r(f):
    out_path = './out_n82/'
    # out_path = './out_top9/'
    fileid = upload(f)
    print(("Processing: " + f))
    data = {'lpmn': modeln82, 'user': user, 'file': fileid}
    data = process(data)
    if data == None:
        return False
    data = data[0]["fileID"]
    content = urlopen(Request(url + '/download' + data)).read().decode('utf-8')
    with open(out_path + os.path.basename(f) + '.ccl', "w", encoding='utf-8') as outfile:
        outfile.write(content)
    return True


def process(data):
    doc = json.dumps(data).encode("utf-8")
    taskid = urlopen(Request(url + '/startTask/', doc, {'Content-Type': 'application/json'})).read().decode("utf-8")
    time.sleep(0.5)
    resp = urlopen(Request(url + '/getStatus/' + taskid))
    data = json.load(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.9)
        resp = urlopen(Request(url + '/getStatus/' + taskid))
        data = json.load(resp)
    if data["status"] == "ERROR":
        print(("Error " + data["value"]))
        return None
    return data["value"]

    in_path = 'bills/*'

    files = glob.glob(in_path)
    with Pool(4) as p:
        print(p.map(r, files))
