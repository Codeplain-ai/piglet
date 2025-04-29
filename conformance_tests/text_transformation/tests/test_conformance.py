"""
Conformance tests for the piglet application.
These tests verify that the application meets the functional requirements
by testing it through its command-line interface.
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
        # Ensure the script exists
        self.assertTrue(os.path.exists(self.app_path), 
                        f"Application file not found at {self.app_path}")

    def run_app(self, input_file_path):
        """
        Run the piglet application with the given input file.
        
        Args:
            input_file_path: Path to the input file
            
        Returns:
            tuple: (stdout, stderr, return_code)
        """
        result = subprocess.run(
            [sys.executable, self.app_path, input_file_path],
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr, result.returncode

    def create_temp_file(self, content):
        """
        Create a temporary file with the given content.
        
        Args:
            content: Content to write to the file
            
        Returns:
            str: Path to the temporary file
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_basic_replacement(self):
        """Test that a single barnyard animal is replaced with 'piglet'."""
        # Create a temporary file with a single animal
        input_content = "The cow jumped over the moon."
        expected_output = "The piglet jumped over the moon."
        
        temp_file_path = self.create_temp_file(input_content)
        try:
            stdout, stderr, return_code = self.run_app(temp_file_path)
            self.assertEqual(return_code, 0, f"Application failed with error: {stderr}")
            self.assertEqual(stdout, expected_output, 
                            f"Expected '{expected_output}', got '{stdout}'")
        finally:
            os.unlink(temp_file_path)

    def test_plural_replacement(self):
        """Test that plural forms of barnyard animals are replaced with 'piglets'."""
        # Create a temporary file with plural animals
        input_content = "The cows were grazing in the field."
        expected_output = "The piglets were grazing in the field."
        
        temp_file_path = self.create_temp_file(input_content)
        try:
            stdout, stderr, return_code = self.run_app(temp_file_path)
            self.assertEqual(return_code, 0, f"Application failed with error: {stderr}")
            self.assertEqual(stdout, expected_output, 
                            f"Expected '{expected_output}', got '{stdout}'")
        finally:
            os.unlink(temp_file_path)

    def test_case_preservation(self):
        """Test that the case of the original text is preserved in replacements."""
        # Create a temporary file with different cases
        input_content = "COWS and Horses and chickens"
        expected_output = "PIGLETS and Piglets and piglets"
        
        temp_file_path = self.create_temp_file(input_content)
        try:
            stdout, stderr, return_code = self.run_app(temp_file_path)
            self.assertEqual(return_code, 0, f"Application failed with error: {stderr}")
            self.assertEqual(stdout, expected_output, 
                            f"Expected '{expected_output}', got '{stdout}'")
        finally:
            os.unlink(temp_file_path)

    def test_multiple_animals(self):
        """Test that multiple different animals in the same text are all replaced."""
        # Create a temporary file with multiple animals
        input_content = "The cow, chicken, and horse were in the barn."
        expected_output = "The piglet, piglet, and piglet were in the barn."
        
        temp_file_path = self.create_temp_file(input_content)
        try:
            stdout, stderr, return_code = self.run_app(temp_file_path)
            self.assertEqual(return_code, 0, f"Application failed with error: {stderr}")
            self.assertEqual(stdout, expected_output, 
                            f"Expected '{expected_output}', got '{stdout}'")
        finally:
            os.unlink(temp_file_path)

    def test_no_animals(self):
        """Test that text without any barnyard animals remains unchanged."""
        # Create a temporary file with no animals
        input_content = "The cat and dog were playing."
        expected_output = "The cat and dog were playing."
        
        temp_file_path = self.create_temp_file(input_content)
        try:
            stdout, stderr, return_code = self.run_app(temp_file_path)
            self.assertEqual(return_code, 0, f"Application failed with error: {stderr}")
            self.assertEqual(stdout, expected_output, 
                            f"Expected '{expected_output}', got '{stdout}'")
        finally:
            os.unlink(temp_file_path)

    def test_empty_file(self):
        """Test that an empty file is processed correctly."""
        # Create an empty temporary file
        input_content = ""
        expected_output = ""
        
        temp_file_path = self.create_temp_file(input_content)
        try:
            stdout, stderr, return_code = self.run_app(temp_file_path)
            self.assertEqual(return_code, 0, f"Application failed with error: {stderr}")
            self.assertEqual(stdout, expected_output, 
                            f"Expected empty output, got '{stdout}'")
        finally:
            os.unlink(temp_file_path)

    def test_missing_file(self):
        """Test that the application handles missing files appropriately."""
        # Use a non-existent file path
        non_existent_file = "/path/to/nonexistent/file.txt"
        
        stdout, stderr, return_code = self.run_app(non_existent_file)
        self.assertNotEqual(return_code, 0, 
                           f"Expected non-zero return code for missing file")

    def test_capitalization_preservation(self):
        """
        Test that capitalization of animal names is preserved in replacements.
        
        Acceptance test: If the original animal is capitalized, the replacement should be
        capitalized. Similarly if the original is all-caps, the replacement should
        be all-caps.
        """
        # Create a temporary file with different capitalization patterns
        input_content = (
            "cow COW Cow\n"
            "horse HORSE Horse\n"
            "chicken CHICKEN Chicken\n"
            "cows COWS Cows\n"
            "horses HORSES Horses\n"
            "chickens CHICKENS Chickens"
        )
        
        expected_output = (
            "piglet PIGLET Piglet\n"
            "piglet PIGLET Piglet\n"
            "piglet PIGLET Piglet\n"
            "piglets PIGLETS Piglets\n"
            "piglets PIGLETS Piglets\n"
            "piglets PIGLETS Piglets"
        )
        
        temp_file_path = self.create_temp_file(input_content)
        try:
            stdout, stderr, return_code = self.run_app(temp_file_path)
            self.assertEqual(return_code, 0, 
                            f"Application failed with error: {stderr}")
            
            # Compare line by line for better error messages
            actual_lines = stdout.strip().split('\n')
            expected_lines = expected_output.strip().split('\n')
            
            self.assertEqual(len(actual_lines), len(expected_lines), 
                            f"Expected {len(expected_lines)} lines, got {len(actual_lines)}")
            
            for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
                self.assertEqual(actual, expected, 
                                f"Line {i+1} mismatch:\nExpected: '{expected}'\nActual: '{actual}'")
        finally:
            os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()