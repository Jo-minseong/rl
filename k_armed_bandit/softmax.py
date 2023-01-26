import numpy as np

def softmax(nl):
    nl = nl - np.max(nl)
    nl = np.exp(nl)
    den = np.sum(nl)
    nl = nl/den
    return nl


sample_list = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 100])
print(softmax(sample_list))