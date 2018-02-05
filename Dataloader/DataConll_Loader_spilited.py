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

    def clean_conll(self, string):
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", "", string)
        string = re.sub(r"\'s", "", string)
        string = re.sub(r"\'ve", "", string)
        string = re.sub(r"n\'t", "", string)
        string = re.sub(r"\'re", "", string)
        string = re.sub(r"\'d", "", string)
        string = re.sub(r"\'ll", "", string)
        string = re.sub(r",", "", string)
        string = re.sub(r"!", "", string)
        string = re.sub(r"\(", "", string)
        string = re.sub(r"\)", "", string)
        string = re.sub(r"\?", "", string)
        string = re.sub(r"\s{2,}", "", string)
        return string.strip()

    def dataLoader(self, path=None, shuffle=False):
        assert isinstance(path, list), "Path Must Be In List"
        print("Data Path {}".format(path))
        for id_data in range(len(path)):
            print("Loading Data Form {}".format(path[id_data]))
            insts = self.Load_Each_Data(path=path[id_data], shuffle=shuffle)
            # if shuffle is True:
            #     print("shuffle data......")
                # random.shuffle(insts)
            self.data_list.append(insts)
        # return train/dev/test data
        if len(self.data_list) == 3:
            return self.data_list[0], self.data_list[1], self.data_list[2]
        if len(self.data_list) == 2:
            return self.data_list[0], self.data_list[1]

    def Load_Each_Data(self, path=None, shuffle=False):
        assert path is not None, "The Data Path Is Not Allow Empty."
        insts = []
        with open(path, encoding="UTF-8") as f:
            inst = Instance()
            now_line = 0
            for line in f.readlines():
                now_line += 1
                sys.stdout.write("\rhandling with the {} line".format(now_line))
                line = line.strip()
                # print(line)
                if line == "" and len(inst.words) != 0:
                    inst.words_size = len(inst.words)
                    insts.append(inst)
                    inst = Instance()
                elif line == "":
                    continue
                else:
                    # line = self.clean_str(line)
                    line = line.strip().split(" ")
                    # print(line)
                    assert len(line) == 2, "Error Format"
                    # if len(line) != 2:
                    #     continue
                    word = line[0]
                    if word == "-DOCSTART-":
                        continue
                    # word = self.clean_conll(word)
                    # if word == "":
                    #     continue
                    # # if line[1] == "O":
                    # #     continue
                    # if (not word[0].isalpha()) and line[1][0] == "I":
                    #     continue
                    # if (not word[0].isalpha()) and line[1][0] == "O":
                    #     continue
                    inst.words.append(word.lower())
                    inst.labels.append(line[1])
                # if len(insts) == 2560:
                #     break
            if len(inst.words) != 0:
                inst.words_size = len(inst.words)
                insts.append(inst)
            print("\n")

        return insts


if __name__ == "__main__":
    print("Loading conll2000 dataset.")
    path = ["../Data/test/test.txt", "../Data/test/test.txt", "../Data/test/test.txt"]
    conll2000data = DataLoader()
    conll2000data.dataLoader(path=path, shuffle=True)



