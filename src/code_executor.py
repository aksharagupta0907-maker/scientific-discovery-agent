
import subprocess


def execute_in_docker(code, timeout=30):
    command = [
        "docker",
        "run",
        "--rm",
        "--network=none",
        "--memory=256m",
        "--cpus=0.5",
        "--pids-limit=64",
        "python:3.11-slim",
        "python",
        "-c",
        code
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Experiment execution timed out.",
            "return_code": None
        }


if __name__ == "__main__":

    test_code = """
print("Hello from Docker Secure Sandbox!")
print("2 + 3 =", 2 + 3)
"""

    output = execute_in_docker(test_code)
    print(output)
