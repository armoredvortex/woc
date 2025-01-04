# Installtion Guide
### Prereqs
Ensure the following are installed:
- Python
- PostgreSQL
- Git

### Step 1: Clone the Repo
`git clone https://github.com/armoredvortex/woc`
### Step 2: Setup Virtual Environment
`python -m venv venv/`
### Step 3: Install Dependencies
`pip install -r requirements.txt`
### Step 4: Set Up PostgreSQL Database
`CREATE DATABSE encrypted_ballot;`
### Step 5: Configure env Variables
```
DATABASE_URL=
SECRET_KEY=
```
### Step 6: Run the application
`flask run`
