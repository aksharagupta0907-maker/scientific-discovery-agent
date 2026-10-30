
import ast


def validate_python_code(code):
    """Perform basic syntax validation before execution."""

    try:
        ast.parse(code)
        return True, "Python syntax is valid."
    except SyntaxError as error:
        return False, f"Syntax error: {error}"


def prepare_experiment(code):
    """
    Validate experiment code without executing it.
    Actual execution will be handled by the Docker sandbox.
    """

    is_valid, message = validate_python_code(code)

    return {
        "valid": is_valid,
        "message": message,
        "code": code if is_valid else None
    }
