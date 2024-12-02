## Project Overview - Attendance System  (Hajiri)
The Financial System is a web-based  API  create in Djnago — a high-level Python Web framework that encourages rapid development and clean, pragmatic design.


## Tech Stack 
Backend: Django
API: Django REST Framework
API Documenation : Swagger API 
Database: Sqlite (for localhost development)

## Features in API.
1.**Income Management**:
- Add Income
- Edit Income 
- Get Income
- Delete Income
Get Income with all filter such as status-Received date,source and so on and sorting and other features 
2. **Expenses Management** - 
- Add Expenses
- Edit Expenses 
- Get Expenses
- Delete Expenses
Get Expenses with all filter such as status-paid, Due date,types and so on and sorting and other features are involve
3. **Loan Managment**: 
- Add Loan
- Edit Loan 
- Get Loan
- Delete Loan
Get Loan with all filter such as status-paid,Loan name and so on and sorting
ie.listing according to the (Amount,Balance to be paid,less than balance ,more than Remaning balance) and other features are involve
List the monthly EMI of that loan and More Features is implemented.
4. **Summart Reports** : 
-Get the list of loan ,total Income ,total Expenses 
Filtering the data according to the specific date range and list it with all available data of that user.
4. **Trend Reports** : 
- Generate Trends reports by selecting the specific date range .
    with that date what is income expenses and loan  
- A chartjs to visualize attendance trends.
- Chartjs help that trend report in a graph as per user requiremnts

## Setup and Installation

### Prerequisites
Ensure you have the following installed on your local machine:
- Python


### This Detailed provides setup instructions for local development.

### Step-by-Step Setup
1. **Clone the Repository:**
git clone https://github.com/bipuld/Financial-System-API.git
cd Financial-System-API
2.  **Create and Activate a Virtual Environment**:
python -m venv en
3.  **Install Required Package**:
pip install -r requirements.txt
4. **Database**:
python manage.py migrate
5. **Create a Superuser**:
python manage.py createsuperuser
create the super user and used that email and password to login in admin /admin
and see all that data 

# Create the User by Registering from API call swagger/ the user and so on detailed are mentioned

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

### Finance (Incomes,Expenses,Report)

-   **Income:**
- **Create Income:**  `POST api/finance/income/ ` - Create Income for login User.
- **list Income:**  `GET  api/api/finance/income/` - Retrive list 
of Income
Some of sorting and filtering example are  
api/finance/income/?status=Pending
api/finance/income/?status=Received&date_received=2024-11-30
api/finance/income/?status=Received&date_received=2024-11-30&source_name=Salary
api/finance/income/?page=1
api/finance/income/?sort=amount(filtering in asc order)
api/finance/income/?sort=-amount(filtering in the desc order)

- **Update Income:**  ` PUT /api/finance/income ` Update Income  for specific Income
- **Delete Income:**  ` DELETE api/finance/income/ ` Delete Income for specific Income


-   **Expenses**
- **Create  Income:**  ` POST /api/finance/expense/ ` Create Expenses 
- **Retrive Income:**  ` GET /api/finance/expense/ ` Retrive Expenses
Some of sorting and filtering example are  
api/finance/expense/?page=2
api/finance/expense/?status=Paid&due_date=2024-11-3
api/finance/expense/?status=Paid&due_date=2024-11-30&category=Water
api/finance/expense/?sort=-amount (desc)
api/finance/expense/?sort=amount (asc)
api/finance/expense/?page=2&sort=due_date
/api/finance/expense/?page=2&status=Paid
- **Update Income:**  ` PUT /api/finance/expense/ ` Update Expenses
- **Delete Income:**  ` DELETE /api/finance/expense/ `Delete Expenses


- **Loan**

- **Create  Loan:**  ` POST /api/finance/loan/ ` Create Loan 
- **Retrive Income:**  ` GET /api/finance/loan/ ` Retrive Loan
Some of sorting and filtering example are  
api/finance/loan/?page=1
api/finance/loan/?page=2&status=Active
api/finance/loan/?status=Paid&laon_name=Car%20Loan
api/finance/loan/?rem_amnt_gte=26000.00&rem_amnt_lte=5000000.00
- **Update Income:**  ` PUT /api/finance/loan/ ` Update Loan
- **Delete Income:**  ` DELETE /api/finance/loan/ `Delete Loan


- **Summary Report**
- **List Summary Report:**  `GET   /api/summary/report/ `  Give all the Report detiled with loan 
Some filter 
api/summary/report/?start_date=2024-11-29&end_date=2024-12-02


- **Trends Income vs expenses**
- **List Trends Income vs expenses:**  `GET   api/summary/income-expenses-trends/ `  Give all the Expenses and income detailes
For Json Repsonse - Pass/Select application/json in headers as Accept 
For Html/CSS/JS Repsonse - Pass/Select text/html in headers as Accept 
