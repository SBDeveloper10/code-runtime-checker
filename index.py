from flask import Flask, render_template, request
import requests
import json
import re
import os
import google.generativeai as genai


app = Flask(__name__)
url = "https://onecompiler-apis.p.rapidapi.com/api/v1/run"

headers = {
	"x-rapidapi-key": "419519b70fmsh7d0fad1f36695a9p14d646jsn3b0b206f3a3c",
	"x-rapidapi-host": "onecompiler-apis.p.rapidapi.com",
	"Content-Type": "application/json"
}

genai.configure(api_key=os.getenv["API_KEY"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convertCode")
def convertCode():
    #     code = '''a = 0
    # for i in range(100000):
    #     a+=1
    #     '''

    code = request.args.get('code')
    from_lang = request.args.get('from_lang')
    to_lang = request.args.get('to_lang')

    finalList = {
        "languagesList": [],
        "executionTimeList": []
    }

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"You are tasked to convert the below {from_lang} code to {','.join(str(i) for i in to_lang)} : \n{code}\nOutput the response in between tags format like <c>#include <stdio.h>...</c>."
    # prompt = f"You are tasked to convert the below python code to c, cpp, javascript : \n{code}\nOutput the response in between tags format like <c>#include <stdio.h>...</c>."
    response = model.generate_content(contents=[prompt], request_options={"timeout": 1000})
    # print(response.text)
    userCode = f'<{from_lang}>{code}</{from_lang}>\n'
    # userCode = f'<python>{code}</python>\n'

    # pattern = r"(?:int\s+main\s*\(\)\s*\{(.*?)\s*return\s+0\s*;)"
    # matches = re.findall(pattern, generatedCode, re.DOTALL)

    c_pattern = r"<(c|cpp)>|(?:int\s+main\s*\(\)\s*\{(.*?)\s*return\s+0\s*;)|<(javascript|python)>\s*(.*?)\s*<\/(javascript|python)>"
    c_matches = re.findall(c_pattern, response.text, re.DOTALL)

    for i in range(len(c_matches)):
        if c_matches[i][0] != '':
            lang = c_matches[i][0]
            userCode += f'<{lang}>{c_matches[i+1][1]}\n</{lang}>\n\n'
        elif c_matches[i][2] != '':
            lang = c_matches[i][2]
            userCode += f'<{lang}>\n{c_matches[i][3]}\n</{lang}>\n'
    
    pattern = r"<(javascript|c|cpp|python)>\s*(.*?)\s*<\/(javascript|c|cpp|python)>"
    matches = re.findall(pattern, userCode, re.DOTALL)

    with open("file-details.json") as file:
        data = file.read()
        obj = json.loads(data)
        languages = obj['languages']
        for match in matches:
            if match[0] in languages.keys():
                lang = languages[match[0]]
                # resultObj = {}
                with open(lang['filename'], 'r') as file:
                    content = file.readlines()
                    langCode = [lang['startwith'] + i for i in match[1].splitlines(keepends=True)]
                    # content.insert(lang['indexAt'], langCode)
                    content[lang['indexAt']:lang['indexAt']] = langCode
                    content = "".join(i for i in content)
                    # print(content)
                    executionTimeData = runCode(match[0], lang['filename'], content)
                    finalList["languagesList"].append(match[0])
                    finalList["executionTimeList"].append(float(executionTimeData['executionTime']))
                    # resultObj['language'] = match[0]
                    # resultObj['executionTime'] = executionTimeData['executionTime']
                    # executionTimeList.append(resultObj)
        file.close()
    print(finalList)
    return finalList


@app.route("/runCode")
def runCode(language, filename, content):
    payload = {
            "language": language,
            "files": [
                {
                    "name": os.path.basename(filename),
                    "content": content
                }
            ]
        }
    
    response = requests.post(url, json=payload, headers=headers)
    # response = {
    #     "stdout": "Hello Peter\n",
    #     "stderr": "null",
    #     "exception": "null",
    #     "executionTime": 41,
    #     "limitPerMonthRemaining": 74694,
    #     "status": "success",
    # }
    data = response.json()
    # print(data)
    if type(data['stdout']) != str:
        # return {'executionTime': 0}
        data['stdout'] = "executionTime=0\n"
    executionTime = data['stdout'].split('executionTime=', 1)[1].replace('\n', '')
    return {'executionTime': executionTime}


if __name__ == "__main__":
    app.run()
