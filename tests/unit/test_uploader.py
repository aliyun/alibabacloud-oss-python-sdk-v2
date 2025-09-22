import unittest
from unittest.mock import Mock
from alibabacloud_oss_v2.uploader import _UploaderDelegate, Uploader, UploadAPIClient, UploaderOptions
from alibabacloud_oss_v2 import models

class TestUpdateProgress(unittest.TestCase):
    """Unit test class for _update_progress method"""

    def setUp(self):
        """Test preparation"""
        # Create required mock objects
        base = Mock(spec=Uploader)
        client = Mock(spec=UploadAPIClient)

        # Create actual UploaderOptions object instead of mock
        options = UploaderOptions(
            part_size=1024 * 1024,  # 1MB
            parallel_num=3,
            leave_parts_on_error=False,
            enable_checkpoint=False,
            checkpoint_dir=None
        )

        # Create request object
        request = models.PutObjectRequest(
            bucket='test-bucket',
            key='test-key'
        )

        # Create _UploaderDelegate instance
        self.uploader_delegate = _UploaderDelegate(
            base=base,
            client=client,
            request=request,
            options=options
        )

        # Initialize necessary attributes
        self.uploader_delegate._transferred = 0
        self.uploader_delegate._total_size = 1000
        self.uploader_delegate._request = request
        self.uploader_delegate._request.progress_fn = None

    def test_update_progress_with_lock_and_callback(self):
        """Test case with progress lock and callback function"""
        # Set test data
        increment = 100

        # Create Mock lock object
        mock_lock = Mock()
        mock_lock.__enter__ = Mock(return_value=mock_lock)
        mock_lock.__exit__ = Mock(return_value=None)

        # Set uploader delegate attributes
        self.uploader_delegate._progress_lock = mock_lock
        callback_mock = Mock()
        self.uploader_delegate._request.progress_fn = callback_mock

        # Call the method under test
        self.uploader_delegate._update_progress(increment)

        # Verify results
        # 1. Verify lock usage
        mock_lock.__enter__.assert_called_once()
        mock_lock.__exit__.assert_called_once()
        # 2. Verify transferred bytes update
        self.assertEqual(self.uploader_delegate._transferred, increment)
        # 3. Verify callback function is called
        callback_mock.assert_called_once_with(increment, increment, self.uploader_delegate._total_size)

    def test_update_progress_with_lock_no_callback(self):
        """Test case with progress lock but no callback function"""
        # Set test data
        increment = 50

        # Create Mock lock object
        mock_lock = Mock()
        mock_lock.__enter__ = Mock(return_value=mock_lock)
        mock_lock.__exit__ = Mock(return_value=None)

        # Set uploader delegate attributes
        self.uploader_delegate._progress_lock = mock_lock
        self.uploader_delegate._request.progress_fn = None

        # Call the method under test
        self.uploader_delegate._update_progress(increment)

        # Verify results
        # 1. Verify lock usage
        mock_lock.__enter__.assert_called_once()
        mock_lock.__exit__.assert_called_once()
        # 2. Verify transferred bytes update
        self.assertEqual(self.uploader_delegate._transferred, increment)
        # 3. Verify callback function is not called
        self.assertIsNone(self.uploader_delegate._request.progress_fn)

    def test_update_progress_without_lock_with_callback(self):
        """Test case without progress lock but with callback function"""
        # Set test data
        increment = 200

        # Set uploader delegate attributes
        self.uploader_delegate._progress_lock = None
        callback_mock = Mock()
        self.uploader_delegate._request.progress_fn = callback_mock

        # Call the method under test
        self.uploader_delegate._update_progress(increment)

        # Verify results
        # 1. Verify transferred bytes update
        self.assertEqual(self.uploader_delegate._transferred, increment)
        # 2. Verify callback function is called
        callback_mock.assert_called_once_with(increment, increment, self.uploader_delegate._total_size)

    def test_update_progress_without_lock_no_callback(self):
        """Test case without progress lock and callback function"""
        # Set test data
        increment = 75

        # Set uploader delegate attributes
        self.uploader_delegate._progress_lock = None
        self.uploader_delegate._request.progress_fn = None

        # Call the method under test
        self.uploader_delegate._update_progress(increment)

        # Verify results
        # 1. Verify transferred bytes update
        self.assertEqual(self.uploader_delegate._transferred, increment)
        # 2. Verify callback function is not called
        self.assertIsNone(self.uploader_delegate._request.progress_fn)

    def test_update_progress_multiple_calls(self):
        """Test multiple calls to _update_progress method"""
        # Set uploader delegate attributes
        self.uploader_delegate._progress_lock = None
        callback_mock = Mock()
        self.uploader_delegate._request.progress_fn = callback_mock

        # Call the method under test multiple times
        increments = [100, 50, 25]
        expected_transferred = 0

        for increment in increments:
            expected_transferred += increment
            self.uploader_delegate._update_progress(increment)

            # Verify state after each call
            self.assertEqual(self.uploader_delegate._transferred, expected_transferred)

        # Verify callback function is called the correct number of times
        self.assertEqual(callback_mock.call_count, len(increments))

        # Verify parameters of the last call
        callback_mock.assert_called_with(increments[-1], expected_transferred, self.uploader_delegate._total_size)


if __name__ == '__main__':
    unittest.main()
