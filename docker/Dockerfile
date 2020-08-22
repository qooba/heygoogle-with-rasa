FROM rasa/rasa:1.10.10
USER root
RUN apt update && apt install git -yq
RUN pip3 install python-jose watchdog[watchmedo]
ENTRYPOINT /bin/bash
