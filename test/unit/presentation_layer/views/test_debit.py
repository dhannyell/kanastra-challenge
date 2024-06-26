import pytest
from unittest import mock
from werkzeug.datastructures import FileStorage

from application_layer.use_cases.debit import DebitUseCase

@pytest.fixture()
def upload_file():
    return FileStorage(filename='input.csv')

@mock.patch.object(DebitUseCase, 'save_debits')
def test_put_upload_file_success(
    save_debits_mock, 
    upload_file, 
    app
):
    save_debits_mock.return_value = 1

    response = app.put(
        "/api/upload-file", 
        data={"file":upload_file},
        headers={
            "Content-Type": "multipart/form-data"
        }
    )
    
    assert response.status == '201 CREATED'
    assert response.json == {"message": "File Uploaded Successfully"}
    save_debits_mock.assert_called_once()

@mock.patch.object(DebitUseCase, 'save_debits')
def test_put_upload_file_success_with_no_insert(
    save_debits_mock, 
    upload_file, 
    app
):
    save_debits_mock.return_value = None

    response = app.put(
        "/api/upload-file", 
        data={"file":upload_file},
        headers={
            "Content-Type": "multipart/form-data"
        }
    )
    
    assert response.status == '200 OK'
    assert response.json == {"message": "File Uploaded Successfully"}
    save_debits_mock.assert_called_once()

@mock.patch.object(DebitUseCase, 'save_debits')
def test_put_upload_file_error_invalid_file(
    save_debits_mock, 
    upload_file, 
    app
):
    save_debits_mock.return_value = None

    upload_file.filename = "input.json"

    response = app.put(
        "/api/upload-file", 
        data={"file":upload_file},
        headers={
            "Content-Type": "multipart/form-data"
        }
    )
    
    assert response.status == '400 BAD REQUEST'
    assert response.json == {"message":"Invalid File"}
    assert save_debits_mock.call_count == 0


def test_put_upload_file_error_invalid_header( 
    upload_file, 
    app
):
    response = app.put(
        "/api/upload-file", 
        data={"file":upload_file},
        headers={
            "Content-Type": "application/json"
        }
    )
    
    assert response.status == '400 BAD REQUEST'
    assert response.json == {"message":"Invalid Content-Type. Include multipart/form-data in Content-Type Header"}

@mock.patch.object(DebitUseCase, 'save_debits')
def test_put_upload_file_error_generic_exception(
    save_debits_mock, 
    upload_file, 
    app
):
    save_debits_mock.side_effect = Exception("Generic Error")

    response = app.put(
        "/api/upload-file", 
        data={"file":upload_file},
        headers={
            "Content-Type": "multipart/form-data"
        }
    )
    
    assert response.status == '500 INTERNAL SERVER ERROR'
    assert response.json == {"message":"Failed to Proccess CSV File"}