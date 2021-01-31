import os

targetPort = os.getenv('PORT')
if not targetPort:
    targetPort = '80'

bind = "0.0.0.0:" + targetPort
workers = 2
threads = 2
timeout = 120