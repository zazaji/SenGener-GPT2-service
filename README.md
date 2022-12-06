## SenGener-GPT2-service
A data service support to SenGener, a GPT2 text-generation Plugin of Obsidian.
This is just a sample service. 

It provides 3 protocol:
### `/func`  which models is valid.

- method: get 
- response:
```json
{
	"poem": "poem", 
	 "english": "english"
 }
```

###  `/generate`  main protocol
- method: post
- post:
```json
{
    "article_type": "poem",
    "context": "和风鸟语噪，",
    "is_index": true,
    "max_length": 10,
    "max_time": 1.2,
    "model_size": "distilgpt2/small",
    "number": 3,
    "temperature": 1,
    "token": "123456789a"
    "top_p": 0.9
}
```
- response:
```json
{"keywords":"",
 "page":0,
 "ref":[
		 {
			 "content":""深山闻<b class=\"match term0\">鸟语</b>",
			 "title":"佚名"
		 }
	 ],
 "sentences":[
		 {"value":"落日彩云斜"},
		 {"value":"林影意踌躇"}
	 ]
 }
```


###  `/refer`  full-text search
- method: post
- post:
```json
{
    "article_type": "poem",
    "context": "鸟语",
    "page": 1
}
```
- response:
```json
{
    "pagei": 1,
    "page":11,
    "ref":[
	    {
		    "content": "深山闻<b class=\"match term0\">鸟语</b>",
		    "title":"佚名"
	    }
    ]
}
```

