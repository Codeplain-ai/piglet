#!/usr/bin/env python3
"""
Conformance tests for the piglet.py application.
Tests that the app correctly handles file arguments.
"""
import unittest
import os
import sys
import tempfile
import subprocess
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

class TestPigletApp(unittest.TestCase):
    """Test suite for the piglet.py application."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.temp_file.write(b"Test content")
        self.temp_file.close()
        
        # Path to the piglet.py script
        self.app_path = os.path.join(os.getcwd(), "piglet.py")
        
        # Verify the app exists
        self.assertTrue(os.path.exists(self.app_path), 
                        f"Application not found at {self.app_path}")

    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary file
        if hasattr(self, 'temp_file') and os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def run_app(self, args=None):
        """
        Run the piglet.py application with the given arguments.
        
        Args:
            args: List of command-line arguments to pass to the app
            
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

    def test_valid_file_argument(self):
        """Test that the app accepts a valid file name and processes it successfully."""
        # Run the app with a valid file
        return_code, stdout, stderr = self.run_app([self.temp_file.name])
        
        # Check that the app ran successfully
        self.assertEqual(return_code, 0, 
                         f"App should return 0 for valid file, got {return_code}. Stderr: {stderr}")
        
        # Check that the app logged processing the file (logging outputs to stderr by default)
        self.assertIn(f"Processing file: {self.temp_file.name}", stderr, 
                      f"App should log processing the file. Got stderr: {stderr}")

    def test_nonexistent_file_argument(self):
        """Test that the app returns an error when the file doesn't exist."""
        # Use a file name that doesn't exist
        nonexistent_file = "nonexistent_file_12345.txt"
        
        # Make sure the file really doesn't exist
        if os.path.exists(nonexistent_file):
            os.unlink(nonexistent_file)
        
        # Run the app with a nonexistent file
        return_code, stdout, stderr = self.run_app([nonexistent_file])
        
        # Check that the app returned an error
        self.assertEqual(return_code, 1, 
                         f"App should return 1 for nonexistent file, got {return_code}")
        
        # Check that the app logged an error about the file not found
        self.assertIn("File not found", stderr, 
                      f"App should log 'File not found' error. Got stderr: {stderr}")

    def test_no_arguments(self):
        """Test that the app requires a file argument."""
        # Run the app with no arguments
        return_code, stdout, stderr = self.run_app([])
        
        # Check that the app returned an error
        self.assertNotEqual(return_code, 0, 
                           f"App should return non-zero when no arguments provided, got {return_code}")
        
        # Check that the app showed usage information
        self.assertIn("usage:", stderr.lower(), 
                      f"App should show usage information. Got stderr: {stderr}")

    def test_too_many_arguments(self):
        """Test that the app accepts only one positional argument."""
        # Run the app with two file arguments
        return_code, stdout, stderr = self.run_app([self.temp_file.name, "second_file.txt"])
        
        # Check that the app returned an error
        self.assertNotEqual(return_code, 0, 
                           f"App should return non-zero when too many arguments provided, got {return_code}")
        
        # Check that the app showed usage information
        self.assertIn("usage:", stderr.lower(), 
                      f"App should show usage information. Got stderr: {stderr}")

if __name__ == "__main__":
    unittest.main()