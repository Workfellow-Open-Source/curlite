from unittest.mock import patch, MagicMock
from curlite.lib import CurlWrapper, Response
import pytest
from curlite import exceptions

@patch("curlite.lib.subprocess.run")
def test_get_request(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="HTTP/1.1 200 OK\n\nHello, World!")
    curl = CurlWrapper()
    response = curl.get("http://example.com")
    assert response.status_code == 200
    assert response.reason == "OK"
    assert response.content == "Hello, World!"


@patch("curlite.lib.subprocess.run")
def test_post_request(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="HTTP/1.1 201 Created\n\n")
    curl = CurlWrapper()
    response = curl.post("http://example.com", data="key=value")
    assert response.status_code == 201
    assert response.reason == "Created"
    assert response.content == ""


@patch("curlite.lib.subprocess.run")
def test_put_request(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="HTTP/1.1 204 No Content\n\n")
    curl = CurlWrapper()
    response = curl.put("http://example.com", data="key=value")
    assert response.status_code == 204
    assert response.reason == "No Content"
    assert response.content == ""


@patch("curlite.lib.subprocess.run")
def test_delete_request(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="HTTP/1.1 204 No Content\n\n")
    curl = CurlWrapper()
    response = curl.delete("http://example.com")
    assert response.status_code == 204
    assert response.reason == "No Content"
    assert response.content == ""


@patch("curlite.lib.subprocess.run")
def test_request_with_params(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="HTTP/1.1 200 OK\n\nHello, World!")
    curl = CurlWrapper()
    response = curl.get("http://example.com", params={"key": "value"})
    assert response.status_code == 200
    assert response.reason == "OK"
    assert response.content == "Hello, World!"


@patch("curlite.lib.subprocess.run")
def test_request_with_headers(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="HTTP/1.1 200 OK\n\nHello, World!")
    curl = CurlWrapper()
    response = curl.get("http://example.com", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.reason == "OK"
    assert response.content == "Hello, World!"


@patch("curlite.lib.subprocess.run")
def test_request_with_timeout(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="HTTP/1.1 200 OK\n\nHello, World!")
    curl = CurlWrapper()
    response = curl.get("http://example.com", timeout=10)
    assert response.status_code == 200
    assert response.reason == "OK"
    assert response.content == "Hello, World!"


class TestCurlResponse:
    def test_json_method_with_valid_json(self):
        response = Response("http:\\example.com", 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"name": "John", "age": 30}')
        assert response.json() == {"name": "John", "age": 30}

    def test_json_method_with_invalid_json(self):
        response = Response("http:\\example.com", 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"name": "John", "age": }')
        with pytest.raises(ValueError):
            response.json()

    def test_text_method(self):
        response = Response("http:\\example.com", 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\nHello, World!')
        assert response.text() == "Hello, World!"

    def test_status_code_property(self):
        response = Response("http:\\example.com", 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\nHello, World!')
        assert response.status_code == 200

    def test_reason_property(self):
        response = Response("http:\\example.com", 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\nHello, World!')
        assert response.reason == "OK"

    def test_raise_for_status_with_informational_error(self):
        response = Response("http:\\example.com", 'HTTP/1.1 100 Continue\n\n')
        with pytest.raises(exceptions.InformationalError):
            response.raise_for_status()

    def test_raise_for_status_with_client_error(self):
        response = Response("http:\\example.com", 'HTTP/1.1 404 Not Found\n\nPage not found')
        with pytest.raises(exceptions.ClientError):
            response.raise_for_status()

    def test_raise_for_status_with_server_error(self):
        response = Response("http:\\example.com", 'HTTP/1.1 503 Service Unavailable\n\nService is temporarily unavailable')
        with pytest.raises(exceptions.ServerError):
            response.raise_for_status()
