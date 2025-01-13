import re

def check_version(current, required):
    def parse_version(version):
        """Convert a version string like '22.04' into a tuple of integers (22, 4)."""
        return tuple(map(int, version.split('.')))

    def compare_versions(current, operator, required):
        """Compare two versions using the specified operator."""
        ops = {
            '==': lambda a, b: a == b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
        }
        if operator not in ops:
            raise ValueError(f"Unsupported operator: {operator}")
        return ops[operator](current, required)

    current_version = parse_version(current)

    # Handle multiple comparisons like '>20.04,<22.04'
    if ',' in required:
        conditions = required.split(',')
        for condition in conditions:
            match = re.match(r'([<>]=?|==)(.+)', condition)
            if not match:
                raise ValueError(f"Invalid condition: {condition}")
            operator, required_version = match.groups()
            if not compare_versions(current_version, operator, parse_version(required_version)):
                return False
        return True

    # Handle single comparison like '==22.04' or '>20.04'
    match = re.match(r'([<>]=?|==)?(.+)', required)
    if not match:
        raise ValueError(f"Invalid required condition: {required}")
    operator, required_version = match.groups()
    operator = operator or '>='  # Default to '>=' if no operator is provided
    return compare_versions(current_version, operator, parse_version(required_version))
