'''
Setup.py files can be used to create libraries
'''

from setuptools import  find_packages, setup



'''
Write code to get requirement.txt as a list variable and pass it in install_requries variable in setup method
'''


setup(
    name="sensor",
    version="0.0.1",
    author="Shubham",
    author_email="shubhamsharma1808@gmail.com",
    packages=find_packages(),
    install_requires=[],
)