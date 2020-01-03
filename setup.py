import setuptools


with open("./readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    use_scm_version={"root": ".", "relative_to": __file__},
    scripts=['w1_therm_gcp.py'],
    test_suite = 'tests',
    setup_requires=['setuptools_scm'],
    name="w1_therm_gcp",
    author="Arnaud LE CANN",
    author_email="arnaud@lecann.com",
    description="GCP device for temperature of a w1 sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arnlec/w1-therm-mqtt",
    license="GPLv3",
    packages=setuptools.find_packages(),
    install_requires=[
        'w1thermsensor==1.1.2',
        'PyYAML==5.2',
        'pyjwt==1.7.1',
        'paho-mqtt==1.4.0'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: GPLv3'
    ],
    python_requires='>=3'
)