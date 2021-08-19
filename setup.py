from setuptools import setup, find_packages

setup(
    name="brench",
    version="0.1",
    description="BRENCH - BRightness Estimation in NeuroComputational models and Humans",
    author="Matko Matic, Lynn Schmittwilken, Joris Vincent",
    author_email="matko.matic@tutanota.com, L.Schmittwilken@tu-berlin.de, joris.vincent@tu-berlin.de",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "numpy",
        "matplotlib",
    ],
)
