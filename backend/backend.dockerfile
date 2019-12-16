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
WORKDIR /app/

EXPOSE 80