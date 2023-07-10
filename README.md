# nicegui_planner

This sample will show you to create an a daily planner (Calendar & Email) using NiceGUI.

You can follow along step-by-step in our blog post ["How to build a Daily Planner using NiceGUI"](https://www.nylas.com/blog/how-to-build-a-daily-planner-using-nicegui/).

## Setup

### System dependencies

- Python v3.x

### Gather environment variables

You'll need the following values:

```text
CLIENT_ID = ""
CLIENT_SECRET = ""
ACCESS_TOKEN = ""
```

Add the above values to a new `.env` file:

```bash
$ touch .env # Then add your env variables
```

### Install dependencies

```bash
$ pip3 install nicegui # Nylas API SDK
$ pip3 install python-dotenv # Environment variables
```

## Usage

Run the file **nicegui_planner.py**:

```bash
$ python3 nicegui_planner.py
```

NiceGUI will open up your browser on port 8080.

## Learn more

Visit our [Nylas Python SDK documentation](https://developer.nylas.com/docs/developer-tools/sdk/python-sdk/) to learn more.
