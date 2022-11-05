from setuptools import find_packages, setup
from os.path import abspath, dirname, join
README_MD = open(join(dirname(abspath(__file__)), "README.md")).read()
setup(
    name="strenc" ,
    version="0.2.6" ,
    description="A simple fully customizable string encoder and decoder" ,
    url="https://github.com/sdcard2008/strenc" ,  #will add later 
    author="Saptak De" ,
    author_email="saptak1234hehe@gmail.com" ,
    packages=find_packages(exclude='tests') ,
    
    include_package_data=True ,
    entry_points={'console_scripts' : ['strenc = _customizekeys:__main']},

    long_description=README_MD ,
    long_description_content_type="text/markdown"

)

