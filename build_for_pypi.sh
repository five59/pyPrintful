#!/bin/bash
python setup.py sdist
python setup.py bdist_wheel
echo "If all went well above, you can now publish to PyPi by running:"
echo "$ twine upload dist/*"
