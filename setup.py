import os
from setuptools import find_packages, setup

def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

install_requires = [
    "click==7.1.2",
    "decorator==4.4.2",
    "networkx==2.5.1",
    "cwltool==3.1.20210426140515",
    "modelcatalog-api==7.1.0",
    "texttable==1.6.3",
    "validators==0.18.1",
    "PyYAML==5.3.1",
    "semver==2.10.2",
    "requests==2.24.0",
    "jsonschema==3.2.0",
    "configparser==5.0.1",
    "certifi==2020.6.20",
    "docker==4.3.1",
]

version = {}
with open("src/dame/__init__.py") as fp:
    exec(fp.read(), version)



# This call to setup_name() does all the work
setup(
    name="dame-cli",
    version=version["__version__"],
    description="A execution manager cli for execution",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mintproject/dame_cli",
    author="Maximiliano Osorio",
    author_email="mosorio@isi.edu",
    license="Apache-2",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    entry_points={"console_scripts": ["dame = dame.__main__:cli"]},
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["dame.tests*"]),
    package_data={"dame": find_package_data("src/dame")},
    exclude_package_data={"dame": ["tests/*"]},
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.6.0",
)
