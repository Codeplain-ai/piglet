#!/usr/bin/env python3
"""
Conformance tests for the piglet application.
"""
import unittest
import os
import sys
import tempfile
import subprocess
from io import StringIO

class PigletAppTest(unittest.TestCase):
    """Test cases for the piglet application."""

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

    def test_single_animal(self):
        """Test replacing a single barnyard animal."""
        input_text = "The cow is in the field."
        expected_output = "The piglet is in the field."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to replace single animal.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_multiple_same_animal(self):
        """Test replacing multiple instances of the same animal."""
        input_text = "The pig and the pig are playing."
        expected_output = "The piglet and the piglet are playing."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to replace multiple instances of the same animal.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_different_animals(self):
        """Test replacing different barnyard animals."""
        input_text = "The cow, the pig, and the chicken are on the farm."
        expected_output = "The piglet, the piglet, and the piglet are on the farm."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to replace different animals.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_singular_and_plural(self):
        """Test replacing both singular and plural forms of animals."""
        input_text = "The cow and the cows are mooing."
        expected_output = "The piglet and the piglets are mooing."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to handle singular and plural forms.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_capitalization_preservation(self):
        """Test that capitalization is preserved when replacing animals."""
        input_text = "Cow and cow. SHEEP and sheep."
        expected_output = "Piglet and piglet. PIGLET and piglet."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to preserve capitalization.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_mixed_text_and_animals(self):
        """Test with text containing both animals and non-animal words."""
        input_text = "The cow is eating grass while the farmer watches."
        expected_output = "The piglet is eating grass while the farmer watches."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with mixed text.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_animals_in_different_positions(self):
        """Test with animals at the beginning, middle, and end of sentences."""
        input_text = "Cow is here. The farmer feeds the chicken. Look at that sheep!"
        expected_output = "Piglet is here. The farmer feeds the piglet. Look at that piglet!"
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with animals in different positions.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_nonexistent_file(self):
        """Test application behavior with a non-existent file."""
        # Use a file path that definitely doesn't exist
        non_existent_file = "/path/to/nonexistent/file_that_does_not_exist.txt"
        
        # Run the application and expect it to fail
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.run(
                [sys.executable, self.app_path, non_existent_file],
                capture_output=True,
                text=True,
                check=True
            )
        
        # Check that the error output contains a relevant message
        self.assertIn("File not found", context.exception.stderr, 
                      "Application did not properly handle non-existent file")

    def test_complex_text(self):
        """Test with a more complex text containing multiple animal references."""
        input_text = """On the farm, there were many animals. 
The cows grazed in the field, while the pigs played in the mud.
A chicken and its chicks pecked at the ground, and the horses ran freely.
Even the sheep seemed happy, and the goats climbed on everything.
"""
        expected_output = """On the farm, there were many animals. 
The piglets grazed in the field, while the piglets played in the mud.
A piglet and its chicks pecked at the ground, and the piglets ran freely.
Even the piglet seemed happy, and the piglets climbed on everything.
"""
        
        output = self.run_app_with_input(input_text).rstrip()
        
        self.assertEqual(expected_output.rstrip(), output, 
                         f"Failed with complex text.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")


if __name__ == '__main__':
    unittest.main()