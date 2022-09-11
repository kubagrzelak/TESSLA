FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

# copy docker-entrypoint and requirements to initialize multi-stage build
COPY ./docker/entrypoint.sh ./docker/requirements.txt /tessla/docker/

# implement multi-stage build to leverage build cache (does not re-install packages when code changes)
RUN pip install -r /tessla/docker/requirements.txt

# copy assets folder
COPY ./assets /tessla/assets

# copy trained models
COPY ./models /tessla/models

# copy source code
COPY ./src /tessla/src

# enable entrypoint script executable
RUN chmod +x /tessla/docker/entrypoint.sh
ENTRYPOINT [ "/tessla/docker/entrypoint.sh" ]