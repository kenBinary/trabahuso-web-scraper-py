# setup

- download geckodriver for firefox and put in `/driver`

- create 3 .env files : `.env`, `.env.development`, `.env.production`

**.env**

```
BROWSER_PROFILE = <path to browser profile>
BROWSER_DRIVER = <path to browser driver>
```

**.env.development** || **.env.production**

```
DATABASE_URL = <path to db file or turso db url>
TURSO_AUTH_TOKEN = <empty or turso auth token>
```

# Running the scraper

`py main.py dev`

- this will run with the local db file in `/db`

`py main.py prod`

- this will run with your turso database
