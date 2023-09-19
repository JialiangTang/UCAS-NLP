import pickle
import numpy as np
import os
import math
import random

data_dir = "./data"
vocab_file = os.path.join(data_dir, "c1998.pkl") #词汇表文件
with open(vocab_file, 'rb') as f:
    vocab = pickle.load(f, encoding='bytes')
word_emb = np.load('c1998_embeddings.zh.npy') #词向量文件

def cosin_distance(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)

#vocab = {v : k for k, v in vocab.items()}
j = random.randint(0,len(vocab)-1) #随机选一个词
word1 = vocab[j]
similar = {}
for i in range(len(vocab)):
    word2 = vocab[i]
    word1_id = vocab.index(word1)
    word2_id = vocab.index(word2)
    word1_emb = word_emb[word1_id]
    word2_emb = word_emb[word2_id]
    similar.update({word2: cosin_distance(word1_emb,word2_emb)})
similar_condition = sorted(similar.items(),key=lambda x : x[1], reverse=True)
#similar.sorted(key=lambda x : x[1], reverse=True)
print(word1)
for k in range(1,11):
    print(similar_condition[k])