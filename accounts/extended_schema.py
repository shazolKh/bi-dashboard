verify_pass_schema = {
    200: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "OTP matched."},
    },
    400: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "Invalid Request format."},
    },
    404: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "OTP didn't match/OTP doesn't exist for this number."},
    },
}

pass_reset_schema = {
    200: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "Password reset successful."},
    },
    400: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "Invalid Request format."},
    },

    404: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "User doesn't exist."},
    },
}

init_pass_schema = {
    200: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "Password reset code updated."},
    },
    201: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "Password reset code created."},
    },
    400: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "Invalid Request format."},
    },
    500: {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "example": {"message": "OTP service error."},
    },
}
