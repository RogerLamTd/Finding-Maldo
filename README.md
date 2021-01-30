# Finding-Maldo
McHacks 2021


Install necessary dependencies:
python3 -m venv venv
. /venv/bin/activate
pip3 install -r requirements.txt

Run it:
export FLASK_APP=hello.py
flask run

to build docker image
docker build -t maldo .

to run in docker:
docker -d -p 80 --rm maldo