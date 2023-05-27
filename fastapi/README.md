# FastAPI test

This project follows the [Real Python](https://realpython.com/) course: [URL shortener fast API](https://realpython.com/courses/url-shortener-fastapi/).

I want to use this to learn setting up CRUD API's and use databases with python.

## Run it

This is a poetry package. So first enter the shell.

```
poetry shell
```

Then use uvicorn to run the server.

```
uvicorn shortener_app.main:app --reload
```

You can always see the docs for the endpoints generated at.

```
ADDRESS/docs
```

## Goal

The aim of the project is to set up an API that shortens URLS and counts the use
of those shortened URLS. This API will have the following endpoints.

| Endpoint              | HTTP Verb | Request Body | Action                 |
| --------------------- | --------- | ------------ | ---------------------- |
| `/`                   | `GET`     |              | "Hello World"          |
| `/url`                | `POST`    | Target URL   | Shows Created URL Info |
| `/{url_key}`          | `GET`     |              | Forward to URL         |
| `/admin/{secret_key}` | `GET`     |              | Admin Info for URL     |
| `/admin/{secret_key}` | `DELETE`  | Secrete Key  | Delete URL             |
| `/docs`               | `GET`     |              | Swagger documentation  |