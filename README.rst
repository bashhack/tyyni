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


Interact With Telegram Bot
==========================

.. code:: python

    >>> import telegram
    >>> bot = telegram.Bot(token='TELEGRAM_API_TOKEN')
    >>> print(bot.get_me())
    {'id': 12345, 'first_name': 'bot_name', 'is_bot': True, 'username': 'bot_username'}
