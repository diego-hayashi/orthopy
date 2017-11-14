# -*- coding: utf-8 -*-
#
# pylint: disable=too-few-public-methods
#
import sympy

from .import recurrence_coefficients
from .tools import evaluate_orthogonal_polynomial


def legendre(k, x, standardization='monic'):
    p0, a, b, c = recurrence_coefficients.legendre(k, standardization)
    return evaluate_orthogonal_polynomial(x, p0, a, b, c)


def jacobi(k, a, b, x, standardization='monic'):
    p0, a, b, c = recurrence_coefficients.jacobi(k, a, b, standardization)
    return evaluate_orthogonal_polynomial(x, p0, a, b, c)


def chebyshev1(k, x, standardization='monic'):
    return jacobi(
            k, -sympy.Rational(1, 2), -sympy.Rational(1, 2), x, standardization
            )


def chebyshev2(k, x, standardization='monic'):
    return jacobi(
            k, sympy.Rational(1, 2), sympy.Rational(1, 2), x, standardization
            )


def hermite(k, x, monic=True):
    '''Hermite polynomials, optionally (default=True) scaled such that the
    leading term has coefficient 1.
    '''
    coeff = sympy.Rational(1, 2**k) if monic else 1
    return coeff * sympy.polys.orthopolys.hermite_poly(k, x)


def laguerre(k, x, monic=True):
    '''Laguerre polynomials, optionally (default=True) scaled such that the
    leading term has coefficient 1.
    '''
    coeff = sympy.Rational((-1)**k, sympy.factorial(k)) if monic else 1
    return coeff * sympy.polys.orthopolys.laguerre_poly(k, x)
