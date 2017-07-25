FROM ubuntu
MAINTAINER dsa dsa@dsa.tech
RUN apt-get -y update
RUN apt-get -y install python-setuptools python-dev build-essential
COPY get-pip.py /
RUN python get-pip.py
RUN pip install numpy
COPY input_agents.py /
COPY design_agents.py /
COPY eval_agents.py /
COPY tests.py /
COPY utils.py /
CMD python tests.py
