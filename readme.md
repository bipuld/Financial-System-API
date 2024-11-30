
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



http://localhost:8000/api/finance/income/?status=Pending
http://localhost:8000/api/finance/income/?status=Received&date_received=2024-11-30
http://localhost:8000/api/finance/income/?status=Received&date_received=2024-11-30&source_name=Salary
http://localhost:8000/api/finance/income/?page=1
http://localhost:8000/api/finance/income/?sort=amount




Expenses

http://localhost:8000/api/finance/expense/?page=2
http://localhost:8000/api/finance/expense/?status=Paid&due_date=2024-11-3
http://localhost:8000/api/finance/expense/?status=Paid&due_date=2024-11-30&category=Water
http://localhost:8000/api/finance/expense/?sort=amount
http://localhost:8000/api/finance/expense/?page=2&sort=due_date