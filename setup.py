import setuptools

with open("docs/README.md", "r") as fh:
    long_description = fh.read()

__version__ = "0.2.3"

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
    include_package_data=True,
    install_requires=[
        'typer>=0.3.2', # For CLI
        'requests>=2.25.1' , #For CLI
        'numpy>=1.19.5',
        'halo>=0.0.31',
        'jsonschema>=3.2.0',
        'pyflakes>=2.2.0'
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
