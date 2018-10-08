from setuptools import setup, find_packages 

setup(
    name="congress",
    description="API for propublica congress",
    url="https://github.com/thedataincubator/congress-api",
    author="TDI",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas'
    ],
    zip_safe=False
)
