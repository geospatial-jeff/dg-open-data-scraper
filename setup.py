from setuptools import setup, find_packages

with open('./requirements.txt') as reqs:
    requirements = [line.rstrip() for line in reqs]

setup(name="dg-open-data-scraper",
      version='0.1',
      author='Jeff Albrecht',
      author_email='geospatialjeff@gmail.com',
      packages=find_packages(),
      install_requires = requirements,
      entry_points= {
          "console_scripts": [
              "dg-open-data=scraper._cli:dg_open_data"
          ]},
      include_package_data=True
      )