from __future__ import division

import sys

class Instance:
    def __init__(self, label):
        self.label = label

    def show(self):
        print(self.label)

class accEval:
    def __init__(self):
        self.correct_num = 0
        self.gold_num = 0

    def acc(self):
        return self.correct_num / self.gold_num

class prfEval:
    def __init__(self, type):
        self.type = type
        self.correct_num = 0
        self.predict_num = 0
        self.gold_num = 0
        self.precision = 0
        self.recall = 0
        self.f = 0

    def prf(self):
        self.precision = self.correct_num / self.predict_num
        self.recall = self.correct_num / self.gold_num
        self.f = 2 * self.precision * self.recall / (self.precision + self.recall)
        return self.f

def getInsts(file_path, insts):
    file = open(file_path, encoding='utf8')
    for line in file.readlines():
        line = line.strip()
        label = line[0:1]
        ins = Instance(label)
        insts.append(ins)
    file.close()
def findEval(label, prf_evals):
    for idx in range(0, len(prf_evals)):
        if label == prf_evals[idx].type:
            return idx
    return -1

gold_insts = []
predict_insts = []
getInsts(sys.argv[1],gold_insts)
getInsts(sys.argv[2],predict_insts)
acc_eval = accEval()
label_table = []
if len(gold_insts) != len(predict_insts):
    print("error")
else:
    for inst in gold_insts:
        label_table.append(inst.label)
    label_table = list(set(label_table))
    prf_evals = []
    for idx in range(0, len(label_table)):
        e = prfEval(label_table[idx])
        prf_evals.append(e)

    for idx in range(0, len(gold_insts)):
        prf_evals[findEval(gold_insts[idx].label, prf_evals)].gold_num += 1
        prf_evals[findEval(predict_insts[idx].label, prf_evals)].predict_num += 1
        if gold_insts[idx].label == predict_insts[idx].label:
            prf_evals[findEval(predict_insts[idx].label, prf_evals)].correct_num += 1

    f_sum = 0
    for e in prf_evals:
        f_sum += e.prf()
    print("fmacro\t" + str(f_sum / len(prf_evals)), end='\t')

    for idx in range(0, len(gold_insts)):
        if gold_insts[idx].label == predict_insts[idx].label:
            acc_eval.correct_num += 1
            acc_eval.gold_num += 1
        else:
            acc_eval.gold_num += 1
    print("acc\t" + str(acc_eval.acc()))
