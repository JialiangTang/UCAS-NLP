import sys
import codecs
import math
import operator
from functools import reduce


def count_ngram(candidate, references, n):
    num = 0
    count = 0
    r = 0
    c = 0
    for j in range(len(candidate)):
        ref_counts, ref_lengths = build_ref(references, j, n)
        # 建立待测句子ngram表，维护长度
        cand_sentence = candidate[j]
        cand_dict = {}
        words = cand_sentence.strip().split()
        limits = len(words) - n + 1
        for i in range(0, limits):
            ngram = ' '.join(words[i:i + n]).lower()
            if ngram in cand_dict:
                cand_dict[ngram] += 1
            else:
                cand_dict[ngram] = 1
        # 考虑到有重复词，该函数计算source和ref中多重词出现的最低次数，作为总匹配ngram词数
        num_delta = 0
        for m in cand_dict.keys():
            m_w = cand_dict[m]
            m_max = 0
            for ref in ref_counts:
                if m in ref:
                    m_max = max(m_max, ref[m])
            m_w = min(m_w, m_max)
            num_delta += m_w
        num += num_delta
        count += limits
        lenw = len(words)
        minn = abs(lenw-ref_lengths[0])
        best = ref_lengths[0]
        for ref in ref_lengths:
            if abs(lenw-ref) < minn:
                minn = abs(lenw-ref)
                best = ref
        r += best
        c += lenw
    if(num == 0):
        pr = 0.0001
    else:
        pr = float(num) / count
    bp = penalty(c, r)
    return pr, bp

def build_ref(references, j, n):
    ref_counts = []
    ref_lengths = []
    # 建立参考译文ngram表，维护长度
    for reference in references:
        ref_sentence = reference[j]
        ngram_d = {}
        words = ref_sentence.strip().split()
        ref_lengths.append(len(words))
        limits = len(words) - n + 1
        # 统计ref中该句的ngram
        for i in range(limits):
            ngram = ' '.join(words[i:i+n]).lower()
            if ngram in ngram_d.keys():
                ngram_d[ngram] += 1
            else:
                ngram_d[ngram] = 1
        ref_counts.append(ngram_d)
    return ref_counts, ref_lengths


def penalty(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/c))
    return bp


def BLEU(source, ref):
    precisions = []
    gram_n = [1, 2, 3, 4] # 考虑1-gram到4-gram
    for i in gram_n:
        pr, penalty = count_ngram(source, ref, i)
        # precisions.append(pr)
        precisions.append((float)(1/4)*math.log(pr))
    
    # 采用几何平均
    # bleu = (reduce(operator.mul, precisions)) ** (1.0 / len(precisions)) * penalty
    bleu = math.exp((reduce(operator.add, precisions))) * penalty
    return bleu


if __name__ == "__main__":
    ref = []
    ref.append(codecs.open(sys.argv[2], 'r', 'utf-8').readlines())
    source = codecs.open(sys.argv[1], 'r', 'utf-8').readlines()
    bleu = BLEU(source, ref)
    # print ("The BELU value of sentence in source.txt is", bleu)
    print (bleu)

    out = open('resnumber.txt', 'w')
    out.write(str(bleu))
    out.close()

