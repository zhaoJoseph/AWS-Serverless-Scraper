FROM public.ecr.aws/ubuntu/ubuntu:latest

RUN apt-get update

RUN apt-get install -y python3

RUN apt install -y python3.11-venv

ENV PYTHONUNBUFFERED=0

ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /pyscraper

COPY requirements.txt .

RUN pip3 install -r requirements.txt 

COPY pyscraper .

RUN playwright install

RUN apt-get install -y libglib2.0-0\                    
        libnss3\                                     
        libnspr4\                                    
        libatk1.0-0\                                 
        libatk-bridge2.0-0\                          
        libcups2\                                    
        libdrm2\                                     
        libdbus-1-3\                                 
        libxcb1\                                     
        libxkbcommon0\                               
        libatspi2.0-0\                               
        libx11-6\                                    
        libxcomposite1\                              
        libxdamage1\                                 
        libxext6\                                    
        libxfixes3\                                  
        libxrandr2\                                  
        libgbm1\                                     
        libpango-1.0-0\                              
        libcairo2\                                   
        libasound2

ENV URL=""

CMD  python webscraper/pyscraper.py ${URL}

