FROM kalilinux/kali-last-release

RUN apt-get update && apt-get install -y theharvester git pip
RUN git clone https://github.com/RachBartmoss/T.O.C.git

WORKDIR T.O.C

RUN git clone https://github.com/rbsec/dnscan.git
RUN pip install -r requirements.txt
RUN chmod +x T.O.C.py

COPY ./ressources/*.txt /T.O.C


ENTRYPOINT ["./T.O.C.py"]