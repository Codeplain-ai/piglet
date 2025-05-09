#!/usr/bin/env python3
"""
Acceptance tests for the piglet application focusing on plural replacement.
"""
import unittest
import os
import sys
import tempfile
import subprocess

class PigletPluralReplacementTest(unittest.TestCase):
    """Test cases for verifying plural animal replacements in the piglet application."""

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

    def test_basic_plural_replacement(self):
        """Test that plural animal names are replaced with 'piglets'."""
        input_text = "The cows are in the field."
        expected_output = "The piglets are in the field."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to replace plural animals with 'piglets'.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_mixed_singular_and_plural(self):
        """Test text containing both singular and plural animal forms."""
        input_text = "One cow and five cows are in the field."
        expected_output = "One piglet and five piglets are in the field."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to correctly handle mixed singular and plural forms.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_multiple_plural_animals(self):
        """Test text containing multiple different plural animal forms."""
        input_text = "The cows, pigs, and chickens are on the farm."
        expected_output = "The piglets, piglets, and piglets are on the farm."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to replace multiple plural animal types.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_irregular_plurals(self):
        """Test handling of irregular plural forms like 'geese'."""
        input_text = "The geese are swimming in the pond."
        expected_output = "The piglets are swimming in the pond."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to handle irregular plural forms.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_same_singular_and_plural(self):
        """Test animals that have the same singular and plural form (like 'sheep')."""
        input_text = "One sheep and many sheep are in the field."
        expected_output = "One piglet and many piglets are in the field."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to correctly handle animals with same singular/plural form.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_plural_capitalization(self):
        """Test that plural replacements maintain proper capitalization."""
        input_text = "cows Cows COWS are all different capitalizations."
        expected_output = "piglets Piglets PIGLETS are all different capitalizations."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed to maintain capitalization in plural replacements.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_plural_at_different_positions(self):
        """Test plural forms at the beginning, middle, and end of sentences."""
        input_text = "Cows are here. The farmer feeds the pigs. Look at those chickens!"
        expected_output = "Piglets are here. The farmer feeds the piglets. Look at those piglets!"
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with plural animals in different positions.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_complex_plural_text(self):
        """Test with a complex text containing various plural animal references."""
        input_text = """On the farm, there were many animals:
- The cows grazed peacefully in the field
- Several pigs rolled in the mud
- A flock of chickens pecked at the ground
- The horses ran freely in the pasture
- Some sheep rested under the tree
- The geese swam in the pond
- Many goats climbed on the rocks"""
        expected_output = """On the farm, there were many animals:
- The piglets grazed peacefully in the field
- Several piglets rolled in the mud
- A flock of piglets pecked at the ground
- The piglets ran freely in the pasture
- Some piglets rested under the tree
- The piglets swam in the pond
- Many piglets climbed on the rocks"""
        
        output = self.run_app_with_input(input_text).rstrip()
        
        self.assertEqual(expected_output.rstrip(), output, 
                         f"Failed with complex plural text.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")

    def test_mixed_plurals_and_non_animals(self):
        """Test text with plural animals mixed with non-animal plural words."""
        input_text = "The cows eat grass while the farmers watch and the tractors work."
        expected_output = "The piglets eat grass while the farmers watch and the tractors work."
        
        output = self.run_app_with_input(input_text).strip()
        
        self.assertEqual(expected_output, output, 
                         f"Failed with mixed plural animals and non-animals.\nInput: '{input_text}'\nExpected: '{expected_output}'\nGot: '{output}'")


if __name__ == '__main__':
    unittest.main()