from setuptools import setup

# TODO: with dependency_links deprecated, pip will no longer auto-install
# github requirements using setup.py one liner. instead: hack it
# (alternative: pip install -r ...)
import subprocess
github_requirements = [
    'git+https://github.com/natb1/test_data.git#egg=test-data'
]
for requirement in github_requirements:
    subprocess.check_call(('pip', 'install', requirement))

setup(
    name='mapping_tools',
    description='tools for mapping domain models',
    long_description=open('README.md').read(),
    url='https://github.com/natb1/mapping_tools',
    author='Nathan Buesgens',
    author_email='nathan@natb1.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='development',
    packages=['mapping_tools'],
    install_requires=[
        'mock', #TODO: make optional - only required for testing
                     ],
)
