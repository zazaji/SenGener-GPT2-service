from flask import Flask, abort, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from flask_cache import Cache
import re
import wsearch
from jieba import analyse
import time
import requests, json
from run_generation import generate_text
from config import MODELPATH


TextRank
textrank = analyse.textrank


app = Flask(__name__)   
cors = CORS(app)
CORS(app, resources=r'/*')
cache = Cache()
cache.init_app(app,config={
    "CACHE_TYPE":"simple"  ##有很多可以选择
})
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route("/func", methods=['get'])
def func():
    res=MODELPATH.keys()
    dic={}
    for d in res:
        dic[d]=d 
    print(dic)
    return jsonify(dic)

#全文检索
@app.route("/refer", methods=['POST'])
def refer():
    data = request.get_json()
    keywords=data['context']
    article_type=data['article_type']
    pagei=data['page']
    page,ref= wsearch.reference_search(keywords,pagei,article_type)
    if len(ref)==0:ref=[{'title':'没有找到匹配内容','content':'...'}]
    return jsonify({'ref':ref,'page':page,'pagei':pagei})

def request_welm(text,we_token,number):
    post_data={
        "prompt":text,
        "model":"xl",
        "max_tokens":50,
        "temperature":0.0,
        "top_p":0.95,
        "top_k":40,
        "n":number,
        "echo":False,
        "stop":",，.。"
    }
    headers = {'Authorization': 'Bearer '+we_token, 'Content-Type': 'application/json'}
    r = requests.post('https://welm.weixin.qq.com/v1/completions', headers=headers, data=json.dumps(post_data))
    print(text,r.json())
    if r.json()['choices'][0]['finish_reason']!='finished':
        return [{'text': '[!error]'}]
    return r.json()['choices']


@app.route("/generate", methods=['POST'])
@cross_origin()
def get_gen():
    data = request.get_json()
    if 'context' not in data or len(data['context'].strip()) == 0:
        return jsonify({'sentences':[],'ref':[{'title':'没有信息输入','content':'...'}],'page':0,'keywords':'--'})
    else:
        res,ref,page,keywords = gen(data)
        print(res)
        return jsonify({'sentences': res,'ref':ref,'page':page,'keywords':' '.join(keywords)})
        
def gen(data):
    results=[]
    article_type=data['article_type']
    is_index=data['is_index']
    token=data['token']
    text = data['context'].strip()[-500:]
    ref=""
    keywords=''
    page=0
    if is_index:
        #检索结果
        keywords = textrank(re.sub('[^\u4e00-\u9fa5]+','',text)[-10:])[:2]
        page,ref= wsearch.reference_search(' '.join(keywords),i=1,article_type=article_type)            
    if len(ref)==0:page,ref=0,[{'title':'没有找到匹配内容','content':'...'}]
    if article_type=='welm':
        results=request_welm(text,token,data['number'])
        results=[{'value':result.text} for result in results]
        return results,ref,page,keywords

    else:
        seed=100
        temperature=0.9
        top_k=60
        try:
            result = generate_text(length=40,  text=text, temperature=temperature,
                top_k=top_k,  seed=seed,  article_type=article_type, number=data['number'] )
        except Exception as e:
            print(e)
            result=[str(e)]

        results+=result
    res=[{'value':r} for r in set(results)]
    return res,ref,page,keywords
