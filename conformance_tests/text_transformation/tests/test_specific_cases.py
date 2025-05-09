#!/usr/bin/env python3
"""
Acceptance tests for the piglet application focusing on specific cases.
"""
import unittest
import os
import sys
import tempfile
import subprocess

class PigletSpecificCasesTest(unittest.TestCase):
    """Test cases for verifying specific text replacements in the piglet application."""

    def setUp(self):
        """Set up test environment."""
        # Store the path to the piglet.py script
        self.app_path = os.path.join(os.getcwd(), "piglet.py")
        # Ensure the script exists
        self.assertTrue(os.path.exists(self.app_path), 
                        f"Application file not found at {self.app_path}")

    def run_app_with_input(self, input_text):
        """
        Run the piglet application with the given input text.
        
        Args:
            input_text (str): The text to write to a temporary file
            
        Returns:
            str: The output from the application
        """
        # Create a temporary file with the input text
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(input_text)
            temp_file_path = temp_file.name
        
        try:
            # Run the application with the temporary file
            result = subprocess.run(
                [sys.executable, self.app_path, temp_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_sebastian_the_suffolk_sheep(self):
        """Test the specific case of 'Sebastian the Suffolk Sheep'."""
        input_text = "Sebastian the Suffolk Sheep"
        expected_output = "Sebastian the Suffolk Piglet"
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to correctly replace 'Sebastian the Suffolk Sheep'.\n"
                         f"Input: '{input_text}'\n"
                         f"Expected: '{expected_output}'\n"
                         f"Got: '{output}'\n"
                         f"This test verifies that proper nouns containing animal names are correctly processed.")

    def test_sebastian_in_context(self):
        """Test 'Sebastian the Suffolk Sheep' in a larger context."""
        input_text = "Once upon a time, Sebastian the Suffolk Sheep lived on a farm with other sheep."
        expected_output = "Once upon a time, Sebastian the Suffolk Piglet lived on a farm with other piglets."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to correctly replace 'Sebastian the Suffolk Sheep' in context.\n"
                         f"Input: '{input_text}'\n"
                         f"Expected: '{expected_output}'\n"
                         f"Got: '{output}'\n"
                         f"This test verifies that proper nouns containing animal names are correctly processed in context.")

    def test_multiple_named_animals(self):
        """Test multiple named animals in the same text."""
        input_text = "Sebastian the Suffolk Sheep and Clara the Chicken were friends with Gary the Goat."
        expected_output = "Sebastian the Suffolk Piglet and Clara the Piglet were friends with Gary the Piglet."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to correctly replace multiple named animals.\n"
                         f"Input: '{input_text}'\n"
                         f"Expected: '{expected_output}'\n"
                         f"Got: '{output}'\n"
                         f"This test verifies that multiple proper nouns containing animal names are correctly processed.")


if __name__ == '__main__':
    unittest.main()