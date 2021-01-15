import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptofetch",
    version="1.2.1",
    description="CLI tool to fetch and view cryptocurrencies prices",
    url="https://github.com/codeswhite/cryptofetch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'interutils',
        'prettytable',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'cryptofetch = cryptofetch:main',
        ],
    },
    author="Max G",
    author_email="max3227@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages()
)
