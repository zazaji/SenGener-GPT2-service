import transformers
import json
import torch
from transformers import AutoModelForCausalLM,AutoTokenizer

modelpath='./model/'
print('AutoTokenizer loading...',modelpath)
tokenizer = AutoTokenizer.from_pretrained(modelpath)
model = AutoModelForCausalLM.from_pretrained(modelpath)

def generate_text(text='',length=10, number=3):
    texts= generate_words(model,tokenizer,text,length,number)
    return texts

def generate_words(model,tokenizer,text,max_new_tokens,number):
    inputs = tokenizer(text,return_tensors='pt')
    text_len=inputs['input_ids'].shape[1]
    generation_output = model.generate(**inputs,
                                    return_dict_in_generate=True,
                                    output_scores=True,
                                    max_new_tokens=max_new_tokens,
                                    # max_new_tokens=80,
                                    do_sample=True,
                                    top_p = 0.6,
                                    # num_beams=5,
                                    eos_token_id=50256,
                                    pad_token_id=0,
                                    num_return_sequences = number)
    res=[]
    for idx,sentence in enumerate(generation_output.sequences):
        gened=tokenizer.decode(sentence[text_len:])
        gened=gened.replace(' ','').replace("[CLS]",'').replace("[UNK]",'').replace("[SEP]",'\n')
        res.append(gened)
        
    return res
