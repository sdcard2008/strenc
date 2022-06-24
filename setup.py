from setuptools import setup

setup(
    name="strenc" ,
    version="0.1.3" ,
    description="A simple fully customizable string encoder and decoder" ,
    url="https://github.com/sdcard2008/strenc" ,  #will add later 
    author="Saptak De" ,
    author_email="saptak1234hehe@gmail.com" ,
    packages=["strenc" , "_customizekeys"] ,
    package_requires=[
        'strenc' ,
        '_customizekeys'
    ] ,

    include_package_data=True ,
    entry_points={'console_scripts' : ['customizekeys = _customizekeys:__main']},

    long_description=
    """
    Simple String Encoder And Decoder , hence the name : str(string)enc(encoder). 
    Keys are customizable using the 'customizekeys'.

    Github Repo : https://github.com/sdcard2008/strenc
     
    """
)

