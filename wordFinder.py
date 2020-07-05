import enchant
# from nltk import everygrams
import itertools as it
from bs4 import BeautifulSoup
import requests
import json
from config import API_KEY_COLLEGIATE, API_KEY_THESAURUS


'''
TO DO: 
- Order words by frequencies, not alphabetically, parse large texts?
- Get definitions for words
- Filter letter inputs for non-letters
- Make upper and lowercase characters equivalent
'''

file = open('dictionary_compact.json', 'r')
# file = open('dict_copy.json', 'r')
data = json.load(file)
file.close()


def words(letters):
    d = enchant.Dict("en_US") # don't use pyenchant?
    letters = letters.lower()
    MAX = len(letters)
    MIN = 3

    final = [[] for _ in range(MAX + 1)]
    count = MAX

    while count >= MIN:
        p = it.permutations(letters, count)
        for w in p:
            s = ''.join(w)
            # if d.check(s) and s not in final[count]:
            if s in data and s not in final[count]:
                final[count].append(s)
        count -= 1

    for sl in final:
        sl.sort()

    final = sorted(list(filter(lambda x: x != [], final)), key=lambda l: len(l[0]), reverse=True)
    return final


def leadingChar(letters, c):
    d = enchant.Dict("en_US")

    full = (letters + c).lower()

    MAX = len(full)
    MIN = 3

    final = [[] for _ in range(MAX + 1)]
    count = MAX
    while count >= MIN:
        p = it.permutations(full, count)
        for w in p:
            s = ''.join(w)
            if (d.check(s)) and s[:len(c)] == c:
                final[count].append(s)
        count -= 1

    final = sorted(list(filter(lambda x: x != [], final)), key=lambda l: len(l[0]), reverse=True)
    return final


def endingChar(letters, c):
    d = enchant.Dict("en_US")

    full = (letters + c).lower()

    MAX = len(full)
    MIN = 3

    final = [[] for _ in range(MAX + 1)]
    count = MAX
    while count >= MIN:
        p = it.permutations(full, count)
        for w in p:
            s = ''.join(w)
            if (d.check(s)) and s[-len(c):] == c:
                final[count].append(s)
        count -= 1

    final = sorted(list(filter(lambda x: x != [], final)), key=lambda l: len(l[0]), reverse=True)
    return final


def addWord(word):
    with open('dict_copy.json', 'r') as f:
        d = json.load(f)
        d[word] = ""
    with open('dict_copy.json', 'w') as f:
        json.dump(d, f)

    updateData()


def updateData():
    f = open('dict_copy.json', 'r')
    global data
    data = json.load(f)
    f.close()


def checkWord(w):

    d = enchant.Dict("en_US")
    return d.check(w)

def definition(w):

    if w in data:
        return data[w]
    else:
        return None

def callAPI(w):

    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{w}?key={API_KEY_COLLEGIATE}'
    r = requests.get(url)


# def words():
#     d = enchant.Dict("en_US")
#
#     while True:
#         inp = input("Enter letters (enter 0 to quit): \n")
#         if inp == '0':
#             break
#         print('...')
#
#         MAX = len(inp)
#         MIN = 2
#
#         final = [[] for _ in range(MAX + 1)]
#         count = MAX
#         while count > MIN:
#             p = it.permutations(inp, count)
#             for w in p:
#                 s = ''.join(w)
#                 if d.check(s):
#                     final[count].append(s)
#             count -= 1
#
#         printFinal(final)
#         print('-------------------------------------')
#
#
# def leadingChar():
#     d = enchant.Dict("en_US")
#     while True:
#         lead = input("Enter the letter the word must start with (enter 0 to quit): \n")
#         if lead == '0' or len(lead) > 1:
#             break
#         inp = input("Enter possible preceding letters (enter 0 to quit): \n")
#         if inp == '0':
#             break
#         full = lead + inp
#
#         MAX = len(full)
#         MIN = 2
#
#         final = [[] for i in range(MAX + 1)]
#         count = MAX
#         while (count > MIN):
#             p = it.permutations(full, count)
#             for w in p:
#                 s = ''.join(w)
#                 if (d.check(s)) and s[0] == lead:
#                     final[count].append(s)
#             count -= 1
#
#         printFinal(final)
#
#
# def endingChar():
#     d = enchant.Dict("en_US")
#     while(True):
#         end = input("Enter the letter the word must end with (enter 0 to quit): \n")
#         if end == '0' or len(end) > 1:
#             break
#         inp = input("Enter possible preceding letters (enter 0 to quit): \n")
#         if inp == '0':
#             break
#         full = inp + end
#
#         MAX = len(full)
#         MIN = 2
#
#         final = [[] for i in range(MAX + 1)]
#         count = MAX
#         while (count > MIN):
#             p = it.permutations(full, count)
#             for w in p:
#                 s = ''.join(w)
#                 if (d.check(s)) and s[-1] == end:
#                     final[count].append(s)
#             count -= 1
#
#         printFinal(final)
#
#
# def printFinal(l):
#     '''
#     print every word, grouped by word length
#     '''
#     n = len(l) - 1
#     ind = -1
#     for i in range(len(l)):
#         if l[ind] != []:
#             print('Words with ' + str(n) + ' letters: ')
#             l[ind].sort()
#             l[ind] = filterDupes(l[ind])
#             s = ''
#             for word in l[ind]:
#                 s = s + word + ', '
#             s = s[:-2]
#             print(s)
#         n -= 1
#         ind -= 1


def filterDupes(l):
    '''
    filter duplicates in a list
    '''
    final = []
    for w in l:
        if w not in final:
            final.append(w)
    return final


def define(s):
    '''
    grab word definitions from dictionary.com
    '''
    url = 'https://www.dictionary.com/browse/' + s
    r = requests.get(url)
    content = BeautifulSoup(r.content, 'html.parser')

    # print(content.prettify())
    # print("\nEND OF HTML CODE!\n" + "\n---------------------------------------------------------------------------\n")

    divs = content.findAll('meta')
    d = divs[1].get('content')
    print(d)
    p = d.split(',')[0] + ': ' + (d.split(',')[1].split(':')[0]).strip()
    print(p.strip())


if __name__ == '__main__':
    print(leadingChar('Ter','wa'))
    pass
