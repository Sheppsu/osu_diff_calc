import setuptools
import re


readme = ''
with open('README.rst') as f:
    readme = f.read()

version = ''
with open('osu_diff_calc/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

project_urls = {
    "Bug Tracker": "https://github.com/Sheepposu/osu_diff_calc/issues",
}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

packages = [
    'osu_diff_calc',
    'osu_diff_calc.osu'
]

setuptools.setup(
    name="osu_diff_calc",
    version=version,
    packages=packages,
    author="Sheepposu",
    description="Library for making difficulty and pp calculations with beatmaps.",
    long_description=readme,
    long_description_content_type="text/plain",
    project_urls=project_urls,
    classifiers=classifiers,
    python_requires=">=3.8.0",
    license="MIT",
    url="https://github.com/Sheepposu/osu_diff_calc",
)
