FROM arm32v6/python:3-alpine
WORKDIR /usr/src/app

# Install build tools
RUN apk --no-cache --update add jq

# Install flask (for the web server)
RUN pip install Flask

# Copy over the code
COPY ./discovery.py .

# Run the daemon
CMD python discovery.py

