import os
import math
import numpy as np
path = os.getcwd()
def main():
    number = input("第几个词？ ")
    targetstr = ""  # 取词

    with open(os.path.join(path, "vocab.txt"), "r", encoding='utf-8') as iv:
        content = iv.readlines()
        #targetstr += content[int(number) - 1].split('/')[0]  # 去掉token \n
        targetstr += content[int(number) - 1]

        maxval_seq = {}  # 最相似的二十个，格式{序号 : cos}

        with open(os.path.join(path, "vec.txt"), "r") as ow:
            listr = ow.readlines()
            test = listr[int(number) - 1].split(' ')  # 获取一个向量列表(100元素)**********
            # print(len(test))
            for i in range(0, len(test)-1):#*****************
                test[i] = eval(test[i])
            #test = test.pop()
            # print(test)
            # print(test[3])
            del test[-1]
            # print(test)
            test = np.array(test)
            
            for i in range(0, len(listr)):  # 遍历整个embeddings
                # if i <3:
                #     print(maxval_seq)
                vec = listr[i].split(' ')
                # vec = [float(item.strip()) for item in vec]
                for j in range(0, len(vec)-1):#*****************
                    vec[j] = eval(vec[j].strip())
                #vec = vec.pop()
                del vec[-1]
                vec = np.array(vec)
                # for k in range(0, 10):
                #     vec[k] = vec[k].strip()

                res = np.dot(vec, test) / (np.linalg.norm(test) * np.linalg.norm(vec))
                # print(i)
                if 0 <= i < 10:
                    maxval_seq[i + 1] = res
                    # print(maxval_seq)
                else:
                    for keys in maxval_seq.keys():
                        maxval_seq = dict(sorted(maxval_seq.items(), key=lambda d:d[1],reverse=True)) #按res排序
                        if res > maxval_seq[keys]:
                            listt = list(maxval_seq.keys())
                            # print(listt[-1])
                            del maxval_seq[listt[-1]]
                            # del maxval_seq[keys]
                            maxval_seq[i + 1] = res
                            # maxval_seq = dict(sorted(maxval_seq.items(), key=lambda x: x[1], reverse=True))
                            # 替换比自己小的，把自己加进字典，按cos倒序重排
                            break
                # print(maxval_seq)

            
            del maxval_seq[int(number)]
            print(targetstr,end="")
            # print(maxval_seq)
            print("The top10 similar words are:")
            for keys in maxval_seq:
                # print(str(keys) + content[keys - 1])
                
                print(content[keys - 1] + "similarity:" , maxval_seq[keys])
                # print(str(keys) + content[keys].strip())


if __name__ == "__main__":
    main()
