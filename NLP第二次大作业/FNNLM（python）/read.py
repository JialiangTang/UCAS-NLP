import numpy as np
test = np.load('./nnlm_word_embeddings.zh.npy')
print(test)
np.savetxt('npy.txt',test)