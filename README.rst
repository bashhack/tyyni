=====
Tyyni
=====

----------------------------------
*Tyyni (adj. calm, serene, stoic)*
----------------------------------


Dev Workflow
============

A TDD workflow is encouraged and to faciliate this methodology, this project uses `pytest` with the following plugins:

- ``pytest-watch``
- ``pytest-testmon``
- ``pytest-cov``
- ``pytest-sugar``

If using Honcho to orchestrate processes, simply run:

.. code:: bash

    honcho start -f Procfile.dev

or execute the following from the command-line:

.. code:: bash

    ptw --runner "pytest --testmon"

These commands can be run with the following command:

.. code:: bash

    docker-compose exec backend-tests /tests-start.sh

Services
========

- Traefik (reverse-proxy/load-balancer)
- PostgreSQL (data store)


TASKS
=====

Creating migrations is handled via Alembic. To create a new migration, we leverage
our mounted Docker volume (see: `docker-compose.dev.volumes.yml`) so that imports are resolved
as expected:

.. code:: bash

    docker-compose exec backend bash

Once in the shell, run:

.. code:: bash

    alembic --autogenerate -m "Name of revision"



NOTE:
If running `pipenv install --dev` presents any issue with the `ujson` dev dependency from FastAPI (ex. missing Python source headers), the resolution is likely installing the `python3-dev` package on the local host (NOT remote Docker host).

.. code:: bash

    apt-get install python3-dev


Access PostgreSQL during initial development:

.. code:: bash

    exec psql -d POSTGRES_DB -U POSTGRES_USER

Dev TODOS:

- `Migrate to v2 <https://docs.traefik.io/migration/v1-to-v2/>`_

Resources:

`Traefik v1.7 Docker Configuration <https://docs.traefik.io/v1.7/configuration/backends/docker/>`_

`pgadmin4 <https://www.pgadmin.org/>`_

`Why use volumes for better development? See: dev.volumes.yml <https://nickjanetakis.com/blog/docker-tip-12-a-much-better-development-experience-with-volumes>`_


