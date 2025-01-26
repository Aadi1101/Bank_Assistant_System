from typing import List
from setuptools import setup, find_packages # type: ignore

def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path,encoding='utf-8') as file:
        requirements = file.readlines()
        requirements = [req.replace('\n','') for req in requirements]
        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements

setup(
    name="AI Powered Bank Assistant",
    version="0.0.1",
    author="Aaditya Komerwar",
    author_email="aadityakomerwar@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)