from setuptools import setup, find_packages

setup(name='pipeline',
      version='0.1',
      description='Brightness models pipeline',
      author='Matko Matic',
      author_email='matko.matic@tutanota.com',
      license='MIT',
#      packages=['pipeline'],
      packages=find_packages(include=['pipeline', 'pipeline.*']),
      zip_safe=False)
