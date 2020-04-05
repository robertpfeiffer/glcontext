#include <Python.h>
#ifdef __ANDROID__
#include <SDL.h>
#else
#include <SDL2/SDL.h>
#endif

struct GLContext {
    PyObject_HEAD
    SDL_GLContext sdl_context;
    SDL_Window* sdl_window;
};

PyTypeObject * GLContext_type;

GLContext * meth_create_context(PyObject * self, PyObject * args, PyObject * kwargs) {
    int glversion = 330;
    static char * keywords[] = {NULL};
    GLContext * res = PyObject_New(GLContext, GLContext_type);
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", keywords)) {
        PyErr_Format(PyExc_Exception, "Could not parse args");
       return NULL;
    }
    
    if (SDL_GL_LoadLibrary(NULL) != 0) {
        PyErr_Format(PyExc_Exception, "SDL could not load libGL: %s", SDL_GetError());
        return NULL;
    }

    res->sdl_window = SDL_GL_GetCurrentWindow();
    if (res->sdl_window == NULL) {
        PyErr_Format(PyExc_Exception, "No SDL window found: %s", SDL_GetError());
        return NULL;
    }
    
    res->sdl_context = SDL_GL_GetCurrentContext();
    if (res->sdl_context == NULL) {
        PyErr_Format(PyExc_Exception, "SDL could not create context: %s", SDL_GetError());
        return NULL;
    }
    
    return res;
}

PyObject * GLContext_meth_enter(GLContext * self) {
    if (SDL_GL_MakeCurrent(self->sdl_window, self->sdl_context) != 0) {
        PyErr_Format(PyExc_Exception, "SDL GL error: %s", SDL_GetError());
        return NULL;
    }
    Py_RETURN_NONE;
}


PyObject * GLContext_meth_exit(GLContext * self) {
    if (SDL_GL_MakeCurrent(self->sdl_window, NULL) != 0) {
        PyErr_Format(PyExc_Exception, "SDL GL error: %s", SDL_GetError());
        return NULL;
    }
    Py_RETURN_NONE;
}

PyObject * GLContext_meth_release(GLContext * self) {
    SDL_GL_DeleteContext(self->sdl_context);
    Py_RETURN_NONE;
}

PyObject * GLContext_meth_load(GLContext * self, PyObject * arg) {
    const char * method = PyUnicode_AsUTF8(arg);
    void * proc = (void *)SDL_GL_GetProcAddress(method);
    return PyLong_FromVoidPtr(proc);
}

void GLContext_dealloc(GLContext * self) {
    Py_TYPE(self)->tp_free(self);
}

PyMethodDef GLContext_methods[] = {
    {"load", (PyCFunction)GLContext_meth_load, METH_O, NULL},
    {"release", (PyCFunction)GLContext_meth_release, METH_NOARGS, NULL},
    {"__enter__", (PyCFunction)GLContext_meth_enter, METH_NOARGS, NULL},
    {"__exit__", (PyCFunction)GLContext_meth_exit, METH_VARARGS, NULL},
    {},
};


PyType_Slot GLContext_slots[] = {
    {Py_tp_methods, GLContext_methods},
    {Py_tp_dealloc, GLContext_dealloc},
    {},
};

PyType_Spec GLContext_spec = {"sdl2.GLContext", sizeof(GLContext), 0, Py_TPFLAGS_DEFAULT, GLContext_slots};

PyMethodDef module_methods[] = {
    {"create_context", (PyCFunction)meth_create_context, METH_VARARGS | METH_KEYWORDS, NULL},
    {},
};

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "empty", NULL, -1, module_methods};

extern "C" PyObject * PyInit_sdl2() {
    PyObject * module = PyModule_Create(&module_def);
    GLContext_type = (PyTypeObject *)PyType_FromSpec(&GLContext_spec);
    PyModule_AddObject(module, "GLContext", (PyObject *)GLContext_type);
    return module;
}
