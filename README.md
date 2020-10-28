# **drf_db_backend**

## To run locally

Follow the below commands. (For Linux/MacOS). For windows they may slightly differ.

```bash
# requires github-cli, otherwise use git clone
gh repo clone Magpie-Analytics/drf_db_backend
cd drf_db_backend
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
python manage.py makemigrations accounts powerbi
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Agenda

- :heavy_check_mark: Create CustomUser model by overriding default User model

  - Replace username with email as default identification field
  - Replace first_name, last_name with `name` aka full name
  - Make `name` required

- :heavy_check_mark: Extend CustomUser into Profile (only for User, not admin/stuffs)

  - Add fields from the ERD to profile
  - Add Signal receivers to auto-create/edit profile row on User creation/edit

- :heavy_check_mark: Divide admin into Superuser and Staff

  - Only let superuser be created by command line, no option for staffs/superusers to create from admin site
  - Create Staff group on migrate complete on post_migrate signal
  - Let stuffs only CRUD users aka Profiles but not themselves.

- :heavy_check_mark: Integrate API based CRUD for CustomUser and Profile

  - Let User view, update and delete account
  - Let User only view and update Profile because profile can only be deleted with account

- :heavy_check_mark: Integrate JWT

  - JWT token and isAuthenticated for every logged in requests.

- :heavy_check_mark: Finalize Licenses

  - Separate table for licenses and user-licenses
  - Add license related fields
  - Dynamic License creation

- :heavy_check_mark: Add Monitoring Table for all Users

- :heavy_check_mark: Add Email verification, Password reset and Change

- :heavy_check_mark: Add PowerBI app containing report model, MSAL logic, report handling.

- :white_check_mark: Add security Pre-cautions

  - Confirm sending token on login
  - Send new access token from old refresh token in cookie
  - Check refresh token expiry and renewal
  - Lock internal APIs(those that don't need client access) completely
  - Check storing password in hash
  - Recheck password reset/change flow
  - Hide backend APIs completely without trusted client
  - Check MSAL Token expiry and renewal cycle

- :white_check_mark: Setup server and Database
  - Finalize Email templates
  - Add static pages(Email confirm/Password Reset/Password change confirm)
  - PostgreSQL Database setup and backup
