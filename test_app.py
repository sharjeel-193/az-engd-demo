import pytest
import azure.functions as func
from unittest.mock import Mock, patch
import logging

# Import the functions from your main file
# Assuming your main file is named function_app.py
# from function_app import http_trigger, BlobTrigger


class TestHttpTrigger:
    """Test cases for the HTTP trigger function"""
    
    def test_http_trigger_with_name_in_query(self):
        """Test HTTP trigger with name parameter in query string"""
        # Arrange
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/http_trigger',
            params={'name': 'Azure'}
        )
        
        # Act
        from function_app import http_trigger
        response = http_trigger(req)
        
        # Assert
        assert response.status_code == 200
        assert "Hello, Azure" in response.get_body().decode()
    
    def test_http_trigger_with_name_in_body(self):
        """Test HTTP trigger with name parameter in request body"""
        # Arrange
        req = func.HttpRequest(
            method='POST',
            body=b'{"name": "GitHub"}',
            url='/api/http_trigger',
            params={}
        )
        
        # Act
        from function_app import http_trigger
        response = http_trigger(req)
        
        # Assert
        assert response.status_code == 200
        assert "Hello, GitHub" in response.get_body().decode()
    
    def test_http_trigger_without_name(self):
        """Test HTTP trigger without name parameter"""
        # Arrange
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/http_trigger',
            params={}
        )
        
        # Act
        from function_app import http_trigger
        response = http_trigger(req)
        
        # Assert
        assert response.status_code == 200
        assert "Pass a name in the query string" in response.get_body().decode()


class TestBlobTrigger:
    """Test cases for the Blob trigger function"""
    
    def test_blob_trigger_processes_blob(self):
        """Test blob trigger function processes blob correctly"""
        # Arrange
        mock_blob = Mock(spec=func.InputStream)
        mock_blob.name = "test-blob.txt"
        mock_blob.length = 1024
        
        # Act
        from function_app import BlobTrigger
        with patch('logging.info') as mock_logging:
            BlobTrigger(mock_blob)
            
            # Assert
            mock_logging.assert_called_once()
            call_args = mock_logging.call_args[0][0]
            assert "test-blob.txt" in call_args
            assert "1024" in call_args
    
    def test_blob_trigger_with_empty_blob(self):
        """Test blob trigger with empty blob"""
        # Arrange
        mock_blob = Mock(spec=func.InputStream)
        mock_blob.name = "empty-blob.txt"
        mock_blob.length = 0
        
        # Act
        from function_app import BlobTrigger
        with patch('logging.info') as mock_logging:
            BlobTrigger(mock_blob)
            
            # Assert
            mock_logging.assert_called_once()
            call_args = mock_logging.call_args[0][0]
            assert "empty-blob.txt" in call_args
            assert "0 bytes" in call_args


if __name__ == "__main__":
    pytest.main([__file__, "-v"])