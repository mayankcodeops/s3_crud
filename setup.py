from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='csvviewer',
    version='1.0.0',
    author="Mayank Sharma",
    author_email="me.mayank.0602@gmail.com",
    description="A package for viewing uploaded CSV file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mayankcodeops/csv_viewer",
    project_urls={
        "Bug Tracker" : "https://github.com/mayankcodeops/csv_viewer/issues"
    },
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-bootstrap',
    ],
)


