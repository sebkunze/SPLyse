import logging

filename = 'SPLyse.log'

def info(msg, args = []):
    log.info(msg, args)

def debug(msg, args = []):
    log.debug(msg, args)

log = logging.getLogger('SPLyse')
log.setLevel(logging.DEBUG)

fLog = logging.FileHandler(filename)
fLog.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fLog.setFormatter(formatter)

log.addHandler(fLog)