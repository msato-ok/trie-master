#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MySubDictionary():
    volume = 0 #現存するDictonary(i.e. ノード)の数
    def __init__(self, prefix, suffixes):
        self.number = MySubDictionary.volume
        MySubDictionary.volume += 1
        self.prefix = prefix
        self.suffixes = []
        for suffix in suffixes:
            if(len(suffix) == 0):
                self.suffixes.append('#')
            else:
                self.suffixes.append(suffix)

    def append(self, suffix):
        if(len(suffix) == 0):
            self.suffixes.append('#')
        else:
            self.suffixes.append(suffix)

    def view_info(self):
        print('Number of sub dictionaries: ' + str(MySubDictionary.volume))
        print('Node ' + str(self.number) + ':')
        print('Vocabulary size: ' + str(len(self.suffixes)))
        print('Prefix: ' + self.prefix)
        print('Vocabulary:')
        for suffix in self.suffixes:
            print(self.prefix + suffix)
        print('')

    def view_terms(self):
        for suffix in self.suffixes:
            if(suffix == '#'):
                print(self.prefix)
            else:
                print(self.prefix + suffix)
        print('')

class MyTrie():
    def __init__(self, vocabulary): #入力は辞書式順序でソート済みであることを想定
        self.sub_dictionaries = [] #各ノード下にある子辞書
        self.table = [] #Trie構築後、ノード間の遷移を可能にするための配列（テーブル）
        max_length = len(max(vocabulary, key=len))
        self.sub_dictionaries.append(MySubDictionary('', vocabulary))
        #根ノード（最大の部分辞書）には入力語彙すべてを格納
        for sub_dictionary in self.sub_dictionaries:
            sub_dictionary.view_info()
            self.table.append({})
            #第iノードからの、a, b, c, ...という文字での遷移先ノードを連想配列で持つ
            #徳永本では通常の配列だが、ここでは分かりやすさのために連想配列とする
            #連想配列でも時間複雑度・計算複雑度ともにオーダは等しいはず…
            indexed_chars = set()
            for suffix in sub_dictionary.suffixes:
                if not suffix[0] in indexed_chars and suffix[0] != '#':
                    indexed_chars.add(suffix[0])
                    #suffixの先頭文字をインデックスする
                    prefix_of_child_dictionary = sub_dictionary.prefix + suffix[0]
                    child_dictionary = MySubDictionary(prefix_of_child_dictionary, [suffix[1:]])
                    self.sub_dictionaries.append(child_dictionary)
                    #いま着目している単語(厳密にはそのsuffix)のみからなる子辞書を作成
                    self.table[sub_dictionary.number][suffix[0]] = child_dictionary.number
                    #いま作った子辞書に対応するノード番号を、
                    #ノードiからsuffix[0]で遷移した先のノード番号として格納
                elif suffix[0] in indexed_chars:
                    #suffix[0]がインデックス済の場合
                    number_of_child_dictionary = self.table[sub_dictionary.number][suffix[0]]
                    child_dictionary = self.sub_dictionaries[number_of_child_dictionary]
                    child_dictionary.append(suffix[1:])
                #suffix[0] == '#'のときはそのノード自身が単語を表す。新規ノード不要

    def common_prefix_search(self, query):
        present_node = 0 #Trieの根ノードから探索開始
        for alphabet in query:
            if alphabet in self.table[present_node]:
                present_node = self.table[present_node][alphabet]
            else:
                print('The result for query \'' + query + '\' was not found.')
                return
        #for文を抜けているので、検索結果が存在
        print('The result for query \'' + query + '\' is:')
        self.sub_dictionaries[present_node].view_terms()

vocabulary = ['age', 'agile', 'alias', 'all', 'alt', 'altus'] #語彙

dictionary = MyTrie(vocabulary)

dictionary.common_prefix_search('altus')
dictionary.common_prefix_search('alt')
dictionary.common_prefix_search('ag')
dictionary.common_prefix_search('alpaca')