from setuptools import setup, find_packages
from os.path import join

name = 'spear.content'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()
readme = open("README.txt").read()
history = ""

setup(name = name,
      version = version,
      description = 'A grok utility to register non AT Plone content type',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'plone CMS zope',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://tracker.trollfot.org',
      license = 'GPL',
      packages = find_packages(),
      namespace_packages = ['spear'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires=[
        'five.grok',
        'setuptools',
        'spear.ids',
        'zope.component',
        'zope.event',
        'zope.interface',
        'zope.schema',
      ],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
