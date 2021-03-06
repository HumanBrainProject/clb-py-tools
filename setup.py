from setuptools import setup, find_packages

requirements = ["requests"]

with open("README.md") as rm:
    long_description = rm.read()

setup(
    name="clb-py-tools",
    version="0.2.0",
    description="The Collaboratory Python Tools are a set of packages to help"
    "with the integration with the Collaboratory services and infrastructure.",
    long_description=long_description,
    author="Human Brain Project Collaboratory Team",
    author_email="support@humanbrainproject.eu",
    url="https://wiki.humanbrainproject.eu/",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=requirements,
    extras_require={
        "testing": ["pytest", "requests-mock", "tox", "pytest-tornasync"],
        "development": ["sphinx", "sphinx_rtd_theme", "sphinxcontrib-napoleon"],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
)
