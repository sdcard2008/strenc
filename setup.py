from setuptools import find_packages, setup
from os.path import abspath, dirname, join
import os
README_MD = open(join(dirname(abspath(__file__)), "README.md")).read()
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()
setup(
    name="strenc" ,
    version="0.2.8" ,
    description="A simple fully customizable string encoder and decoder" ,
    url="https://github.com/sdcard2008/strenc" ,  #will add later 
    author="Saptak De" ,
    author_email="saptak1234hehe@gmail.com" ,
    packages=find_packages(exclude=['strenccli' , 'tests']) ,
    
    include_package_data=True ,
    entry_points={'console_scripts' : ['strenc = strenccli:__main']},

    long_description=README_MD ,
    long_description_content_type="text/markdown",
    install_requires=install_requires

)

