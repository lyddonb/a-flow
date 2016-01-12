from pip.req import parse_requirements
try:
    from pip.download import PipSession
except ImportError, e:
    raise ImportError("cannot import name PipSession, "
                      "Please update pip to >= 1.5")

from setuptools import setup, find_packages


def get_version():
    import imp

    with open('flow/_pkg_meta.py', 'rb') as fp:
        mod = imp.load_source('_pkg_meta', 'biloba', fp)

        return mod.version


def get_requirement_items(filename):
    """
    Load, parse and return the items from a requirements file.
    :param filename: A file path to a requirements text file.
    :return: A list of requirement items.
    """
    with PipSession() as session:
        return list(parse_requirements(filename, session=session))


def get_requirements(filename):
    """
    Get the requirements from a file.

    :param filename: A file path to a requirements text file.
    :return: A list of requirements.
    """
    reqs = get_requirement_items(filename)
    return [str(r.req) for r in reqs]


def get_install_requires():
    return get_requirements('requirements.txt')


def get_dependency_links():
    """
    Give setup() a -version for the requirements that are
    urls to avoid it looking for the related install_require at PyPI.
    """
    reqs = get_requirement_items('requirements.txt')

    if reqs:
        # Detect features of reqs from pip 1.5
        if not hasattr(reqs[0], 'link') and hasattr(reqs[0], 'url'):
            return [req.url + '-x.x' for req in reqs if req.url]

    return [req.link.url + '-x.x' for req in reqs
            if req.link and req.link.url]


setup(
    name='a-flow',
    version=get_version(),
    description='AWS Workflow Library',
    install_requires=get_install_requires(),
    dependency_links=get_dependency_links(),
    maintainer='Beau Lyddon',
    maintainer_email='lyddonb@gmail.com',
    url='https://github.com/lyddonb/a-flow',
    packages=find_packages(
        exclude=['tests']
    ),
    include_package_data=True,
)
