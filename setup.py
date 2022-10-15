from setuptools import setup, find_packages

setup(
    name='streamlib',
    packages=[find_packages('streamlib')],
    version='0.1.0',
    description='An object-based Python library for connecting to music \
    streaming services\' Web APIs',
    author='Seth Sabar',
    author_email='sethsabar@gmail.com',
    license='BSD 3-Clause',
    install_requires=[],
    python_requires='>=3',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3 :: Only",
        "License :: BSD 3-Clause",
        "Intended Audience :: Music Enthusiasts",
    ],
)
