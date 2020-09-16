import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ARgorithmToolkit", 
    version="0.0.1",
    author="ARgorithm",
    author_email="alansandra2013@gmail.com",
    description='''
        A utility toolkit to help develop algorithms suitable in ARgorithmLib
    ''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ARgorithm",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)