try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='replay',
    version='0.1',
    packages=['replay', ],
    license='MIT',
    description='Python driver for rehook bindings.',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['requests>=2.2', ],
)
