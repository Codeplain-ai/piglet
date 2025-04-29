#!/usr/bin/env python3
"""
Conformance tests for the piglet application.
These tests verify that the application meets the functional requirement:
- The App should take a file name of The Text File as the only positional argument.
"""
import unittest
import subprocess
import os
import tempfile
import sys


class TestPigletConformance(unittest.TestCase):
    """Conformance tests for the piglet application."""

    def setUp(self):
        """Set up test environment."""
        # Get the path to the piglet.py script
        self.app_path = os.path.join(os.getcwd(), "piglet.py")
        # Ensure the script exists
        self.assertTrue(os.path.exists(self.app_path), 
                        f"Application file not found at {self.app_path}")

    def run_app(self, args=None):
        """
        Run the piglet application with the given arguments.
        
        Args:
            args: List of command-line arguments to pass to the application
            
        Returns:
            tuple: (return_code, stdout, stderr)
        """
        cmd = [sys.executable, self.app_path]
        if args:
            cmd.extend(args)
            
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    def test_app_accepts_valid_file_path(self):
        """Test that the app accepts a valid file path as an argument."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = temp_file.name
        
        try:
            # Run the app with the temporary file path
            return_code, stdout, stderr = self.run_app([temp_file_path])
            
            # Check that the app ran successfully
            self.assertEqual(return_code, 0, 
                            f"App failed with valid file. Stderr: {stderr}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_app_fails_with_no_arguments(self):
        """Test that the app fails when no arguments are provided."""
        return_code, stdout, stderr = self.run_app([])
        
        # Check that the app failed
        self.assertNotEqual(return_code, 0, 
                           "App should fail when no arguments are provided")
        # Check that the error message mentions the missing argument
        self.assertIn("required", stderr.lower(), 
                     "Error message should indicate a required argument is missing")

    def test_app_fails_with_nonexistent_file(self):
        """Test that the app fails when the specified file doesn't exist."""
        # Generate a path that definitely doesn't exist
        nonexistent_file = os.path.join(
            tempfile.gettempdir(), 
            f"nonexistent_file_{os.urandom(8).hex()}.txt"
        )
        
        # Ensure the file doesn't exist
        if os.path.exists(nonexistent_file):
            os.unlink(nonexistent_file)
            
        return_code, stdout, stderr = self.run_app([nonexistent_file])
        
        # Check that the app failed
        self.assertEqual(return_code, 1, 
                        f"App should return code 1 for nonexistent file. Stderr: {stderr}")
        # Check that the error message mentions the file not found
        self.assertIn("not found", stderr.lower(), 
                     "Error message should indicate file not found")

    def test_app_fails_with_too_many_arguments(self):
        """Test that the app fails when too many arguments are provided."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Test content")
            temp_file_path = temp_file.name
        
        try:
            # Run the app with the temporary file path and an extra argument
            return_code, stdout, stderr = self.run_app([temp_file_path, "extra_arg"])
            
            # Check that the app failed
            self.assertNotEqual(return_code, 0, 
                              "App should fail when too many arguments are provided")
            # Check that the error message mentions the unexpected argument
            self.assertIn("unrecognized arguments", stderr.lower(), 
                         "Error message should indicate unexpected arguments")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_app_processes_valid_file(self):
        """Test that the app processes a valid file correctly."""
        # Create a temporary file with some content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Test content for processing")
            temp_file_path = temp_file.name
        
        try:
            # Run the app with the temporary file path
            return_code, stdout, stderr = self.run_app([temp_file_path])
            
            # Check that the app ran successfully
            self.assertEqual(return_code, 0, 
                            f"App should succeed with valid file. Stderr: {stderr}")
            # Check that the error output indicates the file was processed
            self.assertIn("processing file", stderr.lower(), 
                         "Output should indicate file processing")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()