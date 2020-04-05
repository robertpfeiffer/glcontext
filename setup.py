import platform, sys

from setuptools import Extension, setup

PLATFORMS = {'windows', 'linux', 'darwin', 'android'}

target = platform.system().lower()

for known in PLATFORMS:
    if target.startswith(known):
        target = known

if target not in PLATFORMS:
    target = 'linux'

if '--android' in sys.argv:
    target='android'
    sys.argv.remove('--android')

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
    language="c++",
    libraries=['user32', 'gdi32'],
)

x11 = Extension(
    name='glcontext.x11',
    sources=['glcontext/x11.cpp'],
    extra_compile_args=['-fpermissive'],
    language="c++",
    libraries=['dl'],
)

sdl2 = Extension(
    name='glcontext.sdl2',
    sources=['glcontext/sdl2.cpp'],
    extra_compile_args=['-fpermissive'],
    language="c++",
    libraries=['SDL2'],
)

egl = Extension(
    name='glcontext.egl',
    sources=['glcontext/egl.cpp'],
    extra_compile_args=['-fpermissive'],
    language="c++",
    libraries=['dl'],
)

darwin = Extension(
    name='glcontext.darwin',
    sources=['glcontext/darwin.cpp'],
    extra_compile_args=['-fpermissive', '-Wno-deprecated-declarations'],
    language="c++",
    extra_link_args=['-framework', 'OpenGL', '-Wno-deprecated'],
)

ext_modules = {
    'windows': [wgl],
    'linux': [x11, egl],
    'darwin': [darwin],
    'android': [sdl2, egl]
}
if '--with-sdl2' in sys.argv:
    sys.argv.remove('--with-sdl2')
    for platform in ext_modules:
        if sdl2 not in ext_modules[platform]:
            ext_modules[platform].append(sdl2)

setup(
    name='glcontext',
    version='2.1.0',
    description='Portable OpenGL Context',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/moderngl/glcontext',
    author='Szabolcs Dombi',
    author_email='cprogrammer1994@gmail.com',
    license='MIT',
    platforms=['any'],
    packages=['glcontext'],
    ext_modules=ext_modules[target],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
