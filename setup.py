from setuptools import find_packages, setup

setup(
    name='poll',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'werkzeug',
        'pytest',
        'wtforms',
        'itsdangerous',
        'python_dotenv'
    ],
)
