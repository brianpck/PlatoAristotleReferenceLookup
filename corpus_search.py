"""
Author: Brian Killackey, 2021-2022
For non-commercial scholarly purposes only.

"""

import re
import csv

from collections import defaultdict

def main():
    include_lines = True 
    line_limit = 100
    author = 'aristotle' # current default
    initialize = True
    
    author_params = {
        'aristotle': {
            'filename': 'tlg0086.csv',
            'paging': 'Bekker',
        },
        'plato': {
            'filename': 'tlg0059.csv',
            'paging': 'Stephanus',
        }    
    }
    
    corpus = []
    plato_page_map = defaultdict(list)
    plato_work = ''

    print("Enter {} number below. Type 'p' to search for Plato. Type 'help' for more options.".format(author_params[author]['paging']))

    while True:
        if initialize:
            user_input = 'a'
            initialize = False
        else:
            user_input = input('\n({})\n>>> '.format(author.title())).lower().replace(' ', '')

        if user_input == 'help': 
            print("""Type 'exit' to exit
    Type 'lines' to toggle line number display
    Type 'limit' to change line limit
    Type 'a' or 'aristotle' to search Aristotle; Type 'p' or 'plato' to search Plato

    The following Bekker formats are supported:
    - 423a1 [one line]
    - 1117a3-5 [multiple lines]
    - 1234b [one column]
    - 414b9-415a1 [multiple lines across pages/columns]
    
    The following Stephanus formats are supported:
    - 13 [whole page]
    - 83b [one section of page]
    - 98a1 [individual line]
    - 436e1-5 [multiple lines]
    - 437b-d [multiple sections]
    - 899d5-900a2 [exact span]""")
            continue
        if user_input == 'exit':
            break
        elif user_input == 'lines':
            include_lines = not include_lines
            print('Lines will{} be displayed'.format([' not', ''][include_lines]))
            continue
        elif user_input == 'limit':
            try:
                line_limit = int(input('New limit limit? Current limit is {}. '.format(line_limit)).strip())
            except ValueError:
                print('You must type an integer!')
            continue
        elif user_input in ('a', 'aristotle'):
            author = 'aristotle'
            corpus = load_corpus(author_params[author]['filename'])
            continue
        elif user_input in ('p', 'plato'):
            author = 'plato'
            plato_work = ''
            corpus = load_corpus(author_params[author]['filename'])
            if len(plato_page_map) < 1:
                for work, page in set(tuple(x[:2]) for x in corpus):
                    plato_page_map[int(page)].append(work)
            
            continue
        if author == 'aristotle':
            aristotle_search(user_input, corpus, line_limit, include_lines)
        elif author == 'plato':
            plato_work = plato_search(user_input, corpus, plato_page_map, plato_work, line_limit, include_lines)
            if plato_work: 
                print('\n({} currently assumed.)'.format(plato_work))
        else:
            print('author not recognized!')
            break
            
def load_corpus(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))

def aristotle_search(user_input, corpus, line_limit=100, include_lines=True):
    bekker_regex = re.search(r'(\d+[ab])(\d+)?(\-(\d+[ab])?(\d+))?', user_input)
    if bekker_regex is None:
        print('Bekker number not recognized')
        return
        
    first_page, first_line, last_page, last_line = bekker_regex.group(1), bekker_regex.group(2), bekker_regex.group(4), bekker_regex.group(5)
    if last_line is None:
        if last_page is None and first_line is None:
            last_line = '50'
        else:
            last_line = first_line
    if first_line is None:
        first_line = '1'

    if last_page is None:
        last_page = first_page

    # print(first_page, first_line, last_page, last_line)
    print()
    
    start_flag = False
    for work, page, orig_line, text in corpus:
        line = int(re.search(r'^([0-9]*)', '0' + orig_line).group())
        if not start_flag:
            if page == first_page and int(first_line) <= line:
                start_flag = True
                lines_left = line_limit
                print(work, user_input)
        if start_flag:
            if (page == last_page and line > int(last_line)) or (page > last_page):
                break
            print(text, '(' + page + orig_line + ')' if (include_lines and (line % 5 == 0 or line == 1)) else '')
            lines_left = lines_left - 1
            if lines_left < 1: 
                print('Line limit ({}) exceeded!'.format(line_limit))
                break
    else:
        print("No matching lines were found.")
        
def plato_search(user_input, corpus, plato_page_map, plato_work, line_limit=100, include_lines=True):
    stephanus_regex = re.search(r'(\d+)([a-e])?(\d+)?(\-((\d+)?([a-e]))?(\d+)?)?', user_input)
    if stephanus_regex is None:
        print('Stephanus number not recognized')
        return plato_work
        
    first_page,first_letter,first_line = stephanus_regex.group(1), stephanus_regex.group(2), stephanus_regex.group(3)
    last_page,last_letter,last_line = stephanus_regex.group(6), stephanus_regex.group(7), stephanus_regex.group(8)
    
    if last_line is None:
        if first_line is not None:
            last_line = first_line
        else:
            last_line = 15
    if first_line is None:
        first_line = 1
    if first_letter is None:
        first_letter = 'a'
        last_letter = 'e'
    if last_page is None:
        last_page = first_page
    if last_letter is None:
        last_letter = first_letter
        
    first_page, first_line, last_page, last_line = int(first_page), int(first_line), int(last_page), int(last_line)

    #print(first_page, first_letter, first_line)
    #print(last_page,last_letter,last_line)
    
    plato_works = plato_page_map[first_page]
    #print(plato_works)
    if len(plato_works) == 1:
        plato_work = plato_works[0]
    while plato_work.lower() not in [x.lower() for x in plato_works]:
        plato_num = input('Which work are you searching? Enter the number and your selection will be remembered until you enter the Stephanus number of a different work. Type "x" to enter different Stephanus number.\n{}\n>>> '.format('\n'.join(str(a+1) + ': ' + b for a, b in enumerate(plato_works))))
        if plato_num == 'x': break
        try:
            plato_work = plato_works[int(plato_num) - 1]
        except (ValueError, IndexError) as e:
            print("Please enter a number between 1 and {}".format(len(plato_works)))
    
    print()
    
    
    start_flag = False
    for work, page, letter, line, text in corpus:
        page, line = int(page), int(line)
        if not start_flag:
            if work == plato_work and page == first_page and letter == first_letter and first_line <= line:
                start_flag = True
                lines_left = line_limit
                print(work, user_input)
        if start_flag:
            if (page > last_page) or (page == last_page and letter > last_letter) or (page == last_page and letter == last_letter and line > last_line) or (work != plato_work):
                break
            print(text, '({}{}{})'.format(page, letter, line) if (include_lines and (line % 5 == 0 or line == 1)) else '')
            lines_left = lines_left - 1
            if lines_left < 1: 
                print('Line limit ({}) exceeded!'.format(line_limit))
                break
    else:
        print("No matching lines were found.")
        
    return plato_work
        
main()
