import pickle
import numpy as np
F=open(r'C:\Users\唐嘉良\Desktop\NNLM-master\NNLM-master\data\vocab.zh.pkl','rb')

content=pickle.load(F)
#np.savetxt('pkl.txt',content)
print(content)
