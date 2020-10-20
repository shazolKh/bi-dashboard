# **drf_db_backend**

## Agenda

- :heavy_check_mark: Create CustomUser model by overriding default User model

  - Replace username with email as default identification field
  - Replace first_name, last_name with `name` aka full name
  - Make `name` required

- :heavy_check_mark: Extend CustomUser into Profile (only for User, not admin/stuffs)

  - Add fields from the ERD to profile
  - Add Signal receivers to auto-create/edit profile row on User creation/edit
  - Add license related fields with profile

- :heavy_check_mark: Divide admin into Superuser and Staff

  - Only let superuser be created by command line, no option for staffs/superusers to create from admin site
  - Create Staff group on migrate complete on post_migrate signal
  - Let stuffs only CRUD users aka Profiles but not themselves.

- :heavy_check_mark: Integrate API based CRUD for CustomUser and Profile
  - Let User view, update and delete account
  - Let User only view and update Profile because profile can only be deleted with account
- :heavy_check_mark: Integrate JWT
  - JWT token and isAuthenticated for every logged in requests.
- :white_check_mark: Add PowerBI app containing report model, MSAL logic, report handling.
- :white_check_mark: Add security Pre-cautions
