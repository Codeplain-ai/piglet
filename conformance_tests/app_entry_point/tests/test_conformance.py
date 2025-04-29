"""
Conformance tests for the console application entry point.
These tests verify that the application can be executed properly.
"""
import os
import sys
import tempfile
import unittest
import subprocess
from pathlib import Path


class TestApplicationEntryPoint(unittest.TestCase):
    """Test cases for verifying the application entry point."""

    @classmethod
    def setUpClass(cls):
        """Create a temporary file for testing."""
        # Create a temporary file that will be used as input for the application
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        cls.temp_file.write(b"Test content for piglet application")
        cls.temp_file.close()

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files."""
        # Remove the temporary file
        if os.path.exists(cls.temp_file.name):
            os.unlink(cls.temp_file.name)

    def test_application_file_exists(self):
        """Test that the main application file exists."""
        app_path = Path("piglet.py")
        self.assertTrue(
            app_path.exists(),
            f"Application file '{app_path}' does not exist"
        )
        self.assertTrue(
            app_path.is_file(),
            f"'{app_path}' exists but is not a file"
        )

    def test_application_can_be_executed(self):
        """Test that the application file can be executed with Python."""
        app_path = Path("piglet.py")
        # Check if file exists first to avoid unnecessary errors
        self.assertTrue(app_path.exists(), f"Application file '{app_path}' does not exist")
        
        # Verify the file can be executed with Python
        result = subprocess.run([sys.executable, str(app_path), self.temp_file.name], capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, 
                         f"Failed to execute '{app_path}' with Python. Exit code: {result.returncode}")

    def test_command_line_execution(self):
        """Test that the application can be executed from command line."""
        try:
            # Run the application as a subprocess
            result = subprocess.run(
                [sys.executable, "piglet.py", self.temp_file.name],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Check that the process exited with code 0 (success)
            self.assertEqual(
                result.returncode, 0,
                f"Application exited with code {result.returncode} instead of 0. "
                f"stderr: {result.stderr}"
            )
        except Exception as e:
            self.fail(f"Failed to execute application: {e}")

    def test_output_capture(self):
        """Test that the application produces expected output."""
        result = subprocess.run(
            [sys.executable, "piglet.py", self.temp_file.name],
            capture_output=True,
            text=True,
            check=False
        )
        
        # The application should not produce errors
        self.assertEqual(
            result.returncode, 0,
            f"Application exited with code {result.returncode} instead of 0"
        )
        
        # Since the application uses logging, we expect some output
        # but we don't want to be too specific about the exact format
        # as that's an implementation detail
        self.assertNotIn(
            "Traceback", result.stderr,
            f"Application produced error traceback: {result.stderr}"
        )

    def test_error_handling(self):
        """Test that the application handles errors gracefully."""
        # We'll simulate an error by passing an invalid argument
        result = subprocess.run(
            [sys.executable, "piglet.py", "--invalid-argument", self.temp_file.name],
            capture_output=True,
            text=True,
            check=False
        )
        
        # The application should exit with code 2 when given invalid arguments
        # This is the standard behavior for argparse when it encounters an invalid argument
        self.assertEqual(
            result.returncode, 2,
            f"Application with invalid argument exited with unexpected code {result.returncode}. "
            f"Expected code 2 (standard argparse error code for invalid arguments)."
        )


if __name__ == '__main__':
    unittest.main()