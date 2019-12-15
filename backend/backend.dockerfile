FROM bashhack/uvicorn-gunicorn-fastapi

# Install Python dependencies
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system --dev

# Expose for Jupyter
# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyterlab ; fi"
EXPOSE 8888

COPY ./app /app
WORKDIR /app/

EXPOSE 80