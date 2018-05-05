"""functions for principal component analysis."""
import numpy as np
from scipy import linalg


def pca(data, vnames=None, standardize=False, covariance=False, sort=False):
    '''
    Performs principal component analysis on a numpy data array.

    Inputs are
    data - an array containing one row per observation and one column per
    variable observed.  There must be at least two columns and two rows.
    standardize - optional, default = False.  If True,
    values are normalized to a mean of zero and standard deviation of one.
    covariance - optional, default = False.  If True a covariance matrix is
    used as the basis of the calculations.  By default, correlation is used.
    sort - optional, default = False.  If outputs are sorted without names,
    the user can't tell which variables are represented!

    Outputs are
    eigenval - the eigenvalues sorted in descending order.
    eigenvec - eigenvectors in the same order, with one column per variable.
    pct_acct - percent of variance accounted for by each principal component.
    loadings - factor loadings for each component.
    '''

    if standardize:
        data = (data - np.mean(data, 0)) / np.std(data, 0, ddof=1)

    # R is the correlation matrix.
    if covariance:
        r_matrix = np.cov(data, rowvar=False)
    else:
        r_matrix = np.corrcoef(data, rowvar=False)
    val, vec = linalg.eig(r_matrix)
    val = np.real(val)   # use real values

    if not sort:
        pct_acct = 100*val/np.sum(val)
        loadings = np.matmul(vec, np.diag(val)**0.5)
        if not vnames:
            return val, vec, pct_acct, loadings
        return val, vec, pct_acct, loadings, vnames

    # Sort eigenvalues and vectors in order of decreasing variance.
    # Values in "val" are the variance.
    # Argsort sorts in increasing order.  [::-1] reverses the output array.
    sort_index = np.argsort(val)[::-1]
    eigenval = val[sort_index]
    eigenvec = vec[sort_index, :]

    pct_acct = 100*eigenval/np.sum(eigenval)

    loadings = np.matmul(eigenvec, np.diag(eigenval)**0.5)

    if not vnames:
        return eigenval, eigenvec, pct_acct, loadings
    out_names = np.array(vnames)[sort_index]
    return eigenval, eigenvec, pct_acct, loadings, out_names


if __name__ == '__main__':
    # Check the outputs using the Emery and Thomson example from MS 263
    data = np.array([[2.5, 2.4],
                     [0.5, 0.7],
                     [2.2, 2.9],
                     [1.9, 2.2],
                     [3.1, 3.0],
                     [2.3, 2.7],
                     [2, 1.6],
                     [1, 1.1],
                     [1.5, 1.6],
                     [1.1, 0.9]])
    # The example adjusts the data by subtracting the mean, but does not
    # compute z-scores, so match that.
    data = data - np.mean(data, 0)
    [eigenval, eigenvec, pct_acct, loadings] = pca(data, covariance=True)
    print('Test data:\n', data)
    print('Eigenvalues:\n', eigenval)
    print('Eigenvectors:\n', eigenvec)
    print('Variance accounted for by each component:\n', pct_acct)
    print('Component loadings:\n', loadings)
