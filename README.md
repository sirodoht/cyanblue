# cyanblue

Sci-Hub London website.

## Contributing

Feel free to send an email patch to
[~sirodoht/public-inbox@lists.sr.ht](mailto:~sirodoht/public-inbox@lists.sr.ht).

On how to contribute using email patches see
[git-send-email.io](https://git-send-email.io/).

## Development

This is a [Django](https://www.djangoproject.com/) codebase. Check out the
[Django docs](https://docs.djangoproject.com/) for general technical
documentation.

### Structure

The Django project is `cyanblue`. There is one Django app, `main`, with all
business logic. Application CLI commands are generally divided into two
categories, those under `python manage.py` and those under `make`.

### Dependencies

A file named `.envrc` is used to define the environment variables required for
this project to function. One can either export it directly or use
[direnv](https://github.com/direnv/direnv). There is an example environment
file one can copy as base:

```sh
cp .envrc.example .envrc
```

`.envrc` should contain the following variables:

```sh
export SECRET_KEY=some-secret-key
export EMAIL_HOST_USER=smtp-user
export EMAIL_HOST_PASSWORD=smtp-password
```

When on production, also include the following:

```sh
export NODEBUG=1
```

### Database

This project uses SQLite. To create the database and schema and apply
migrations, run:

```sh
python manage.py migrate
```

### Serve

To run the Django development server:

```sh
python manage.py runserver
```

## Testing

Using the Django test runner:

```sh
python manage.py test
```

For coverage, run:

```sh
make cov
```

## Code linting & formatting

The following tools are used for code linting and formatting:

* [black](https://github.com/psf/black) for code formatting.
* [isort](https://github.com/pycqa/isort) for imports order consistency.
* [flake8](https://gitlab.com/pycqa/flake8) for code linting.

To use:

```sh
make format
make lint
```

## Deployment

Deployment [is configured](uwsgi.ini) using
[uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) in
[emperor mode](https://uwsgi.readthedocs.io/en/latest/Emperor.html).

In this case, environment variables are set in the `uwsgi.ini` file.

Also, [we use](scihublondon.org) nginx to proxy all requests to uWSGI.

## License

This software is licensed under the MIT license. For more information, read the
[LICENSE](LICENSE) file.
