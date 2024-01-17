FROM python:3.11 as builder

WORKDIR /builder

COPY . . 

RUN pip install -r requirements.txt
RUN pip install wheel setuptools && python setup.py bdist_wheel

# Second stage: Build actual container
FROM python:3.11-slim

WORKDIR /app

# Copy only the built wheel file 
COPY --from=builder /builder/dist/*.whl .

RUN pip install pipx
# Install it using pip
RUN pipx install turbocase-2.0.0-py3-none-any.whl 

# Typical Django entrypoint
ENTRYPOINT [ "/root/.local/bin/turbocase" ]
