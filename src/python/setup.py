from pathlib import Path
from zensols.pybuild import SetupUtil

su = SetupUtil(
    setup_path=Path(__file__).parent.absolute(),
    name="zensols.dsprov",
    package_names=['zensols', 'resources'],
    # package_data={'': ['*.html', '*.js', '*.css', '*.map', '*.svg']},
    package_data={'': ['*.conf', '*.json', '*.yml']},
    description='This library provides integrated MIMIC-III with discharge summary provenance of data annotations and Pythonic classes.',
    user='plandes',
    project='dsprov',
    keywords=['tooling'],
    # has_entry_points=False,
).setup()
