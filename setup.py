'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''
from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function returns the list of requirements except "-e ."
    '''
    try:
        requirement_list:List[str] = []
        with open("requirements.txt", 'r') as file:
            # Returns a list of all the lines in the requirements.txt file
            lines = file.readlines()
            # Read every line individually
            for line in lines:
                #strip every line of any whitespaces
                requirement = line.strip()
                if requirement and "-e ." not in requirement:
                    requirement_list.append(requirement)  # Append the requirement to the list
    
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list


setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Arnav Malhotra",
    author_email="arnavmalhotra73@gmail.com",
    packages=find_packages(),   # Identifies all folders to build as packages
    install_requires=get_requirements()  # When packages are being built it makes sure that the requirements are installed
)

#-e . Refers to setup.py file and runs that file as well, builds the python project as a package with all these requirements pre-installed
# Builds the python project as well as all folders containing __init__.py file as package
# Can be used when the entire project is completed and can be built as a package
