from setuptools import setup


with open('README.md') as f:
	readme = f.read()
	
#with open('LICENSE') as f:
#	license = f.read()

setup(name='cryptool',
      version='0.1.0',
      description='A detection and decryption tool for basic ciphers.',
      url='https://github.com/mpalmer7/cryptool',
      author='mpalmer7',
      author_email='',
      license='',
      packages=find_packages(exclude=('tests')),
      zip_safe=False)