
### Endpoints
#### User Authentication
- **Register:** `POST account/register/` - Register a new user.
- **Login:** `POST account/login/` - Authenticate user and retrieve JWT tokens.
- **Logout:** `POST account/logout/` - Revoke tokens and log out.

### User Profile
- **Retrieve Profile:** `GET account/profile/` - Fetch the user's profile.
- **Update Profile:** `PUT account/profile/` - Update the user's profile.

### JWT Token Management
- **Token Refresh:** `POST account/token/refresh/` - Refresh the JWT access token.
- **Token Verify:**`POST account/token/verify/` - Verify the validity of a JWT access token.

### Documentation
- **Swagger UI:** `GET /swagger/` - Access API documentation.

