

from whoosh.index import create_in,open_dir
from whoosh.query import Term,compound,And
from whoosh.fields import *
from whoosh.sorting import FieldFacet
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser,FuzzyTermPlugin
import os
import config
index_dir=config.INDEX

if  os.path.exists(index_dir):
    #open a index
    ix= open_dir(index_dir)  
else:
    #create schema, search field stored=True
    schema = Schema(title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                    url=ID(stored=False),
                    author=ID(stored=True),
                    ctype=ID(stored=False),
                    content=TEXT(stored=True, analyzer=ChineseAnalyzer())
                    )
    #create index
    os.mkdir(index_dir)
    ix = create_in(index_dir, schema)

searcher = ix.searcher()

## search keywords
def reference_search(search_str,i=1,article_type='poem'):
    textlist = []
    if len(search_str)==0:return 0,textlist
    if search_str[-1]=='"' and search_str[0]=='"' :
        searchstr=search_str[1:-1]

    parser = QueryParser("content", ix.schema)
    myquery=And([parser.parse("ctype:"+article_type),parser.parse(searchstr)])
    results = searcher.search_page(myquery,i,pagelen=20) #,limit=100

    for hit in results: #highlight hits
        title='<a href="'+hit['url']+'">'+hit['title']+'</a>' if 'url' in hit.keys() else hit['title']
        textlist.append({'title':hit['author'] +' - '+title if 'author' in hit.keys() else title, 'content':hit.highlights("content", top=10)})
    
    #limit max pages to 20
    pages=(len(results)-1)//20+1 if len(results)<400 else 20
    return pages,textlist
