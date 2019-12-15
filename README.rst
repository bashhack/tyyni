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

Services
========

- Traefik (reverse-proxy/load-balancer)
- PostgreSQL (data store)



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
