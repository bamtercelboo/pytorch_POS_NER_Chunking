class Eval:
    def __init__(self):
        self.predict_num = 0
        self.correct_num = 0
        self.gold_num = 0

        self.precision = 0
        self.recall = 0
        self.fscore = 0

    def clear_PRF(self):
        self.predict_num = 0
        self.correct_num = 0
        self.gold_num = 0

        self.precision = 0
        self.recall = 0
        self.fscore = 0

    def getFscore(self):
        if self.predict_num == 0:
            self.precision = 0
        else:
            self.precision = (self.correct_num / self.predict_num) * 100

        if self.gold_num == 0:
            self.recall = 0
        else:
            self.recall = (self.correct_num / self.gold_num) * 100

        if self.precision + self.recall == 0:
            self.fscore = 0
        else:
            self.fscore = 2 * (self.precision * self.recall) / (self.precision + self.recall)

        return self.precision, self.recall, self.fscore

    def acc(self):
        return self.correct_num / self.gold_num


class EvalPRF:

    def evalPRF(self, predict_labels, gold_labels, eval):
        gold_ent = self.get_ent(gold_labels)
        predict_ent = self.get_ent(predict_labels)
        eval.predict_num += len(predict_ent)
        eval.gold_num += len(gold_ent)

        for p in predict_ent:
            if p in gold_ent:
                eval.correct_num += 1

    def get_ent(self, labels):
        idx = 0
        idy = 0
        endpos = -1
        ent = []
        while(idx < len(labels)):
            if (self.is_start_label(labels[idx])):
                idy = idx
                endpos = -1
                while(idy < len(labels)):
                    if not self.is_continue_label(labels[idy], labels[idx], idy - idx):
                        endpos = idy - 1
                        break
                    endpos = idy
                    idy += 1
                ent.append(self.cleanLabel(labels[idx]) + '[' + str(idx) + ',' + str(endpos) + ']')
                idx = endpos
            idx += 1
        return ent

    def cleanLabel(self, label):
        # start = ['B', 'b', 'M', 'm', 'E', 'e', 'S', 's', 'I', 'i']
        start = ['B', 'b', 'I', 'i']
        if len(label) > 2 and label[1] == '-':
            if label[0] in start:
                return label[2:]
        return label

    def is_continue_label(self, label, startLabel, distance):
        if distance == 0:
            return True
        if len(label) < 3:
            return False
        if distance != 0 and self.is_start_label(label):
            return False
        if (startLabel[0] == 's' or startLabel[0] == 'S') and startLabel[1] == '-':
            return False
        if (startLabel[0] == 'b' or startLabel[0] == 'B') and startLabel[1] == '-':
            return False
        if self.cleanLabel(label) != self.cleanLabel(startLabel):
            return False
        return True

    def is_start_label(self, label):
        # start = ['b', 'B', 's', 'S']
        # start = ['i', 'I']
        start = ['b', 'B']
        if len(label) < 3:
            return False
        # else:
        #     return (label[0] in start) and label[1] == '-'
        else:
            flag = ((label[0] in start) and label[1] == '-')
            return flag
            # return ((label[0] in start) and label[1] == '-')
