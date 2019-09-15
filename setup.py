import platform

from setuptools import Extension, setup

PLATFORMS = {'windows', 'linux', 'darwin'}

target = platform.system().lower()

for known in PLATFORMS:
    if target.startswith(known):
        target = known

if target not in PLATFORMS:
    target = 'linux'

if target == 'darwin':
    import os
    from distutils.sysconfig import get_config_var
    from distutils.version import LooseVersion
    if 'MACOSX_DEPLOYMENT_TARGET' not in os.environ:
        current_system = LooseVersion(platform.mac_ver()[0])
        python_target = LooseVersion(get_config_var('MACOSX_DEPLOYMENT_TARGET'))
        if python_target < '10.9' and current_system >= '10.9':
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'

wgl = Extension(
    name='glcontext.wgl',
    sources=['glcontext/wgl.cpp'],
    libraries=['user32', 'gdi32'],
)

x11 = Extension(
    name='glcontext.x11',
    sources=['glcontext/x11.cpp'],
    extra_compile_args=['-fpermissive'],
    libraries=['dl'],
)

egl = Extension(
    name='glcontext.egl',
    sources=['glcontext/egl.cpp'],
    extra_compile_args=['-fpermissive'],
    libraries=['dl'],
)

darwin = Extension(
    name='glcontext.darwin',
    sources=['glcontext/darwin.cpp'],
    extra_compile_args=['-fpermissive', '-Wno-deprecated-declarations'],
    extra_link_args=['-framework', 'OpenGL', '-Wno-deprecated'],
)

ext_modules = {
    'windows': [wgl],
    'linux': [x11, egl],
    'darwin': [darwin],
}

setup(
    name='glcontext',
    version='0.1.0',
    ext_modules=ext_modules[target],
)