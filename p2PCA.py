
import numpy as np
from numpy import linalg as LA


def PCA(B):
    """
    Calculates PCA of a matrix B.
    Parameters
    ----------
    B: TYPE float, m x n matrix

    Returns
    -------
    mean: TYPE float 
            DESCRIPTION: m x 1 vector, the mean of B
    
    eigenAAT: TYPE float matrix m x p
                DESCRIPTION: The p largest eigenvectors of A^TA
    weights: TYPE float matrix p x n
        The weights of A projected into the eigenvectors of its covariance matrix
    """
    for i in range(B.shape[1]):
        B[i,:] = (B[i,:] - np.mean(B[i,:]))/np.var(B[i,:])


    # mean center the data in B
    mean = np.mean(B, axis=1)
    A = np.zeros(shape=B.shape)
    for i in range(B.shape[1]):
        A[:, i] = B[:, i] - mean

    At = np.transpose(A)
    AtA = At.dot(A)  # Calulaete the C tilitat matix
    _, eigenAtA = LA.eigh(AtA)
    eigenAtA = np.flip(eigenAtA, 1)  # reverse the orders of the eigen vektorer.

    eigenAAt = A.dot(eigenAtA)

    # normalize the eigen vektorer
    for i in range(eigenAAt.shape[1]):
        eigenAAt[:, i] = eigenAAt[:, i] / LA.norm(eigenAAt[:, i])

    weights = np.transpose(eigenAAt).dot(A)  # The weights of A projektet in to the eigen vektores of its covariance matrix
    return mean, eigenAAt, weights


if __name__ == '__main__':
    A = (np.zeros(shape=(2, 3)))
    A[0, 0] = 2
    A[0, 1] = 1
    A[0, 2] = 1.1
    A[1, 0] = 1.1
    A[1, 1] = -1
    A[1, 2] = -1
    print(PCA(np.transpose(A)))
