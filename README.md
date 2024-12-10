## Installation

1. Clone the repository:
   ```bash
   # Using HTTPS:
   git clone https://github.com/your-username/your-repository.git
   # Using SSH:
   git clone git@github.com:your-username/your-repository.git
   ```

2. Add the `.env` file by requesting it from me.

3. [Install Poetry](https://python-poetry.org/docs/):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

4. Install the required dependencies:
   ```bash
   poetry install
   ```

5. Activate the virtual environment created by Poetry:
   ```bash
   poetry shell
   ```

## Run Instructions

1. To run the FastAPI app:
   ```bash
   python backend/app.py
   ```

2. To run the Flask app:
   ```bash
   flask --app frontend.app run
   ```

## Database Setup

1. Ensure that your MySQL database is running on `127.0.0.1:<port_number>`.
   Replace <port_number> with your MySQL server's port number. The default is 3306.

2. Create the `User` and `Task` tables using the SQL statements provided in the [Database Metadata](db_metadata.md) file.
