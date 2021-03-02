#!/usr/bin/env python3
# coding: utf-8
# states: {'B': 0, 'S': 0, 'M': 0, 'E': 0}
# observes: words
class HmmTrain:
    def __init__(self):
        self.line_index = -1    #训练语料的行号
        self.char_set = set()   #训练语料中的字集

    def init(self):  # 初始化字典
        trans_dict = {}  # 隐藏状态转移概率
                            # {'B': {'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0},
                            #  'S': {'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0},
                            #  'M': {'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0},
                            # ...}
        emit_dict = {}  # 发射概率(状态->词语的条件概率),{'B':{ }, 'S': { }, 'M': {}, 'E': { }}
        Count_dict = {}  # 各状态出现次数，用于归一化, {'B': 0, 'S': 0, 'M': 0, 'E': 0}
        start_dict = {}  # 存储状态的初始（首字状态）概率，{'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0}
        state_list = ['B', 'M', 'E', 'S']  # 状态序列
        
        for state in state_list:
            trans_dict[state] = {}
            for s in state_list:
                trans_dict[state][s] = 0.0
        for state in state_list:
            start_dict[state] = 0.0  #{'B': 0.0, 'S': 0.0, 'M': 0.0, 'E': 0.0}
            emit_dict[state] = {}    #{'B': {}, 'S': {}, 'M': {}, 'E': {}}
            Count_dict[state] = 0    # {'B': 0, 'S': 0, 'M': 0, 'E': 0}
        return trans_dict, emit_dict, start_dict, Count_dict

    #保存模型
    def save_model(self, word_dict, model_path):
        f = open(model_path, 'w')
        f.write(str(word_dict))
        f.close()

    # (词语,状态)=>(word, word_status) => 科威特 ['B', 'M', 'E']
    def get_word_status(self, word):  # 根据词语word，输出词语SBME状态列表
        #S:单字词, B:词的开头, M:词的中间, E:词的末尾
        #能 ['S'], 前往 ['B', 'E'],科威特 ['B', 'M', 'E']
        word_status = []
        if len(word) == 1:
            word_status.append('S')
        elif len(word) == 2:
            word_status = ['B', 'E']
        else:
            M_num = len(word) - 2
            M_list = ['M'] * M_num
            word_status.append('B')
            word_status.extend(M_list)
            word_status.append('E')
        return word_status

    #基于人工标注语料库，学习发射概率emit_dict，初始状态start_dict， 转移概率trans_dict
    def train(self, trainData, transMat, emitMat, startStates):
        trans_dict, emit_dict, start_dict, Count_dict = self.init() #初始化
        for line in open(trainData,encoding='utf-8'):  #逐行(逐句)处理
            self.line_index += 1
            line = line.strip()
            if not line:   #空行
                continue
            char_list = []
            for i in range(len(line)):
                if line[i] == " ":
                    continue
                char_list.append(line[i])   # 字序列
            self.char_set = set(char_list)  # 字集合

            word_list = line.split(" ")  #单词序列
            line_status = []  # 状态序列
            for word in word_list:
                line_status.extend(self.get_word_status(word))  # 一句话对应一行连续的状态

            if len(char_list) != len(line_status): continue  # 字和状态序列不匹配，不处理
            # print(word_list) # ['对外开放', '迈出', '了', '新', '的', '步伐', '。']
            # print(line_status) # ['B', 'M', 'M', 'E', 'B', 'E', 'S', 'S', 'S', 'B', 'E', 'S']
            for i in range(len(line_status)):
                Count_dict[line_status[i]] += 1  # 对应状态次数
                if i == 0:  # 首字状态计数
                    start_dict[line_status[0]] += 1
                else:  # 非首字
                    trans_dict[line_status[i - 1]][line_status[i]] += 1  # 计算转移概率
                    if char_list[i] not in emit_dict[line_status[i]]:   # 统计发射概率
                        emit_dict[line_status[i]][char_list[i]] =1# 0.0
                    else:
                        emit_dict[line_status[i]][char_list[i]] += 1  # 用于计算发射概率
        # 进行归一化
        for key in start_dict:  # 状态的初始概率
            start_dict[key] = start_dict[key] * 1.0 / self.line_index
        for row in trans_dict:  # 状态转移概率
            for col in trans_dict[row]:
                trans_dict[row][col] = trans_dict[row][col] / Count_dict[row]
        for key in emit_dict:  # 发射概率(状态->词语的条件概率)
            for word in emit_dict[key]:
                emit_dict[key][word] = emit_dict[key][word] / Count_dict[key]
        #保存模型
        self.save_model(trans_dict, transMat)
        self.save_model(emit_dict, emitMat)
        self.save_model(start_dict, startStates)
        return #trans_dict, emit_dict, start_dict

if __name__ == "__main__":
    trainData = './data/train.txt'     #语料放在当前目录的data目录下
    transMat = './model/prob_trans.model'     #统计模型存储在当前目录的model目录下
    emitMat = './model/prob_emit.model'
    startStates = './model/prob_start.model'
    trainer = HmmTrain()
    trainer.train(trainData, transMat, emitMat, startStates)