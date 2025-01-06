#!/usr/bin/env python3

import sys
import case_utils
from case_utils.case_validate import validate
import traceback

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_uco.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f'Python version: {sys.version}')
    print(f'case_utils version: {case_utils.__version__}')
    print(f'Python path: {sys.path}')
    print('Validating against CASE 1.3.0...')

    try:
        validate(file_path, case_version='case-1.3.0', ontology_version='1.3.0', debug=True)
        print('Validation successful')
        sys.exit(0)
    except Exception as e:
        print('Validation error:', str(e))
        print('Error type:', type(e).__name__)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 