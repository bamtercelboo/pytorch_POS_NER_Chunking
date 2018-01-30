# @Author : bamtercelboo
# @Datetime : 2018/1/30 15:58
# @File : DataConll2000_Loader.py
# @Last Modify Time : 2018/1/30 15:58
# @Contact : bamtercelboo@{gmail.com, 163.com}

"""
    FILE :  DataConll2000_Loader.py
    FUNCTION :
        Loading conll2000 dataset.
        Download From Here : https://www.clips.uantwerpen.be/conll2000/chunking/
"""
import os
import sys
import re
import random
import shutil
import torch
from Dataloader.Instance import Instance
import hyperparams as hy
torch.manual_seed(hy.seed_num)
random.seed(hy.seed_num)


class DataLoader():
    def __init__(self):
        print("Loading Data......")
        self.data_list = []

    def clean_str(self, string):
        """
        Tokenization/string cleaning for all datasets except for SST.
        Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
        """
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s", string)
        string = re.sub(r"\'ve", " \'ve", string)
        string = re.sub(r"n\'t", " n\'t", string)
        string = re.sub(r"\'re", " \'re", string)
        string = re.sub(r"\'d", " \'d", string)
        string = re.sub(r"\'ll", " \'ll", string)
        string = re.sub(r",", " , ", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\(", " \( ", string)
        string = re.sub(r"\)", " \) ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"\s{2,}", " ", string)
        return string.strip().lower()

    def dataLoader(self, path=None, shuffle=False):
        assert isinstance(path, list), "Path Must Be In List"
        for id_data in range(len(path)):
            print("Loading Data Form {}".format(path[id_data]))
            insts = self.Load_Each_Data(path=path[id_data], shuffle=shuffle)
            self.data_list.append(insts)
        # return train/dev/test data
        # return self.data_list[0], self.data_list[1], self.data_list[2]
        return self.data_list[0], self.data_list[1], self.data_list[2]

    def Load_Each_Data(self, path=None, shuffle=False):
        assert path is not None, "The Data Path Is Not Allow Empty."
        insts = []
        with open(path, encoding="UTF-8") as f:
            inst = Instance()
            for line in f.readlines():
                line = line.strip()
                if line == "" and len(inst.words) != 0:
                    insts.append(inst)
                    inst = Instance()
                else:
                    line = line.strip().split(" ")
                    assert len(line) == 3, "Error Format"
                    inst.words.append(line[0])
                    inst.labels.append(line[2])
            if len(inst.words) != 0:
                insts.append(inst)
        return insts


if __name__ == "__main__":
    print("Loading conll2000 dataset.")
    path = ["../Data/test/test.txt", "../Data/test/test.txt", "../Data/test/test.txt"]
    conll2000data = DataLoader()
    conll2000data.dataLoader(path=path, shuffle=True)



