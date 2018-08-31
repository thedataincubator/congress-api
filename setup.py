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
    test_require=[
        'pytest',
        'responses'
    ]
    zip_safe=False
)
