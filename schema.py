import ARgorithmToolkit
import yaml
import sys
from os import listdir
from os.path import join

def get_files():
    mypath = 'schemas'
    onlyfiles = [join(mypath,x) for x in listdir("schemas") if x[-3:]=='yml' and x!='general_schema.yml']
    return onlyfiles

def get_schema(x):
    with open(x, 'r') as stream:
        try:
            schema = yaml.safe_load(stream)
            return schema
        except yaml.YAMLError as exc:
            print(exc)

def is_present(loc):
    keywords = loc.split('.')[1:]
    model = ARgorithmToolkit
    try:
        for word in keywords:
            model = getattr(model,word)
    except:
        return False
    return True

def check_schema(x):
    required_tags = ['date', 'category', 'author', 'states', 'functions']
    schema = get_schema(x)
    for r in required_tags:
        if r not in schema.keys():
            return "error"
    status = {
        "class" : {},
        "functions" : {}
    }
    classflag ='class' in schema
    if classflag:
        for c in schema['class']:
            loc = list(c.keys())[0]
            status['class'][loc] = "present" if is_present(loc) else "error"
    for f in schema['functions']:
        func_name = list(f.keys())[0]
        function = f[func_name]['function']
        if function == 'None' :
            status['functions'][func_name] = "absent"
        else:
            loc = function['name']
            status['functions'][func_name] = "present" if is_present(loc) else "error"
    return status

def flatten_dict(dd, separator ='_', prefix =''): 
    return { prefix + separator + k if prefix else k : v 
             for kk, vv in dd.items() 
             for k, v in flatten_dict(vv, separator, kk).items() 
             } if isinstance(dd, dict) else { prefix : dd } 

if __name__ == "__main__":
    files = get_files()
    status = {}
    for x in files:
        status[x] = check_schema(x)
    flat_status = flatten_dict(status,separator="/")
    count = {
        "total" : 0,
        "present" : [],
        "absent" : [],
        "error" : []
    }
    for f in flat_status:
        count["total"] += 1
        count[flat_status[f]].append(f)
    
    argument = sys.argv[1] if len(sys.argv) > 1 else None
    present = len(count['present'])
    absent = len(count['absent'])
    color = "00FFEE"
    tag = "All verified"
    if count["total"] == present:
        color = "2FE817"
    elif count['total'] == present+absent:
        color = "CAC235"
        pc = present/total * 100
        tag = f"{pc:.2f}%"
    else:
        color = "ED1B12"
        tag = "ERROR"
    if argument == "--color":
        print(color)
    elif argument == "--tag":
        print(tag)
    else:
        if tag=="ERROR":
            [print("ERROR : " , x) for x in count['error']]
        elif tag!="All verified":
            [print("ABSENT : ",x) for x in count['absent']]
        else:
            print(tag)
    