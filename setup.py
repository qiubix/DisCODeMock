from setuptools import setup

setup(name='discoderunner',
      version='0.1',
      description='Integration testing for DisCODe',
      url='http://github.com/qiubix/DisCODeRunner',
      author='qiubix',
      author_email='qiubix@gmail.com',
      license='MIT',
      packages=['discoderunner'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
