import sys

class Instance:
    def __init__(self, label, seg_info, type):
        self.type = type
        self.label = label
        self.seg_info = seg_info

    def show(self):
        print(self.label, self.seg_info, self.type)

class Eval:
    def __init__(self):
        self.type = 0
        self.correct_num = 0
        self.gold_num = 0

        self.acc = 0
    def prf(self):
        self.acc = self.correct_num / self.gold_num
        print(self.type, self.acc)

def getInsts(file_path, insts):
    file = open(file_path, encoding='utf8')
    for line in file.readlines():
        seg = line.strip()
        seg_info = seg.split(" ")
        label = line[0:1]
        sl = len(seg_info)
        if sl > 30:
            sl = 30
        ins = Instance(label, seg_info, sl)
        insts.append(ins)
    file.close()

gold_insts = []
predict_insts = []
evals = []
for idx in range(0, 30):
    e = Eval()
    e.type = idx + 1
    evals.append(e)
getInsts(sys.argv[1],gold_insts)
getInsts(sys.argv[2],predict_insts)
if len(gold_insts) != len(predict_insts):
    print('error')
else:
    for idx in range(0,len(gold_insts)):
        type = gold_insts[idx].type - 1
        evals[type].gold_num += 1
        if (gold_insts[idx].label == predict_insts[idx].label):
            evals[type].correct_num += 1

    print('sent_length', 'acc')
    for e in evals:
        e.prf()