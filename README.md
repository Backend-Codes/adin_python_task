# Campaign Summary API

## Project Description

This project provides an API that summarizes campaign data from an SQL database according to specified date ranges. The API is developed using the FastAPI framework and SQLAlchemy for database operations.

## Getting Started

### Requirements

- Python 3.9+
- Docker (optional, if you want to run using Docker)
- MySQL database (or another SQL database, but MySQL is used in this project)

### Installation

1. Clone the project:

    ```bash
    git clone https://github.com/your-repo/campaign-summary-api.git
    cd campaign-summary-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Using Docker

If you want to use Docker, you can easily run your project with Docker:

1. Build the Docker image:

    ```bash
    docker build -t campaign-summary-api .
    ```

2. Start the Docker container:

    ```bash
    docker run -d -p 8000:8000 --name campaign-summary-api campaign-summary-api
    ```

### Environment Variables

You need to define the database connection details in the `.env` file:

    ```env
    DATABASE_HOSTNAME=your_host_name
    DATABASE_PORT=your_db_port
    DATABASE_NAME=your_db_name
    DATABASE_USERNAME=your_username
    DATABASE_PASSWORD=your_password
    ```

### Usage

To run the API, use the following command:

    ```bash
    uvicorn app.main:app --reload
    ```

### Endpoints

* `GET /campaigns/summary`: Returns campaign summary data for a specified date range and campaign ID.

### Parameters

* `campaign_id` (optional): The campaign ID. If not provided, summaries for all campaigns will be returned.
* `start_date` (required): The start date. Format: YYYY-MM-DD
* `end_date` (required): The end date. Format: YYYY-MM-DD

### Example Requests

    ```bash
    curl -X 'GET' \
      'http://127.0.0.1:8000/campaigns/summary?start_date=2023-04-20&end_date=2023-04-30' \
      -H 'accept: application/json'
    ```

### Tests

To run the tests that come with the project:

1. Install pytest:

    ```bash
    pip install pytest
    ```

2. Run the tests:

    ```bash
    pytest
    ```

The tests are located in the tests directory and validate the API with sample requests.

### Contributing

If you would like to contribute, please create a pull request. Any contributions and feedback are welcome!