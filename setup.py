from setuptools import setup

import configparser

config = configparser.ConfigParser()
config.read('s3mtools.cfg')
VERSION = config['SYSTEM']['version']

setup(
    name = 's3mtools',
    version = VERSION,
    description = 'The data-centric, model-first approach to information management. ',
    long_description = """The toolset for creating sharable, structured, semantic models.""",
    author = 'Timothy W. Cook',
    author_email = 'tim@datainsights.tech',
    url = 'https://datainsights.tech/S3Model/',  
    download_url = 'https://github.com/DataInsightsInc/S3Model/archive/' + VERSION + '.tar.gz',  
    keywords = ['context rdf xml machine learning data-centric semantic interoperability semantics'], 
    tests_require=['pytest',],  
    setup_requires=['pytest-runner',],  
    python_requires='>=3.6',
    packages=['s3m'],
    package_dir={'s3m': 's3m'},
    package_data={'docs': ['docs/*']},
    data_files=[('data', ['data/README.md']),
                ('dmlib', ['dmlib/dm-description.xsl']),
                ('rm', ['rm/s3model.owl', 'rm/s3model_3_0_0.xsd','rm/s3model_3_0_0.rdf', 'rm/s3model_3_0_0.xsl', 'rm/dm-description.xsl' ]),
                ('',['s3mtools.cfg','README.md','LICENSE.txt'])], 
    install_requires=[
      ],
    entry_points='''
            [console_scripts]
            s3mtools=s3m.manage:main
        ''',    
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Customer Service',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Education',
                   'Intended Audience :: Financial and Insurance Industry',
                   'Intended Audience :: Healthcare Industry',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Legal Industry',
                   'Intended Audience :: Manufacturing',
                   'Intended Audience :: Other Audience',
                   'Intended Audience :: Religion',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Telecommunications Industry',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   ],

)