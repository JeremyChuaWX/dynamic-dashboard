# dynamic dashboard

## Dependencies

- Docker

## Setup

- Run the command to setup the project directory

  ```bash
  make setup
  ```

- Place the CSV files in the `./artifacts` directory

- Copy and rename `.env.example` to `.env`

- Edit any values in `.env` as required

- Run the command to migrate the database

  ```bash
  make migrate
  ```

- Run the command to seed the database

  ```bash
  make seed
  ```

## Usage

- Run the command to start the web application

  ```bash
  make start
  ```
