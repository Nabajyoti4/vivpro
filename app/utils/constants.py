# Response Name
SUCCESS = "success"
ERROR_404 = "error_404"
AUTHORIZATION_ERROR = "authorization_error"
INTERNAL_SERVER_ERROR = "internal_server_error"
VALIDATION_ERROR = "validation_error"
CREATE_SUCCESS = "create_success"

response_mapper = {
    SUCCESS: {"status_code": 200, "message": "Success"},
    CREATE_SUCCESS: {"status_code": 201, "message": "Created"},
    ERROR_404: {"status_code": 404, "message": "Not Found"},
    AUTHORIZATION_ERROR: {"status_code": 401, "message": "UnAuthorized"},
    INTERNAL_SERVER_ERROR: {"status_code": 500, "message": "Internal Server Error"},
    VALIDATION_ERROR: {"status_code": 422, "message": "Validation Error"},
}

candidate_question_scale = 7
