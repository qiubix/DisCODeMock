from setuptools import setup


def readme():
    with open('README.md') as file:
        return file.read()


setup(name='discoderunner',
      version='0.1',
      description='Integration testing for DisCODe',
      long_description=readme(),
      url='http://github.com/qiubix/DisCODeRunner',
      author='qiubix',
      author_email='qiubix@gmail.com',
      license='MIT',
      packages=['discoderunner'],
      install_requires=[
          'pyhamcrest',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/install_discode.sh'],
      zip_safe=False)
