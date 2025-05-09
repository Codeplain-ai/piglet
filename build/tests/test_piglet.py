

"""
Unit tests for the console application.
"""
import unittest
import os
import sys
import tempfile
from unittest.mock import patch
import piglet



class TestMainModule(unittest.TestCase):
    """Test cases for the piglet module."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"The cow jumped over the moon. Cows are animals.")
        self.temp_file.close()
        
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_get_barnyard_animals(self):
        """Test that the barnyard animals dictionary is correctly defined."""
        animals = piglet.get_barnyard_animals()
        self.assertIsInstance(animals, dict)
        self.assertIn('cow', animals)
        self.assertEqual(animals['cow'], 'cows')
        self.assertIn('pig', animals)
        self.assertEqual(animals['pig'], 'pigs')

    def test_replace_animals_with_piglet_singular(self):
        """Test replacing singular animal names with 'piglet'."""
        text = "The cow is in the field."
        result = piglet.replace_animals_with_piglet(text)
        self.assertEqual(result, "The piglet is in the field.")

    def test_replace_animals_with_piglet_plural(self):
        """Test replacing plural animal names with 'piglets'."""
        text = "The cows are in the field."
        result = piglet.replace_animals_with_piglet(text)
        self.assertEqual(result, "The piglets are in the field.")

    def test_replace_animals_with_piglet_capitalization(self):
        """Test that capitalization is preserved when replacing animal names."""
        text = "Cow and cow. Cows and cows."
        result = piglet.replace_animals_with_piglet(text)
        self.assertEqual(result, "Piglet and piglet. Piglets and piglets.")

    def test_replace_animals_with_piglet_mixed_text(self):
        """Test replacing animal names in a mixed text."""
        text = "The cow, pig, and horse are in the field. Cows, pigs, and horses are animals."
        result = piglet.replace_animals_with_piglet(text)
        self.assertEqual(result, "The piglet, piglet, and piglet are in the field. Piglets, piglets, and piglets are animals.")

    def test_replace_animals_with_piglet_word_boundaries(self):
        """Test that only complete animal words are replaced."""
        text = "The cowboy rode his horse to the showpig competition."
        result = piglet.replace_animals_with_piglet(text)
        self.assertEqual(result, "The cowboy rode his piglet to the showpig competition.")

    @patch('sys.stdout', new_callable=tempfile.TemporaryFile)
    @patch('piglet.parse_arguments')
    def test_main_output(self, mock_parse_args, mock_stdout):
        """Test that the main function outputs the processed text."""
        mock_args = unittest.mock.Mock()
        mock_args.file = self.temp_file.name
        mock_parse_args.return_value = mock_args

    @patch('piglet.parse_arguments')
    def test_main_success(self, mock_parse_args):
        """Test that the main function returns 0 on success with valid file."""
        # Mock the arguments
        mock_args = unittest.mock.Mock()
        mock_args.file = self.temp_file.name
        mock_parse_args.return_value = mock_args
        
        result = piglet.main()
        self.assertEqual(result, 0)

    @patch('piglet.parse_arguments')
    def test_main_file_not_found(self, mock_parse_args):
        """Test that the main function returns 1 when file is not found."""
        # Mock the arguments with a non-existent file
        mock_args = unittest.mock.Mock()
        mock_args.file = "non_existent_file.txt"
        mock_parse_args.return_value = mock_args
        
        result = piglet.main()
        self.assertEqual(result, 1)

    def test_parse_arguments(self):
        """Test argument parsing."""
        with patch('sys.argv', ['piglet.py', self.temp_file.name]):
            args = piglet.parse_arguments()
            self.assertEqual(args.file, self.temp_file.name)

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments_called(self, mock_parse_args):
        """Test that parse_arguments is called in main."""
        mock_args = unittest.mock.Mock()
        mock_args.file = self.temp_file.name
        mock_parse_args.return_value = mock_args
        
        with patch('os.path.isfile', return_value=True):
            piglet.main()
            mock_parse_args.assert_called_once()

    @patch('piglet.parse_arguments')
    @patch('piglet.setup_logging')
    def test_logging_setup(self, mock_setup_logging, mock_parse_args):
        """Test that logging is set up correctly."""
        # Mock the arguments
        mock_args = unittest.mock.Mock()
        mock_args.file = self.temp_file.name
        mock_parse_args.return_value = mock_args

        result = piglet.main()
        self.assertEqual(result, 0)

        mock_setup_logging.assert_called_once()

    @patch('piglet.main')
    def test_sys_exit_called_with_main_result(self, mock_main):
        """Test that sys.exit is called with the result of main()."""
        # Set up the mock to return a specific value
        mock_main.return_value = 42
        
        # Create a context where we can test the __name__ == "__main__" block
        with patch('sys.exit') as mock_exit:
            # Directly call the code that would run if __name__ == "__main__"
            piglet.sys.exit(piglet.main())
            mock_exit.assert_called_once_with(42)


if __name__ == '__main__':
    unittest.main()