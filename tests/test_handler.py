import time
from unittest.mock import patch

from feedify.handler import FeedifyHandler


@patch('feedify.handler.Path.exists', return_value=False)
def test_needs_refresh_no_file(mock_exists):
    assert FeedifyHandler.needs_refresh('https://www.example.com/')


@patch('feedify.handler.Path')
def test_needs_refresh_overdue(mock_path):
    mock_path.return_value.exists.return_value = True
    mock_path.return_value.stat.return_value.st_mtime = time.time() - (60 * 16)

    assert FeedifyHandler.needs_refresh('https://www.example.com/')


@patch('feedify.handler.Path')
def test_needs_refresh_too_soon(mock_path):
    mock_path.return_value.exists.return_value = True
    mock_path.return_value.stat.return_value.st_mtime = time.time()

    assert not FeedifyHandler.needs_refresh('https://www.example.com/')

