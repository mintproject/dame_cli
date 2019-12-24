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
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
    "Click>=7.0",
    "PyYAML>=5.1.2",
    "yamlordereddictloader",
    "jsonschema>=3.0.0",
    "requests",
    "semver>=2.8.1",
    "modelcatalog-api>=1.7.0",
]

version = {}
with open("src/mint/__init__.py") as fp:
    exec(fp.read(), version)



# This call to setup_name() does all the work
setup(
    name="mint",
    version=version["__version__"],
    description="A execution manager cli for execution",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mintproject/mint-execution-manager",
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
    entry_points={"console_scripts": ["mint = mint.__main__:cli"]},
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["mint.tests*"]),
    package_data={"mint": find_package_data("src/mint")},
    exclude_package_data={"mint": ["tests/*"]},
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.5.0",
)
