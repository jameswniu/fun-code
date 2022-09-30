import os, sys
import re
import string
import glob
import shutil


# function that clean script name for readability
def clean_script_name(content):
    # ----
    # format filename for readability
    # ----
    title = content.replace('_', ' ').capitalize()

    for k, v in abbv.items():
        title = re.sub(r'\b{}\b'.format(k), f'{v}', title)
        title = re.sub(r'\b{}\b'.format(k.capitalize()), f'{v}', title)

    for letter in letter_l:
        title = re.sub(r'\b{}\b'.format(letter), letter.upper(), title)

    return title


header = ('analytics'
          , 'automation'
          , 'cleaning'
          , 'database'
          , 'extraction'
          , 'reporting'
          , 'automation'
          , 'integration'
          , 'modeling'
          , 'OS'
          , 'visualization'
          , 'raw_data'
          , 'output'
          , 'fun-code'
)
abbv = {
    'w': 'with'
    , 'n': 'and'
    , 'linux': 'Linux'
    , 'windows': 'Windows'
    , 'icd': 'ICD'
    , 'icd9': 'ICD-9'
    , 'icd10': 'ICD-10'
    , 'json': 'JSON'
    , 'csv': 'CSV'
    , 'vs': 'vs.'
    , 'api': 'API'
    , 'w9': 'W-9'
    , 'ocr': 'OCR'
    , 'id': 'ID'
    , 'postgresql': 'PostgreSQL'
    , 'asc': 'ASC'
    , 'x12': 'X12'
    , 'nlp': 'NLP'
    , 'scp': 'SCP'
    , 'ssh': 'SSH'
    , 'excel': 'Excel'
    , 'state': 'State'
    , 'npi': 'NPI'
    , 'city': 'City'
    , 'usps': 'USPS'
    , 'datetime': 'DateTime in specified timezone'
    , 'reg': 'Regression'
    , 'knn': 'KNN'
    , 'temp': 'temporary'
    , 'states': 'States'
    , 'barplot': 'Barplot'
    , 'us': 'US'
    , 'nyc': 'NYC'
}

letter_l = list(string.ascii_lowercase)
pwd = os.getcwd()


#----
# grep only relevant files for processing
#----
script_d = {}

for raw in glob.glob('*.*'):
    sep = raw.split('__')

    for head in header:
        for ele in sep:
            if head == ele:
                script_d[raw] = 1

# [print(k) for k in script_d]


for head in header:
    for f in glob.glob(f'{pwd}\{head}\*.*'):
        if '.md' not in f:
            os.remove(f)


readme_d = {}

for script in script_d:
    print(script)
    #----
    # separate category header
    #----
    sep = script.split('__')

    # category to put script into folder
    script_header = sep[:-1]

    # script name to be formatted for readability
    content = sep[-1]
    # print(content)

    #----
    # clean script name for readability
    #----
    title = clean_script_name(content)

    #----
    # put script into folder with path according to header list and name according to content
    #----


    src = rf'{pwd}\{script}'

    for script_head in script_header:
        des = rf'{pwd}\{script_head}\{content}'

        shutil.copy(src, des)

        print('->' + f'...\{script_head}\{content}')

        if 'Config.py' not in title:
            readme_d[f'{script_head}|{title}'] = 1


    print()
    print(title)


    print('-' * 150)


# print(readme_d)
#----
# edit readme files with readable file names
#----
for head in header:
    with open(rf'{pwd}\{head}\README.md', 'w') as fw:
        print('# Scripts for {}'.format(head.capitalize()), file=fw )
        for k in readme_d:
            script_head = k.split('|')[0]
            title = k.split('|')[1]

            if head == script_head:
                print(title + '\n', file=fw)
