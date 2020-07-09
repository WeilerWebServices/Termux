import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="flasktodo",
    version="0.0.1",
    author="Julio Pochet & Nathan Weiler",
    author_email="jrpochetedmead192@stevenscollege.edu | njweiler192@stevenscollege.edu",
    url="https://github.com/jpochetedmead/flask-todo",
    description="A simple to-do application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['flask', 'psycopg2'],
    tests_require=['pytest'],
    python_requires='>=3.6',
)
