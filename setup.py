import setuptools

setuptools.setup(
    name='runcible_ubnt_driver',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Grayson Head',
    author_email='grayson@graysonhead.net',
    packages=setuptools.find_packages(),
    license='GPL V3',
    install_requires=[
        'runcible>=0.2.0',
        'VyattaConfParser>=0.5.3'

    ],
    long_description=open('README.md').read(),
    # This is what Runcible looks at to decide if this is a driver candidate or not
    entry_points={'runcible.drivers': 'ubnt_edgerouter = runcible_ubnt.drivers.er_driver:UBNTEdgeRouterDriver'}
)
