import requests
import sys
import json

if __name__ == '__main__':
    url = "http://localhost:8888/productionplan"
    if(len(sys.argv) < 2):
        print("Please put the file name")
        sys.exit(0)

    print(sys.argv[1])
    filename = sys.argv[1]
    f = open(filename)
    data = json.load(f)
    answer = requests.post(url, json=data)
    out_filename = "answer_" + filename.split('/')[-1]
    out_path = '/'.join(filename.split('/')[:-1]) + "/" + out_filename
    with open(out_path, "w") as outfile:
        outfile.write(answer.text)
    print(answer.text)
