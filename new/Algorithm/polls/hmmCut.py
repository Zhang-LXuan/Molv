#!/usr/bin/env python3
# coding: utf-8
# File: hmm_cut.py
 
class HmmCut:
    def __init__(self):
        trans_path = r'C:\Users\12570\Desktop\Molv\new\new\Algorithm\polls\model\prob_trans.model'
        emit_path = r'C:\Users\12570\Desktop\Molv\new\new\Algorithm\polls\model\prob_emit.model'
        start_path = r'C:\Users\12570\Desktop\Molv\new\new\Algorithm\polls\model\prob_start.model'
        self.prob_trans = self.load_model(trans_path)
        self.prob_emit = self.load_model(emit_path)
        self.prob_start = self.load_model(start_path)
 
    '''加载模型'''
    def load_model(self, model_path):
        f = open(model_path, 'r')
        a = f.read()
        word_dict = eval(a)#返回字符串表达式的值
        f.close()
        return word_dict
 
    '''viterbi算法求解'''
    def viterbi(self, obs, states, start_p, trans_p, emit_p):  # 维特比算法（一种递归算法）
        # 算法的局限在于训练语料要足够大，需要给每个词一个发射概率, 如果dict中不存在这个key,则给一个很小的值或者0
        V = [{}] #tabular
        path = {}
        for y in states: #init
            V[0][y] = start_p[y] * emit_p[y].get(obs[0],0)
            path[y] = [y]
        for t in range(1,len(obs)):
            V.append({})
            newpath = {}
            for y in states:
                (prob,state ) = max([(V[t-1][y0] * trans_p[y0].get(y,0) * emit_p[y].get(obs[t],0) ,y0) for y0 in states if V[t-1][y0]>0])
                V[t][y] =prob
                newpath[y] = path[state] + [y]
            path = newpath
        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
        return (prob, path[state])
    # 分词
    def cut(self, sent):
        prob, pos_list = self.viterbi(sent, ('B', 'M', 'E', 'S'), self.prob_start, self.prob_trans, self.prob_emit)
        seglist = list()
        word = list()
        for index in range(len(pos_list)):
            if pos_list[index] == 'S':
                word.append(sent[index])
                seglist.append(word)
                word = []
            elif pos_list[index] in ['B', 'M']:
                word.append(sent[index])
            elif pos_list[index] == 'E':
                word.append(sent[index])
                seglist.append(word)
                word = []
        seglist = [''.join(tmp) for tmp in seglist]
 
        return seglist
 
#测试
if __name__ == "__main__":
    sent1 = '华中农业大学信息学院计算机科学系'
    sent2 = '目前在自然语言处理技术中，中文处理技术比西文处理技术要落后很大一段距离，许多西文的处理方法中文不能直接采用，就是因为中文必需有分词这道工序。中文分词是其他中文信息处理的基础，搜索引擎只是中文分词的一个应用。'''
    cuter = HmmCut()
    seglist1 = cuter.cut(sent1)
    seglist2 = cuter.cut(sent2)
    print(seglist1)
    print(seglist2)