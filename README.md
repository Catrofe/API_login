# Login API

Hello dev's.

This is my first API using validations.
Below I will put how to run the application but before talking about my API and what dependencies usin and why.

### Database

In this API I will be using postgres, as part of the challenge proposed by my teacher.
I believe that the choice of the database was due to the fact that it is robust and well structured. In addition to being a requirement in several Brazilian companies.

### ORM
This API uses SQLAlchemy as the ORM. It was my first real contact with ORM, I went through great difficulties but I saw how robust it is, besides being one of the main orm's on the market, it's one of the few to support async.

### Framework used
The framework used was FastAPI, as it has an easy syntax, good documentation and a shorter learning curve.
I think it's a great choice overall, even though I'm not able to render HTML.

## How to Run the application
To run the application just use the following command in terminal.

```bash
docker-compose up
```

After that, just use the routes already established to register, log in, log out and so on.

### Routes

0.0.0.0:8000/register
0.0.0.0:8000/login
0.0.0.0:8000/logout/{id}
0.0.0.0:8000/logged/{id}

### Testing and development


If you want to create new features, routes and etc, just clone the repository. To run the tests, change the following variable:

![image](https://user-images.githubusercontent.com/82066310/156360456-ed740c00-4948-4c4f-813d-c2816a51749e.png)

Change to:

```bash
engine = build_engine("sqlite:///db.sqlite3")
```

