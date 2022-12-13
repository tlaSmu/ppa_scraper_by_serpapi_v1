import csv
from serpapi import GoogleSearch


def write_data(filename, res_data):
    with open(f'{filename}', 'a', encoding='utf-8') as res_file:
        res_file.write(res_data)

def clear_file(filename):
    with open(f"{filename}",'w') as f:
        pass


def get_list_of_paa_google(keyword, cluster_name, UNIQUE_QUESTIONS,api_key):
    params = {
        "q": keyword,
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    }
    search = GoogleSearch(params)
    
    try:
        results = search.get_dict()
        related_questions = results["related_questions"]

        for res in related_questions:
            question = res['question']
            if question in UNIQUE_QUESTIONS:
                continue
            UNIQUE_QUESTIONS.append(question)

            snippet = res['snippet']
            data = f"\"google\",\"{cluster_name}\",\"{keyword}\",\"{question}\",\"{snippet}\"\n"
            write_data('result.csv', data)

            try:
                next_page_token = res['next_page_token']
                get_paa_from_next_page(keyword, cluster_name, next_page_token, UNIQUE_QUESTIONS)
            except KeyError:
                print('null')

        return related_questions
    except KeyError:
        print(keyword+' -- Google is null')


def get_paa_from_next_page(keyword, cluster_name, next_page_token, UNIQUE_QUESTIONS,):
    params = {
    "engine": "google_related_questions",
    "next_page_token": next_page_token,
    "api_key": api_key
    }
    search = GoogleSearch(params)
    
    try:
        results = search.get_dict()
        related_questions = results["related_questions"]

        for res in related_questions:
            question = res['question']
            if question in UNIQUE_QUESTIONS:
                continue
            UNIQUE_QUESTIONS.append(question)

            snippet = res['snippet']
            data = f"\"google\",\"{cluster_name}\",\"{keyword}\",\"{question}\",\"{snippet}\"\n"
            write_data('result.csv', data)

        return related_questions
    except KeyError:
        print(keyword+' -- Google is null')


def get_list_of_paa_bing_or_yahoo(keyword, cluster_name, search_engine, UNIQUE_QUESTIONS, api_key):
    params = {
    "engine": search_engine,
    "q": keyword,
    "api_key": api_key
    }
    search = GoogleSearch(params)
    
    try:
        results = search.get_dict()
        related_questions = results["related_questions"]

        for res in related_questions:
            question = res['question']
            if question in UNIQUE_QUESTIONS:
                continue
            UNIQUE_QUESTIONS.append(question)

            snippet = res['snippet']
            data = f"\"{search_engine}\",\"{cluster_name}\",\"{keyword}\",\"{question}\",\"{snippet}\"\n"
            write_data('result.csv', data)

        return related_questions

    except KeyError:
        print(keyword+' -- '+search_engine+' is null')
    

# main
data = f"\"se\",\"cluster_name\",\"keyword\",\"question\",\"snippet\"\n"
write_data('result.csv', data)
api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

with open('cluster.csv', mode='r') as infile:
    reader = csv.reader(infile)
    uni_cluster = []      # for
    for row in reader:
        cluster_name = row[0]
        keyword = row[1]

        # for
        if cluster_name in uni_cluster:
            pass
        else:
            uni_cluster.append(cluster_name)
            UNIQUE_QUESTIONS = [] # for

        print('=================')
        print('START >>  '+cluster_name)

        
        len_UNIQUE_QUESTIONS = len(UNIQUE_QUESTIONS)
        print('LEN = '+str(len_UNIQUE_QUESTIONS))
        if len(UNIQUE_QUESTIONS) > 30:
            continue
        else:
            get_list_of_paa_google(keyword, cluster_name, UNIQUE_QUESTIONS, api_key)
        
        len_UNIQUE_QUESTIONS = len(UNIQUE_QUESTIONS)
        print('LEN = '+str(len_UNIQUE_QUESTIONS))
        if len(UNIQUE_QUESTIONS) > 30:
            continue
        else:
            get_list_of_paa_bing_or_yahoo(keyword, cluster_name, 'bing', UNIQUE_QUESTIONS, api_key)

        len_UNIQUE_QUESTIONS = len(UNIQUE_QUESTIONS)
        print('LEN = '+str(len_UNIQUE_QUESTIONS))
        if len(UNIQUE_QUESTIONS) > 30:
            continue
        else:
            get_list_of_paa_bing_or_yahoo(keyword, cluster_name, 'yahoo', UNIQUE_QUESTIONS, api_key)
        
print(' == DONE ==')