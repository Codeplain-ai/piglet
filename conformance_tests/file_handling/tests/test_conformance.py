"""
Conformance tests for the piglet application.
These tests verify that the application correctly handles command-line arguments
as specified in the functional requirements.
"""
import unittest
import subprocess
import os
import tempfile
import sys


class TestCommandLineArguments(unittest.TestCase):
    """Test cases for verifying command-line argument handling."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"Test content")
        self.temp_file.close()
        
        # Path to the piglet.py script
        self.script_path = os.path.join(os.getcwd(), "piglet.py")
        
        # Ensure the script exists
        self.assertTrue(os.path.exists(self.script_path), 
                        f"Script not found at {self.script_path}")

    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_no_arguments(self):
        """Test that the application requires at least one argument."""
        # Run the application with no arguments
        result = subprocess.run(
            [sys.executable, self.script_path],
            capture_output=True,
            text=True
        )
        
        # Verify that the application exits with a non-zero status
        self.assertNotEqual(result.returncode, 0, 
                           "Application should fail when no arguments are provided")
        
        # Verify that the error message mentions the missing argument
        self.assertIn("required", result.stderr.lower(), 
                     "Error message should indicate a required argument is missing")

    def test_too_many_arguments(self):
        """Test that the application accepts only one positional argument."""
        # Run the application with two arguments
        result = subprocess.run(
            [sys.executable, self.script_path, "file1.txt", "file2.txt"],
            capture_output=True,
            text=True
        )
        
        # Verify that the application exits with a non-zero status
        self.assertNotEqual(result.returncode, 0, 
                           "Application should fail when too many arguments are provided")
        
        # Verify that the error message mentions the unexpected argument
        self.assertIn("unrecognized arguments", result.stderr.lower(), 
                     "Error message should indicate too many arguments were provided")

    def test_valid_file_path(self):
        """Test that the application accepts a valid file path."""
        # Run the application with a valid file path
        result = subprocess.run(
            [sys.executable, self.script_path, self.temp_file.name],
            capture_output=True,
            text=True
        )
        
        # Verify that the application exits with a zero status
        self.assertEqual(result.returncode, 0, 
                        f"Application should succeed with valid file path: {self.temp_file.name}")

        # Verify that the output indicates the file is being processed
        combined_output = (result.stdout + result.stderr).lower()
        self.assertIn("processing file", combined_output, 
                     "Output should indicate the file is being processed")

    def test_nonexistent_file(self):
        """Test that the application reports an error for a non-existent file."""
        # Create a path to a file that doesn't exist
        nonexistent_file = os.path.join(tempfile.gettempdir(), "nonexistent_file.txt")
        
        # Ensure the file doesn't exist
        if os.path.exists(nonexistent_file):
            os.unlink(nonexistent_file)
        
        # Run the application with a non-existent file path
        result = subprocess.run(
            [sys.executable, self.script_path, nonexistent_file],
            capture_output=True,
            text=True
        )
        
        # Verify that the application exits with a non-zero status
        self.assertNotEqual(result.returncode, 0, 
                           f"Application should fail with non-existent file: {nonexistent_file}")

        # Verify that the error message mentions the file not being found
        combined_output = (result.stdout + result.stderr).lower()
        self.assertIn("file not found", combined_output, 
                     "Output should indicate the file was not found")


if __name__ == '__main__':
    unittest.main()