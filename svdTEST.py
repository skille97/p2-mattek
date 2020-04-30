'''
svd
'''
import numpy as np
from numpy import linalg as LA

def PCA(B):
    mean = np.mean(B,axis=1)
    A = np.zeros(shape=B.shape)
    for i in range(B.shape[1]):
        A[:,i] = B[:,i]-mean
    At = np.transpose(A)

    AtA = At.dot(A)
    _, eigenAtA = LA.eigh(AtA)
    eigenAtA = np.flip(eigenAtA, 1)

    eigenAAt = A.dot(eigenAtA)

    for i in range(eigenAAt.shape[1]):
        eigenAAt[:,i] = eigenAAt[:,i]/LA.norm(eigenAAt[:,i])
        
    weights = np.transpose(eigenAAt)@A
    return weights

if __name__ == '__main__':
    A = (np.zeros(shape=(2, 3)))
    A[0, 0] =2
    A[0, 1] =1
    A[0, 2] =1.1
    A[1, 0] =1.1
    A[1, 1] =-1
    A[1, 2] =-1
    print(PCA(np.transpose(A)))
