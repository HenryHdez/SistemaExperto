FROM ubuntu:18.04 as build

WORKDIR /opt/app

# apt-get Utilidades del sistema
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++-5\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app
# INSTALAR PIP
RUN apt update && apt install -y python3-pip

# INTALACION DE R
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        software-properties-common \
                ed \
        less \
        locales \
        vim-tiny \
        wget \
        ca-certificates \
        && add-apt-repository --enable-source --yes "ppa:marutter/rrutter3.5" \
    && add-apt-repository --enable-source --yes "ppa:marutter/c2d4u3.5" 

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen en_US.utf8 \
    && /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
        && apt-get install -y --no-install-recommends --fix-missing\
                 littler \
         r-base \
         r-base-dev \
         r-recommended \
    && ln -s /usr/lib/R/site-library/littler/examples/install.r /usr/local/bin/install.r \
    && ln -s /usr/lib/R/site-library/littler/examples/install2.r /usr/local/bin/install2.r \
    && ln -s /usr/lib/R/site-library/littler/examples/installGithub.r /usr/local/bin/installGithub.r \
    && ln -s /usr/lib/R/site-library/littler/examples/testInstalled.r /usr/local/bin/testInstalled.r \
    && install.r docopt \
    && rm -rf /tmp/downloaded_packages/ /tmp/*.rds \
    && rm -rf /var/lib/apt/lists/*

# INTALACION DE LATEX
RUN apt-get update -y
RUN apt-get install -y latexmk
RUN apt-get install texlive-latex-base
RUN apt-get install -y texlive-fonts-recommended
RUN apt-get install -y texlive-latex-extra
RUN apt-get install texlive-lang-spanish
RUN apt-get install -y unixodbc-dev

#INSTALACION DE FREETDS
RUN apt-get install -y unixodbc-dev freetds-dev freetds-bin tdsodbc

#INSTALACIÓN DE PAQUETES
COPY requirements.txt /opt/app/requirements.txt
RUN pip3 install -r requirements.txt

#Correr python
COPY odbcinst.ini /etc/odbcinst.ini
COPY __pycache__ /opt/app/__pycache__
#COPY instance /opt/app/instance 
#COPY otros /opt/app/otros 
COPY static /opt/app/static 
COPY templates /opt/app/templates 
COPY COL_adm1.sf.rds /opt/app/COL_adm1.sf.rds 
COPY Areas.py /opt/app/Areas.py
COPY Costos_funcionamiento.py /opt/app/Costos_funcionamiento.py 
COPY Diseno_inicial.py /opt/app/Diseno_inicial.py 
COPY Doc_latex.py /opt/app/Doc_latex.py 
COPY Gases.py /opt/app/Gases.py 
COPY index.py /opt/app/index.py 
COPY Modulo1.py /opt/app/Modulo1.py 
COPY Modulo2.py /opt/app/Modulo2.py 
COPY Modulo4.py /opt/app/Modulo4.py 
COPY Modulo21.py /opt/app/Modulo21.py 
COPY Pailas.py /opt/app/Pailas.py 
COPY index.py /opt/app/index.py
EXPOSE 7000
CMD ["python3", "index.py"]