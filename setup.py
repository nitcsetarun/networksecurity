"""
"""


from setuptools import find_packages,setup
from typing import List
from networksecurity.logging import logger


def get_requirements()->List[str]:
    """
    """
    requrementslist:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            logger.logging.info("Entring try block")
            lines=file.readlines()
            for line in lines:
                requirements=line.strip()
                if requirements and requirements!='-e .':
                    requrementslist.append(requirements)
    except FileNotFoundError:
        print("File Not Found")

    return requrementslist 


setup(
    name="Network Security",
    version="1.0.0.0",
    description="to demonstrate MLOPS pipeline",
    author="Tarun Kumar",
    author_email="tk.tarunkumar47@gmail.com",
    packages=find_packages(),
    requires=get_requirements()
)


