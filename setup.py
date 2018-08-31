from setuptools import setup 

setup(
    name="congress",
    description="API for propublica congress",
    url="https://github.com/thedataincubator/congress-api",
    author="TDI",
    license='MIT',
    packages=['congress'],
    install_requires=[
        'requests',
        'pandas'
    ],
    zip_safe=False
)
