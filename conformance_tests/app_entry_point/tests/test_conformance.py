"""
Conformance tests for the console application entry point.
These tests verify that the application can be executed properly
and behaves as expected when run as a standalone script.
"""
import unittest
import subprocess
import sys
import os
import importlib

class TestApplicationEntryPoint(unittest.TestCase):
    """Test cases for verifying the application entry point functionality."""
    
    def setUp(self):
        """Create a temporary test file for the application to process."""
        self.test_file_path = "temp_test_file.txt"
        with open(self.test_file_path, "w") as f:
            f.write("This is a test file for the application.")
    
    def tearDown(self):
        """Clean up the temporary test file."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        # Also clean up any other temporary files created during tests
        if os.path.exists("temp_error_test.py"):
            os.remove("temp_error_test.py")

    def test_application_can_be_executed(self):
        """Test that the application can be executed as a standalone script."""
        try:
            result = subprocess.run(
                [sys.executable, "piglet.py", self.test_file_path],
                capture_output=True,
                text=True,
                check=False
            )
            self.assertEqual(result.returncode, 0, 
                f"Application failed to execute with error: {result.stderr}")
        except FileNotFoundError:
            self.fail("Application file 'piglet.py' not found in the current directory")
        except Exception as e:
            self.fail(f"Failed to execute application: {str(e)}")

    def test_application_returns_success_exit_code(self):
        """Test that the application returns exit code 0 on successful execution."""
        result = subprocess.run(
            [sys.executable, "piglet.py", self.test_file_path],
            capture_output=True,
            text=True,
            check=False
        )
        self.assertEqual(result.returncode, 0, 
            f"Application did not return success exit code. Got {result.returncode} instead. Error: {result.stderr}")

    def test_application_produces_expected_output(self):
        """Test that the application produces expected output when executed."""
        result = subprocess.run(
            [sys.executable, "piglet.py", self.test_file_path],
            capture_output=True,
            text=True,
            check=False
        )
        # Check that stderr contains the expected log message
        self.assertIn(f"Processing file: {self.test_file_path}", result.stderr,
            f"Application did not produce expected log output. Got: {result.stderr}")

    def test_application_can_be_imported(self):
        """Test that the application can be imported as a module without executing main."""
        try:
            # Temporarily remove the application directory from sys.path if it's there
            # to ensure we're importing the right module
            cwd = os.getcwd()
            if cwd in sys.path:
                sys.path.remove(cwd)
            sys.path.insert(0, cwd)
            
            # Import the module
            module = importlib.import_module("piglet")
            
            # Check that the module has the expected attributes
            self.assertTrue(hasattr(module, "main"), 
                "Application module does not have a 'main' function")
            self.assertTrue(hasattr(module, "setup_logging"), 
                "Application module does not have a 'setup_logging' function")
            
        except ImportError:
            self.fail("Failed to import application module 'piglet'")
        except Exception as e:
            self.fail(f"Unexpected error when importing application module: {str(e)}")

    def test_error_handling(self):
        """Test that the application handles errors gracefully."""
        # Test with a non-existent file
        non_existent_file = "non_existent_file.txt"
        
        # Make sure the file doesn't exist
        if os.path.exists(non_existent_file):
            os.remove(non_existent_file)
            
        result = subprocess.run(
            [sys.executable, "piglet.py", non_existent_file],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Check that it returns a non-zero exit code
        self.assertEqual(result.returncode, 1, 
            "Application did not return error exit code when given a non-existent file")
        
        # Also test with a script that raises an exception
        with open("temp_error_test.py", "w") as f:
            f.write("""
import sys
def main():
    raise Exception("Test exception")
if __name__ == "__main__":
    sys.exit(main())
""")
        
        result = subprocess.run(
            [sys.executable, "temp_error_test.py"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Check that it returns a non-zero exit code
        self.assertNotEqual(result.returncode, 0, 
            "Application did not return error exit code when an exception was raised")


if __name__ == '__main__':
    unittest.main()
