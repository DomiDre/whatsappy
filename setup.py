from setuptools import setup, find_packages

with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

setup(
  name='whatsappy',
  version='1.0.0',
  description='Run Whatsapp in Selenium for programmatic access',
  url='https://github.com/DomiDre/whatsappy',
  author='Dominique Dresen',
  author_email='dominiquedresen@gmail.com',
  license=license,
  long_description=readme,
  install_requires=[
    'selenium'
  ],
  python_requires='>2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
  platforms=['Linux'],
  package_dir={'whatsappy': 'whatsappy'},
  packages=find_packages(
    exclude=(
      '_build',
      'docs',
      '_static',
      '_templates'
      'tests',
      'examples'
      )
  ),
  keywords='whatsapp selenium'
)