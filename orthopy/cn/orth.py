import numpy

from ..c1.recurrence_coefficients import Legendre
from ..tools import math_comb


def tree(X, n, symbolic=False):
    """Evaluates the entire tree of orthogonal polynomials for the n-cube

    The computation is organized such that tree returns a list of arrays, L={0, ...,
    dim}, where each level corresponds to the polynomial degree L.  Further, each level
    is organized like a discrete (dim-1)-dimensional simplex. Let's demonstrate this for
    3D:

    L = 1:
         (0, 0, 0)

    L = 2:
         (1, 0, 0)
         (0, 1, 0) (0, 0, 1)

    L = 3:
         (2, 0, 0)
         (1, 1, 0) (1, 0, 1)
         (0, 2, 0) (0, 1, 1) (0, 0, 2)

    The main insight here that makes computation for n dimensions easy is that the next
    level is composed by:

       * Taking the whole previous level and adding +1 to the first entry.
       * Taking the last row of the previous level and adding +1 to the second entry.
       * Taking the last entry of the last row of the previous and adding +1 to the
         third entry.

    In the same manner this can be repeated for `dim` dimensions.
    """
    # p0, a, b, c = legendre(n + 1, "normal", symbolic=symbolic)
    legendre_iterator = Legendre("normal", symbolic=symbolic)
    p0 = legendre_iterator.p0

    dim = X.shape[0]

    p0n = p0 ** dim
    out = []

    level = numpy.array([numpy.ones(X.shape[1:], dtype=int) * p0n])
    out.append(level)

    a = []
    b = []
    c = []

    for L in range(n):
        aa, bb, cc = next(legendre_iterator)
        a.append(aa)
        b.append(bb)
        c.append(cc)

        level = []
        for i in range(dim - 1):
            m1 = math_comb(L + dim - i - 1, dim - i - 1)
            if L > 0:
                m2 = math_comb(L + dim - i - 2, dim - i - 1)
            r = 0
            for k in range(L + 1):
                m = math_comb(k + dim - i - 2, dim - i - 2)
                val = out[-1][-m1:][r : r + m] * (a[L - k] * X[i] - b[L - k])
                if L - k > 0:
                    val -= out[-2][-m2:][r : r + m] * c[L - k]
                r += m
                level.append(val)

        # treat the last one separately
        val = out[-1][-1] * (a[L] * X[-1] - b[L])
        if L > 0:
            val -= out[-2][-1] * c[L]
        level.append([val])

        out.append(numpy.concatenate(level))

    return out