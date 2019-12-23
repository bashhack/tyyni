FROM bashhack/uvicorn-gunicorn-fastapi

# Install Python dependencies
COPY app/Pipfile Pipfile
COPY app/Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system --dev

# Expose for Jupyter
# Using inside the container:
#
#   $ docker-compose exec backend bash
#   $ $JUPYTER

ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyterlab==1.2.4 ; fi"
EXPOSE 8888

COPY ./app /app

ENV PYTHONPATH=/app

COPY ./app/tests-start.sh /tests-start.sh

RUN chmod +x /tests-start.sh

# This will make the container wait, doing nothing, but alive
CMD ["bash", "-c", "while true; do sleep 1; done"]

# Afterwards you can exec a command /tests-start.sh in the live container, like:
# docker exec -it backend-tests /tests-start.sh
