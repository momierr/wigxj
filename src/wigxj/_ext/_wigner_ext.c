#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "wigxjpf.h"
#include <math.h>

static int g_max_two_j = 400;
static int g_initialized = 0;

static void _cleanup(void) {
    if (g_initialized) {
        wig_temp_free();
        wig_table_free();
        g_initialized = 0;
    }
}

static int _check_j(int n, const double *js) {
    for (int i = 0; i < n; i++) {
        if (lround(2*js[i]) > g_max_two_j) {
            PyErr_Format(PyExc_ValueError,
                        "j exceeds max_j=%d; call wigxj.init(max_j) first",
                        g_max_two_j / 2);
            return -1;
        }
    }
    return 0;
}

static PyObject *py_init(PyObject *self, PyObject *args) {
    int max_j;
    if (!PyArg_ParseTuple(args, "i", &max_j))
        return NULL;
    if (max_j < 0) {
        PyErr_SetString(PyExc_ValueError, "max_j must be >= 0");
        return NULL;
    }
    _cleanup();
    g_max_two_j = 2 * max_j;
    wig_table_init(g_max_two_j, 9);
    wig_temp_init(g_max_two_j);
    g_initialized = 1;
    Py_RETURN_NONE;
}

static PyObject *py_wigner3j(PyObject *self, PyObject *args) {
    double j1, j2, j3, m1, m2, m3;
    if (!PyArg_ParseTuple(args, "dddddd", &j1, &j2, &j3, &m1, &m2, &m3))
        return NULL;
    double js[] = {j1, j2, j3};
    if (_check_j(3, js) < 0) {
        return NULL;
    }
    return PyFloat_FromDouble(wig3jj(
        (int)lround(2*j1), (int)lround(2*j2), (int)lround(2*j3),
        (int)lround(2*m1), (int)lround(2*m2), (int)lround(2*m3)));
}

static PyObject *py_wigner6j(PyObject *self, PyObject *args) {
    double j1, j2, j3, j4, j5, j6;
    if (!PyArg_ParseTuple(args, "dddddd", &j1, &j2, &j3, &j4, &j5, &j6))
        return NULL;
    double js[] = {j1, j2, j3, j4, j5, j6};
    if (_check_j(6, js) < 0) {
        return NULL;
    }
    return PyFloat_FromDouble(wig6jj(
        (int)lround(2*j1), (int)lround(2*j2), (int)lround(2*j3),
        (int)lround(2*j4), (int)lround(2*j5), (int)lround(2*j6)));
}

static PyObject *py_wigner9j(PyObject *self, PyObject *args) {
    double j1, j2, j3, j4, j5, j6, j7, j8, j9;
    if (!PyArg_ParseTuple(args, "ddddddddd",
                          &j1, &j2, &j3, &j4, &j5, &j6, &j7, &j8, &j9))
        return NULL;
    double js[] = {j1, j2, j3, j4, j5, j6, j7, j8, j9};
    if (_check_j(9, js) < 0) {
        return NULL;
    }
    return PyFloat_FromDouble(wig9jj(
        (int)lround(2*j1), (int)lround(2*j2), (int)lround(2*j3),
        (int)lround(2*j4), (int)lround(2*j5), (int)lround(2*j6),
        (int)lround(2*j7), (int)lround(2*j8), (int)lround(2*j9)));
}

static PyObject *py_clebsch_gordan(PyObject *self, PyObject *args) {
    double j1, m1, j2, m2, j3, m3;
    if (!PyArg_ParseTuple(args, "dddddd", &j1, &m1, &j2, &m2, &j3, &m3))
        return NULL;
    double js[] = {j1, j2, j3};
    if (_check_j(3, js) < 0) {
        return NULL;
    }
    double w3j = wig3jj(
        (int)lround(2*j1), (int)lround(2*j2), (int)lround(2*j3),
        (int)lround(2*m1), (int)lround(2*m2), (int)lround(-2*m3));
    long n = lround(-j1 + j2 - m3);
    double phase = (labs(n) % 2L == 0L) ? 1.0 : -1.0;
    return PyFloat_FromDouble(phase * sqrt(2*j3 + 1.0) * w3j);
}

static PyMethodDef methods[] = {
    {"init",           py_init,           METH_VARARGS, "init(max_j): reinitialize tables for j up to max_j"},
    {"wigner3j",       py_wigner3j,       METH_VARARGS, "wigner3j(j1,j2,j3,m1,m2,m3)"},
    {"wigner6j",       py_wigner6j,       METH_VARARGS, "wigner6j(j1,j2,j3,j4,j5,j6)"},
    {"wigner9j",       py_wigner9j,       METH_VARARGS, "wigner9j(j1,...,j9)"},
    {"clebsch_gordan", py_clebsch_gordan, METH_VARARGS, "clebsch_gordan(j1,m1,j2,m2,j3,m3)"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "_wigner", NULL, -1, methods
};

PyMODINIT_FUNC PyInit__wigner(void) {
    wig_table_init(g_max_two_j, 9);
    wig_temp_init(g_max_two_j);
    g_initialized = 1;
    Py_AtExit(_cleanup);
    return PyModule_Create(&moduledef);
}
