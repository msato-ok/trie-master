#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue

class MySubDictionary():
    volume = 0 #現存するDictonary(i.e. ノード)の数
    def __init__(self, number, prefix, suffixes):
        MySubDictionary.volume += 1
        self.number = number
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
    def __init__(self, lower_bound, upper_bound, vocabulary): #入力は辞書式順序でソート済みであることを想定
        self.origin = lower_bound - 1
        width = upper_bound - self.origin
        self.sub_dictionaries = {} #各ノード下にある子辞書
        self.base = {} #対応ノードの「ずらした量」を記憶させるcheck配列
        self.check = {} #各ノードの「親」を記憶させるbase配列
        max_length = len(max(vocabulary, key=len))
        self.sub_dictionaries[0] = MySubDictionary(0, '', vocabulary)
        #根ノード（最大の部分辞書）には入力語彙すべてを格納
        nodes_to_be_explored = Queue.Queue()
        #未探索ノードの集合queueで持つ（幅優先での構築。深さ優先ならstackを使う）
        nodes_to_be_explored.put(0)
        #根ノードから探索開始
        while True:
            node = nodes_to_be_explored.get()
            sub_dictionary = self.sub_dictionaries[node]
            sub_dictionary.view_info()
            pre_indexed_chars = set()
            for suffix in sub_dictionary.suffixes:
                if not suffix[0] in pre_indexed_chars and suffix[0] != '#':
                    pre_indexed_chars.add(suffix[0])
            candidate_for_base = 0
            while True:
                acceptable = True
                for char in pre_indexed_chars:
                    if (candidate_for_base + ord(char) - self.origin) in self.check.keys():
                        #check[i + ord(char) - self.origin]にすでに親が格納されていればその列は使えない
                        acceptable = False
                        break
                if(acceptable):
                    #base[node]として使える値が見つかった
                    break
                candidate_for_base += 1
            self.base[node] = candidate_for_base
            #base[node]に値を格納

            indexed_chars = set()
            for suffix in sub_dictionary.suffixes:
                if not suffix[0] in indexed_chars and suffix[0] != '#':
                    indexed_chars.add(suffix[0])
                    #suffixの先頭文字をインデックスする
                    prefix_of_child_dictionary = sub_dictionary.prefix + suffix[0]
                    column_of_child_dictionary = self.base[node] + (ord(suffix[0]) - self.origin)
                    nodes_to_be_explored.put(column_of_child_dictionary)
                    child_dictionary = MySubDictionary(column_of_child_dictionary, \
                        prefix_of_child_dictionary, [suffix[1:]])
                    self.sub_dictionaries[column_of_child_dictionary] = child_dictionary
                    #いま着目している単語(厳密にはそのsuffix)のみからなる子辞書を作成
                    self.check[column_of_child_dictionary] = node
                    #子辞書のノード番号をcheck配列に格納
                elif suffix[0] in indexed_chars:
                    #suffix[0]がインデックス済の場合
                    column_of_child_dictionary = self.base[node] + (ord(suffix[0]) - self.origin)
                    child_dictionary = self.sub_dictionaries[column_of_child_dictionary]
                    child_dictionary.append(suffix[1:])
                #suffix[0] == '#'のときはそのノード自身が単語を表す。新規ノード不要

            if nodes_to_be_explored.empty():
                break

    def common_prefix_search(self, query):
        present_node = 0 #Trieの根ノードから探索開始
        for alphabet in query:
            if not self.base[present_node] + (ord(alphabet) - self.origin) in self.check:
                #該当列のcheckの値が存在しない
                print('The result for query \'' + query + '\' was not found.')
                return
            elif self.check[self.base[present_node] + (ord(alphabet) - self.origin)] != present_node:
                #該当列のcheckの値が現在のノードと一致しない
                print('The result for query \'' + query + '\' was not found.')
                return
            else:
                present_node = self.base[present_node] + (ord(alphabet) - self.origin)
        #for文を抜けているので、検索結果が存在
        print('The result for query \'' + query + '\' is:')
        self.sub_dictionaries[present_node].view_terms()

vocabulary = ['age', 'agile', 'alias', 'all', 'alt', 'altus'] #語彙

dictionary = MyTrie(ord('a'), ord('z'), vocabulary)

dictionary.common_prefix_search('altus')
dictionary.common_prefix_search('alt')
dictionary.common_prefix_search('ag')
dictionary.common_prefix_search('alpaca')