#!/usr/bin/env python3
"""
Acceptance tests for the piglet application focusing on capitalization preservation.
"""
import unittest
import os
import sys
import tempfile
import subprocess

class PigletCapitalizationTest(unittest.TestCase):
    """Test cases for verifying capitalization preservation in the piglet application."""

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

    def test_lowercase_animals(self):
        """Test that lowercase animal names are replaced with lowercase 'piglet'."""
        input_text = "The cow is in the field with a pig and a chicken."
        expected_output = "The piglet is in the field with a piglet and a piglet."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to preserve lowercase.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_capitalized_animals(self):
        """Test that capitalized animal names are replaced with capitalized 'Piglet'."""
        input_text = "Cow is in the field with Pig and Chicken."
        expected_output = "Piglet is in the field with Piglet and Piglet."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to preserve capitalization.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_uppercase_animals(self):
        """Test that ALL CAPS animal names are replaced with ALL CAPS 'PIGLET'."""
        input_text = "COW is in the field with PIG and CHICKEN."
        expected_output = "PIGLET is in the field with PIGLET and PIGLET."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to preserve uppercase.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_mixed_case_animals(self):
        """Test handling of mixed case animal names."""
        input_text = "cow Cow COW are all in the field."
        expected_output = "piglet Piglet PIGLET are all in the field."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with mixed case animals.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_plural_capitalization(self):
        """Test that plural forms follow the same capitalization rules."""
        input_text = "cows Cows COWS are all in the field."
        expected_output = "piglets Piglets PIGLETS are all in the field."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with plural capitalization.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_mixed_singular_plural_capitalization(self):
        """Test mixed singular and plural forms with different capitalizations."""
        input_text = "The cow and the COWS. Pig and PIGS. chicken and Chickens."
        expected_output = "The piglet and the PIGLETS. Piglet and PIGLETS. piglet and Piglets."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with mixed singular/plural capitalization.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_sentence_start_capitalization(self):
        """Test capitalization at the start of sentences."""
        input_text = "Cow is here. pig is there. CHICKEN is everywhere."
        expected_output = "Piglet is here. piglet is there. PIGLET is everywhere."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with sentence start capitalization.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_complex_capitalization_patterns(self):
        """Test with complex text containing various capitalization patterns."""
        input_text = """On the farm:
- cow, Cow, and COW
- pigs, Pigs, and PIGS
- A GOOSE and many Geese
- sheep and Sheep (both singular and plural)"""
        expected_output = """On the farm:
- piglet, Piglet, and PIGLET
- piglets, Piglets, and PIGLETS
- A PIGLET and many Piglets
- piglet and Piglet (both singular and plural)"""
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with complex capitalization patterns.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")


if __name__ == '__main__':
    unittest.main()