from setuptools import setup,find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyluog',
    version='0.13.8',
    description='A python module for using Luogu Api.',
    url='https://pypi.org/project/pyluog',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hlwdy',
    author_email='hlwdyck@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    platforms="any",
    install_requires=['requests','matplotlib','Pillow']
)