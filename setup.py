from setuptools import setup, find_packages

setup(
    name="connectify",
    version="0.1.0",
    description="Connectify — unified small wrappers for popular APIs (MVP)",
    author="Ivan",
    packages=find_packages(),
    install_requires=["requests"],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
