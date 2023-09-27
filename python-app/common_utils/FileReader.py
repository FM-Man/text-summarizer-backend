import os


def read_files():
    total_data = {}
    summary_list = []
    dataset_directory_path = '..\\java-app\\datasets\\Bangla-Text-summarization-Dataset-main'
    documents_list = []

    for indx in range(1,201):
        f = f'{dataset_directory_path}\\Documents\\document_{indx}.txt'
        s1 = f'{dataset_directory_path}\\Summaries\\document_{indx}_summary_1.txt'
        s2 =f'{dataset_directory_path}\\Summaries\\document_{indx}_summary_2.txt'

        if os.path.exists(f):
            with open(f, 'r', encoding="utf8", errors='ignore') as filef:
                file_text = filef.read().split('ext:')[1]
                documents_list.append(file_text)
        else:
            print(f'{f} not found')
        
        if os.path.exists(s1):
            with open(s1, 'r', encoding="utf8", errors='ignore') as files1:
                file_text = files1.read()
                summary_list.append(file_text)
        else:
            print(f'{s1} not found')
        
        if os.path.exists(s2):
            with open(s2, 'r', encoding="utf-16-le", errors='ignore') as files2:
                file_text = files2.read()
                summary_list.append(file_text)
        else:
            print(f'{s2} not found')



    total_data['documents'] = documents_list
    total_data['summary']=summary_list

    return total_data

