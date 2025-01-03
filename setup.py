from setuptools import setup, find_packages

setup(
    name='checkpoint',
    version='0.1.10',
    packages=find_packages(exclude=['tests.py']),
    include_package_data=True,
    description='functions for checkpointing',
    url='https://github.com/nyancat1232/checkpoint_function',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)