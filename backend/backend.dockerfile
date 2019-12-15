FROM bashhack/uvicorn-gunicorn-fastapi

# Install Python dependencies
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system --dev

# Expose for Jupyter
EXPOSE 8888

COPY ./app /app
WORKDIR /app/

EXPOSE 80