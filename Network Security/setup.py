from setuptools import find_packages, setup
from typing import List

'''part of packaging and distribution python projects, used to define configuration, metadata, dependencies and more'''

def get_requirements()-> List[str]:
    # return list of requirements

    
    requirement_lst : List[str] = []



    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirement= line.strip()

                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt is not found")

    return requirement_lst

print(get_requirements())

setup(
    name= 'Network Security',
    version= '0.0.1',
    author= 'Vaishnavi',
    author_email= 'vaishnavisoni1723@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)