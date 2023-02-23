# Expense Tracker
The bot allows to track personal expenses via Telegram

### How to install
Using GitHub CLI:
```bash
gh repo clone Ph0enixGh0st/expense_tracker
```
Or download and unpack ZIP file from GIT Hub repository: https://github.com/Ph0enixGh0st/expense_tracker.git

# Prerequisites
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

# Before use please fill in the following env variables:

`TELEGRAM_API_TOKEN` — Telegram API token taken from BotFather
`TELEGRAM_PROXY_URL` - Proxy URL
`TELEGRAM_PROXY_LOGIN` - Proxy Login
`TELEGRAM_PROXY_PASSWORD` - Proxy Password
`TELEGRAM_ACCESS_ID` — Telegram ID


# To use with Docker please use the command below:
Please fill in env variables first.
```
docker build -t expense_tracker ./
docker run -d --name tracker -v /{YOUR_PATH_HERE}/db:/home/db expense_tracker
```

In order to connect to running container:
```
docker exec -ti tracker bash
```

