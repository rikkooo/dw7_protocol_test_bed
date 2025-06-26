from setuptools import setup, find_packages

setup(
    name='dw6',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'GitPython',
        'httpx',
        'pytest',
        'pytest-cov',
        'pytest-mock',
        'pytest-anyio',
    ],
    entry_points={
        'console_scripts': [
            'dw6=dw6.main:main',
        ],
    },
    author='Windsurf Engineering',
    author_email='engineering@windsurf.ai',
    description='A robust, state-driven development workflow system.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/windsurfer-ai/windsurf-development-workflow',
)
