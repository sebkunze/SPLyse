import logging

def info(msg, args = []):
    log.info(msg, args)

log = logging.getLogger('SPLyse')
log.setLevel(logging.DEBUG)

fLog = logging.FileHandler('SPLyse.log')
fLog.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fLog.setFormatter(formatter)

log.addHandler(fLog)