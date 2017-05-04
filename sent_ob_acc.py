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

def getInsts(file_path, insts, obs):
    file = open(file_path, encoding='utf8')
    count = 1
    for line in file.readlines():
        line = line.strip()
        end = line.find('[')
        seg = line[2:end-1]
        seg_info = seg.split(" ")
        label = line[0:1]
        type = 'noob'
        for word in seg_info:
            flag = 0
            for ob_word in obs:
                if word == ob_word:
                    type = 'ob'
                    flag = 1
                    break
            if flag == 1:
                break
        ins = Instance(label, seg_info, type)
        insts.append(ins)
        count += 1
    file.close()

def getOB(file_path, obs):
    file = open(file_path, encoding='utf8')
    for line in file.readlines():
        line = line.strip()
        obs.append(line)
    file.close()

gold_insts = []
predict_insts = []
evals = []
obs = []

e = Eval()
e.type = 'ob'
evals.append(e)

e = Eval()
e.type = 'nonob'
evals.append(e)

getOB(sys.argv[3], obs)
getInsts(sys.argv[1],gold_insts, obs)
getInsts(sys.argv[2],predict_insts, obs)
if len(gold_insts) != len(predict_insts):
    print('error')
else:
    for idx in range(0,len(gold_insts)):
        type = gold_insts[idx].type
        pos = 0
        if type == 'ob':
            pos = 0
        else:
            pos = 1
        evals[pos].gold_num += 1
        if (gold_insts[idx].label == predict_insts[idx].label):
            evals[pos].correct_num += 1

    print('type', 'acc')
    for e in evals:
        e.prf()
