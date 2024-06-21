messages = {
    "common": {
        "api_success": {"msg": "Data fetched successfully", "status_code": 2000},
        "api_failed": {"msg": "Unexpected error! Please contact the administrator", "status_code": 5000},
        "invalid_request": {"msg": "Invalid Request", "status_code": 4001},
        "no_data_available": {"msg": "Data not available", "status_code": 2040},
        "form_saved": {"msg": "Form saved successfully", "status_code": 2000},
        "update_fail": {"msg": "Update failed", "status_code": 5000},
        "pincode_missing": {"msg": "Pincode required", "status_code": 4000},
        "dont_have_update_permission": {"msg": "You do not have the permission to update this entity",
                                        "status_code": 4003},
    },
    "login": {
        "invalid_credentials": {"msg": "You have entered invalid credentials. Please try again", "status_code": 4001},
        "invalid_token": {"msg": "Invalid Token", "status_code": 4001},
        "login_success": {"msg": "Login successful", "status_code": 2000},
        "provide_username_and_password": {"msg": "Please enter a valid username and password", "status_code": 2040},
        "logout_success": {"msg": "Logout Successful", "status_code": 2000},
    },
    "registration": {
        "register_success": {"msg": "User created successfully", "status_code": 2001},
        "register_email_link_success": {"msg": "Email verified successfully", "status_code": 2000},
        "register_email_link_expire": {"msg": "The link has expired", "status_code": 4000},
        "register_token_not_found": {"msg": "The link has expired", "status_code": 4004},
        "registration_no_exist": {"msg": "Registration number already exists", "status_code": 4009},
        "email_exist": {"msg": "Email Id already exists", "status_code": 4009},
        "username_exist": {"msg": "Username already exists", "status_code": 4009},
    },
    "user": {
        "username_missing": {"msg": "Username is missing", "status_code": 6001},
        "username_not_available": {"msg": "Username already exists", "status_code": 4000},
        "username_available": {"msg": "Username is available", "status_code": 2000},
        "email_verify_link_sent": {"msg": "Email verification link sent", "status_code": 2000},
        "user_info_saved": {"msg": "Information saved successfully", "status_code": 2000},
        "user_not_found": {"msg": "User not found", "status_code": 4004},
        "invalid_reset_link": {"msg": "Invalid reset link", "status_code": 4000},
        "wrong_old_password": {"msg": "Wrong Old Password", "status_code": 4000},
        "password_changed_success": {"msg": "Password changed successfully", "status_code": 2004},
        "password_reset_email_success": {
            "msg": "We have sent instructions for resetting your password to your registered email",
            "status_code": 2000},
        "password_reset_success": {"msg": "Your password reset is successful!", "status_code": 2000},
    },
    "profile": {
        "create_success": {"msg": "Profile created successfully", "status_code": 2001},
        "update_success": {"msg": "Profile is updated", "status_code": 2000},
        "profile_not_available": {"msg": "Profile is not available", "status_code": 4000},
    }
}
