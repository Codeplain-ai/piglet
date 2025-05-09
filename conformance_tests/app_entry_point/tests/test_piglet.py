#!/usr/bin/env python3
"""
Conformance tests for the piglet.py application entry point.
"""
import unittest
import subprocess
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr
import tempfile


class TestPigletEntryPoint(unittest.TestCase):
    """Test cases for the piglet.py application entry point."""

    def setUp(self):
        """Set up test environment."""
        # Ensure piglet.py exists in the current directory
        self.assertTrue(os.path.exists("piglet.py"), 
                        "piglet.py not found in the current directory")
        
        # Make sure piglet.py is executable
        if not os.access("piglet.py", os.X_OK) and sys.platform != "win32":
            os.chmod("piglet.py", os.stat("piglet.py").st_mode | 0o111)
        
        # Create a temporary test file
        self.test_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.test_file.write("This is a test file for piglet.py")
        self.test_file.close()
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'test_file') and os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)

    def test_basic_execution(self):
        """Test that the application can be executed without errors."""
        try:
            result = subprocess.run(
                [sys.executable, "piglet.py", self.test_file.name],
                capture_output=True,
                text=True,
                timeout=5
            )
            self.assertEqual(result.returncode, 0, 
                            f"Application failed with return code {result.returncode}. "
                            f"stderr: {result.stderr}")
            # Check that the application processed the file (log messages go to stderr)
            self.assertIn(f"Processing file: {self.test_file.name}", result.stderr)
        except subprocess.TimeoutExpired:
            self.fail("Application execution timed out after 5 seconds")
        except Exception as e:
            print(f"Exception: {e}")
            self.fail(f"Failed to execute application: {str(e)}")

    def test_output_format(self):
        """Test that the application produces expected log output."""
        result = subprocess.run(
            [sys.executable, "piglet.py"],
            capture_output=True,
            text=True
        )

        # The application should not produce any output to stdout by default
        self.assertEqual(result.stdout.strip(), "", 
                        f"Unexpected stdout output: {result.stdout}")
        
        # Debug messages are not shown at default INFO level
        self.assertNotIn("Application started", result.stdout)
        self.assertNotIn("Application completed successfully", result.stdout)

    def test_file_not_found(self):
        """Test that the application returns an error when file is not found."""
        non_existent_file = "non_existent_file.txt"
        result = subprocess.run(
            [sys.executable, "piglet.py", non_existent_file],
            capture_output=True,
            text=True
        )
        
        # The application should return non-zero exit code
        self.assertEqual(result.returncode, 1, 
                        f"Application did not return error code for non-existent file")
        
        # Check that the error message is in stderr
        self.assertIn(f"File not found: {non_existent_file}", result.stderr)

    def test_debug_output(self):
        """Test that the application produces debug output when debug logging is enabled."""
        # Import the piglet module directly
        import piglet
        import logging

        # Set the logger to DEBUG level
        logger = logging.getLogger(piglet.__name__)
        logger.setLevel(logging.DEBUG)

        # Create a mock args object with the file parameter
        import argparse
        args = argparse.Namespace()
        args.file = self.test_file.name

        # Capture stderr where log messages are sent
        output = io.StringIO()
        try:
            with redirect_stderr(output):
                piglet.main(args)
            result_stderr = output.getvalue()

            # Debug messages should be present
            self.assertIn("Application started", result_stderr, 
                         "Debug message 'Application started' not found in output")
            self.assertIn("Application completed successfully", result_stderr,
                         "Debug message 'Application completed successfully' not found in output")
        except Exception as e:
            self.fail(f"Failed to execute application in debug mode: {str(e)}")

    def test_return_code_success(self):
        """Test that the application returns 0 on successful execution."""
        result = subprocess.run(
            [sys.executable, "piglet.py", self.test_file.name],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0, 
                        f"Application did not return 0 on success. "
                        f"Return code: {result.returncode}, stderr: {result.stderr}")

    def test_exception_handling(self):
        """Test that the application handles exceptions properly and returns non-zero exit code."""
        # Create a temporary script that imports piglet and forces an exception
        with open("temp_exception_test.py", "w") as f:
            f.write("""
import piglet
import types

# Replace main function with one that raises an exception
original_main = piglet.main
def failing_main():
    raise Exception("Test exception")
piglet.main = failing_main

# Run the application
import sys
sys.exit(piglet.main())
""")
        
        try:
            result = subprocess.run(
                [sys.executable, "temp_exception_test.py"],
                capture_output=True,
                text=True
            )
            
            # Check that the application returns non-zero exit code on exception
            self.assertNotEqual(result.returncode, 0, 
                               "Application returned 0 despite an exception being raised")
            
            # Check that the error is logged
            self.assertIn("Test exception", result.stderr, 
                         "Exception message not found in stderr output")
            self.assertIn("Test exception", result.stderr, 
                         "Exception message not found in stderr output")
        finally:
            # Clean up temporary file
            if os.path.exists("temp_exception_test.py"):
                os.remove("temp_exception_test.py")


if __name__ == "__main__":
    unittest.main()