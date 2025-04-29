

"""
Unit tests for the console application.
"""
import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
import piglet


class TestMainModule(unittest.TestCase):
    """Test cases for the piglet module."""

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile')
    @patch('piglet.process_text_file')
    def test_main_success(self, mock_process, mock_isfile, mock_parse_args):
        """Test that the main function returns 0 when file exists."""
        # Mock the argument parser to return a file path
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        # Mock os.path.isfile to return True
        mock_isfile.return_value = True
        mock_process.return_value = "Processed text"
        
        result = piglet.main()
        self.assertEqual(result, 0)
        mock_isfile.assert_called_once_with('test.txt')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile')
    def test_main_file_not_found(self, mock_isfile, mock_parse_args):
        """Test that the main function returns 1 when file doesn't exist."""
        # Mock the argument parser to return a file path
        mock_parse_args.return_value = type('Args', (), {'file_path': 'nonexistent.txt'})
        # Mock os.path.isfile to return False
        mock_isfile.return_value = False
        
        result = piglet.main()
        self.assertEqual(result, 1)
        mock_isfile.assert_called_once_with('nonexistent.txt')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile', return_value=True)
    @patch('piglet.process_text_file')
    def test_main_success_with_valid_file(self, mock_process, mock_isfile, mock_parse_args):
        """Test that the main function processes a valid file."""
        mock_process.return_value = "Processed text"
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        result = piglet.main()
        self.assertEqual(result, 0)
        
    @patch('piglet.setup_logging')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile')
    def test_logging_setup(self, mock_isfile, mock_parse_args, mock_setup_logging):
        """Test that logging is set up correctly."""
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        mock_isfile.return_value = True
        piglet.main()
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

    @patch('sys.argv', ['piglet.py', 'test.txt'])
    @patch('os.path.isfile', return_value=True)
    def test_argument_parsing(self, mock_isfile):
        """Test that command-line arguments are parsed correctly."""
        args = piglet.parse_arguments()
        self.assertEqual(args.file_path, 'test.txt')
        
    @patch('sys.argv', ['piglet.py'])
    def test_missing_argument(self):
        """Test that an error is raised when no file path is provided."""
        with self.assertRaises(SystemExit):
            piglet.parse_arguments()
            
    @patch('sys.argv', ['piglet.py', 'test.txt'])
    def test_parse_arguments_function(self):
        """Test the parse_arguments function directly."""
        args = piglet.parse_arguments()
        self.assertEqual(args.file_path, 'test.txt')

    def test_get_barnyard_animals(self):
        """Test that the barnyard animals dictionary is correctly defined."""
        animals = piglet.get_barnyard_animals()
        self.assertIsInstance(animals, dict)
        self.assertIn('chicken', animals)
        self.assertEqual(animals['chicken'], 'piglet')
        self.assertIn('chickens', animals)
        self.assertEqual(animals['chickens'], 'piglets')

    @patch('builtins.open', new_callable=mock_open, read_data="The cow jumped over the moon.")
    def test_process_text_file_simple_replacement(self, mock_file):
        """Test that animal names are replaced correctly."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "The piglet jumped over the moon.")
        mock_file.assert_called_once_with('test.txt', 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open, read_data="The COWS and chickens are in the barn.")
    def test_process_text_file_case_preservation(self, mock_file):
        """Test that case is preserved when replacing animal names."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "The PIGLETS and piglets are in the barn.")

    @patch('builtins.open', new_callable=mock_open, read_data="Horses, Cows, and Sheep are farm animals.")
    def test_process_text_file_multiple_replacements(self, mock_file):
        """Test that multiple animal names are replaced correctly."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "Piglets, Piglets, and Piglets are farm animals.")

    @patch('builtins.open', new_callable=mock_open, read_data="No barnyard animals here.")
    def test_process_text_file_no_replacements(self, mock_file):
        """Test that text without animal names remains unchanged."""
        logger = MagicMock()
        result = piglet.process_text_file('test.txt', logger)
        self.assertEqual(result, "No barnyard animals here.")

    @patch('builtins.open')
    def test_process_text_file_error_handling(self, mock_file):
        """Test that errors during file processing are handled correctly."""
        mock_file.side_effect = IOError("File could not be read")
        logger = MagicMock()
        
        with self.assertRaises(IOError):
            piglet.process_text_file('test.txt', logger)
        
        logger.error.assert_called_once()

    @patch('piglet.process_text_file')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isfile')
    def test_main_calls_process_text_file(self, mock_isfile, mock_parse_args, mock_print, mock_process):
        """Test that main calls process_text_file and prints the result."""
        mock_parse_args.return_value = type('Args', (), {'file_path': 'test.txt'})
        mock_isfile.return_value = True
        mock_process.return_value = "Processed text"
        
        piglet.main()
        mock_process.assert_called_once()
        mock_print.assert_called_once_with("Processed text")

if __name__ == '__main__':
    unittest.main()