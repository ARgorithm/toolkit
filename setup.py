import setuptools

with open("docs/README.md", "r") as fh:
    long_description = fh.read()

__version__ = "0.0.12"

setuptools.setup(
    name="ARgorithmToolkit",
    version=__version__,
    author="ARgorithm",
    author_email="alansandra2013@gmail.com",
    description='A utility toolkit to help develop algorithms suitable for ARgorithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ARgorithm",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'typer', # For CLI
        'requests' , #For CLI
        'numpy'
    ],
    project_urls={  # Optional
        'Source': 'https://github.com/ARgorithm/toolkit',
        'Bug Reports' : "https://github.com/ARgorithm/toolkit/issues",
        'Documentation' : 'https://argorithm.github.io/toolkit'
    },
    entry_points = {
        'console_scripts': [
            'ARgorithm = ARgorithmToolkit.cli:app',
        ],
    }
)
