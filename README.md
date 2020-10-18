# **drf_db_backend**

## Agenda

- :heavy_check_mark: Create CustomUser model by overriding default User model

  - :arrow_forward: Replace username with email as default identification field
  - :arrow_forward: Replace first_name, last_name with `name` aka full name
  - :arrow_forward: Make `name` required

- :heavy_check_mark: Extend CustomUser into Profile (only for User, not admin/stuffs)

  - :arrow_forward: Add fields from the ERD to profile
  - :arrow_forward: Add Signal receivers to auto-create/edit profile row on User creation/edit
  - :arrow_forward: Add license related fields with profile

- :heavy_check_mark: Divide admin into Superuser and Staff

  - :arrow_forward: Only let superuser be created by command line, no option for staffs/superusers to create from admin site
  - :arrow_forward: Create Staff group on migrate complete on post_migrate signal
  - :arrow_forward: Let stuffs only CRUD users aka Profiles.

- :white_check_mark: Integrate API based CRUD for CustomUser
- :white_check_mark: Integrate JWT
- :white_check_mark: Add PowerBI app containing report model, MSAL logic, report handling.
- :white_check_mark: Add security Pre-cautions
