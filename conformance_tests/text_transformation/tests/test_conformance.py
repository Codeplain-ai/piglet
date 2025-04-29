"""
Conformance tests for the piglet application.
These tests verify that the application meets the functional requirements
by testing it as a black box through its command-line interface.
"""
import unittest
import os
import subprocess
import tempfile
import sys


class TestPigletConformance(unittest.TestCase):
    """Conformance tests for the piglet application."""

    def setUp(self):
        """Set up the test environment."""
        # Store the path to the piglet.py script
        self.app_path = os.path.join(os.getcwd(), "piglet.py")
        # Verify the script exists
        self.assertTrue(os.path.exists(self.app_path), 
                        f"Application not found at {self.app_path}")

    def run_app_with_input(self, input_text):
        """
        Run the application with the given input text and return its output.
        
        Args:
            input_text (str): Text to write to a temporary file for processing
            
        Returns:
            str: Standard output from the application
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file_path = temp_file.name
            # Write the input text to the file
            temp_file.write(input_text)
            
        try:
            # Run the application with the temporary file
            result = subprocess.run(
                [sys.executable, self.app_path, temp_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_basic_animal_replacement(self):
        """Test that a single animal name is replaced correctly."""
        input_text = "The cow is in the field."
        expected_output = "The piglet is in the field."
        
        output = self.run_app_with_input(input_text)
        
        self.assertEqual(output, expected_output, 
                         f"Failed to replace 'cow' with 'piglet'. Got: '{output}'")

    def test_plural_animal_replacement(self):
        """Test that plural animal names are replaced correctly."""
        input_text = "The cows are in the field."
        expected_output = "The piglets are in the field."
        
        output = self.run_app_with_input(input_text)
        
        self.assertEqual(output, expected_output, 
                         f"Failed to replace 'cows' with 'piglets'. Got: '{output}'")

    def test_case_preservation(self):
        """Test that case is preserved when replacing animal names."""
        input_text = "The cow, the COW, and the Cow are different cases."
        expected_output = "The piglet, the PIGLET, and the Piglet are different cases."
        
        output = self.run_app_with_input(input_text)
        
        self.assertEqual(output, expected_output, 
                         f"Failed to preserve case during replacement. Got: '{output}'")

    def test_multiple_animal_replacements(self):
        """Test that multiple different animal names are replaced correctly."""
        input_text = "The farm has cows, chickens, pigs, and horses."
        expected_output = "The farm has piglets, piglets, piglets, and piglets."
        
        output = self.run_app_with_input(input_text)
        
        self.assertEqual(output, expected_output, 
                         f"Failed to replace multiple animal names. Got: '{output}'")

    def test_no_animal_names(self):
        """Test that text without animal names remains unchanged."""
        input_text = "This text has no barnyard animals mentioned."
        expected_output = "This text has no barnyard animals mentioned."
        
        output = self.run_app_with_input(input_text)
        
        self.assertEqual(output, expected_output, 
                         f"Text without animal names was modified. Got: '{output}'")

    def test_word_boundaries(self):
        """Test that only complete animal names are replaced."""
        input_text = "The cowbell and the pigpen are not animals."
        expected_output = "The cowbell and the pigpen are not animals."
        
        output = self.run_app_with_input(input_text)
        
        self.assertEqual(output, expected_output, 
                         f"Parts of words were incorrectly replaced. Got: '{output}'")

    def test_capitalization_preservation_acceptance(self):
        """
        Acceptance test: Verify that capitalization of animal names is preserved in replacements.
        
        If the original animal is capitalized, the replacement should be capitalized.
        Similarly if the original is all-caps, the replacement should be all-caps.
        """
        test_cases = [
            # Format: (description, input_text, expected_output)
            (
                "lowercase animals",
                "The cow and chicken are in the barn.",
                "The piglet and piglet are in the barn."
            ),
            (
                "UPPERCASE animals",
                "The COW and CHICKEN are in the barn.",
                "The PIGLET and PIGLET are in the barn."
            ),
            (
                "Capitalized animals",
                "The Cow and Chicken are in the barn.",
                "The Piglet and Piglet are in the barn."
            ),
            (
                "mixed case animals",
                "The cOw and ChIcKeN are in the barn.",
                "The piglet and Piglet are in the barn."
            ),
            (
                "sentence with multiple capitalization patterns",
                "cow Cow COW cOw CoW are different capitalizations.",
                "piglet Piglet PIGLET piglet Piglet are different capitalizations."
            ),
            (
                "plural forms with different capitalizations",
                "cows Cows COWS are plural forms.",
                "piglets Piglets PIGLETS are plural forms."
            ),
            (
                "multiple animal types with different capitalizations",
                "cows CHICKENS Horses pIgS are different animals.",
                "piglets PIGLETS Piglets piglets are different animals."
            )
        ]
        
        for description, input_text, expected_output in test_cases:
            with self.subTest(description=description):
                output = self.run_app_with_input(input_text)
                self.assertEqual(output, expected_output, 
                                f"Failed to preserve capitalization for {description}.\n"
                                f"Input: '{input_text}'\n"
                                f"Expected: '{expected_output}'\n"
                                f"Got: '{output}'")


if __name__ == '__main__':
    unittest.main()