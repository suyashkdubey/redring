import subprocess
import platform

class PythonUtilities():
    """
    provides python utilities that python scanners can use
    """
    # below are the helper functions that utility uses and should not be used explicitly, if needed there are os specific scanners avilable.
    def _detect_system(self) -> str:
        """
        detects the operating system of the system and returns it.
        """
        system = platform.system()
        return system.strip().lower()

    def _determine_python_command_for_system(self) -> tuple[str, ...]:
        """
        detects the python commands that runs on specific os and returns it.
        """
        system = self._detect_system()
        if system == "windows":
            return ("python", "py")
        return ("python", "python3")

    # below are the available utilities that developers can use
    def find_python(self) -> str | None:
        commands = self._determine_python_command_for_system()
        for command in commands:
            result = subprocess.run([command, "-c", "import sys; print(sys.executable)"], capture_output=True, text=True)
            if result.returncode != 0:
                continue
            executable = result.stdout.strip()
            if executable:
                return executable
        return None