import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfn_man",
    version="0.0.1",
    author="Steven Miller",
    author_email="sjmiller609@gmail.com",
    description="man pages for cloud formation",
    entry_points={
        'console_scripts': [
            'cfn-man = cfn_man:main',
    ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix"
    ],
)
