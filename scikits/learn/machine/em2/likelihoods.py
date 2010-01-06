#! /usr/bin/python
#
# Copyrighted David Cournapeau
# Last Change: Thu Jan 22 02:00 PM 2009 J

"""This module implements various basic functions related to multivariate
gaussian, such as likelihood, confidence interval/ellipsoids, etc..."""

import numpy as np

from scikits.learn.machine.em.densities import multiple_gauss_den
from _lk import quadform, logsumexp as _logsumexp

def mnormalik(data, mu, va, log=False, out=None):
    k = np.shape(mu)[0]
    n, d = np.shape(data)

    if out is not None:
        out = np.asarray(out)
        (no, ko) = out.shape
        if not no == n or not ko == k:
            raise ValueError("Argout not the right size (%d, %d), "
                        "expected (%d, %d)" % (no, ko, n, k))
    else:
        out = np.empty((n, k), dtype=data.dtype, order='C')

    if mu.shape == va.shape:
        inva = 1/va
        fac = (2*np.pi) ** (-d/2.0) * np.prod(np.sqrt(inva), axis=-1)
        inva *= -0.5
        #pquadform(data, mu, inva, np.log(fac), out)
        quadform(data, mu, inva, np.log(fac), out)
        if not log:
            return np.exp(out)
        else:
            return out
    else:
        raise ValueError("Full covariance not yet supported")

def pquadform(input, mu, sp, fac, out):
    for c in range(k):
        x = (input-mu[c]) ** 2
        out[:, c] = np.dot(x, sp[c].T)
        out[:,c] += fac[c]

def test(data, mu, va, log=False):
    y = mnormalik(data, mu, va, log)
    yr = multiple_gauss_den(data, mu, va, log=log)
    np.testing.assert_array_almost_equal(y, yr)

def logsumexp(x, out=None):
    if not out:
        y = np.empty(x.shape[0], x.dtype)

    _logsumexp(x, y)
    return y

if __name__ == '__main__':
    d = 20
    k = 15
    n = 1e4
    log = True

    type = np.float64

    mu = np.random.randn(k, d).astype(type)
    va = np.random.randn(k, d).astype(type)
    va **= 2 

    x = np.random.randn(n, d).astype(type)

    test(x[:1000, :], mu, va, log)
    y = np.empty((n, k), dtype=x.dtype)
    mnormalik(x, mu, va, out=y, log=log)
    #mnormalik(x, mu, va, out=None, log=log)

    x = np.array([[-1000., -1001], [-2000, -2500]])
    print logsumexp(x)
    print np.log(np.sum(np.exp(x), axis=-1))
