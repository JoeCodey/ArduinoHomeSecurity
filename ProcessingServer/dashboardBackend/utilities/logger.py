import logging 


# Define new log level called "LOGIC"
# -- For displaying noteable behaviour during execution 

LOGIC_LEVEL_NUM = 15
MAJORCHECKPOINT_LEVEL_NUM = 25
logging.addLevelName(LOGIC_LEVEL_NUM, "LOGIC")
logging.addLevelName(MAJORCHECKPOINT_LEVEL_NUM, "MAJORCHECKPOINT")

def logic(self, message, *args, **kws):
    if self.isEnabledFor(LOGIC_LEVEL_NUM):
        self._log(LOGIC_LEVEL_NUM, message, args, **kws) 
def MAJORCHECKPOINT(self, message, *args, **kws):
    if self.isEnabledFor(MAJORCHECKPOINT_LEVEL_NUM):
        self._log(MAJORCHECKPOINT_LEVEL_NUM, message, args, **kws)

logging.Logger.majorcheckpoint = MAJORCHECKPOINT
logging.Logger.logic = logic

# USE ANSI codes to colourize outputs 

FMT = "[{levelname:^9}] {asctime} {msecs:03.0f} [{filename}s:{lineno}] {message}"
FORMATS = {
    logging.DEBUG: f"\33[32m{FMT}\33[0m", 
    logging.INFO: f"\33[34m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\33[1m{FMT}\33[0m",
    MAJORCHECKPOINT_LEVEL_NUM: f"\033[1;35m{FMT}\33[0m", 
    LOGIC_LEVEL_NUM: f"\33[38;2;255;116;23m{FMT}\33[0m"
}

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{",datefmt='%H:%S')
        return formatter.format(record)

handler = logging.StreamHandler() 
handler.setFormatter(CustomFormatter())

logging.basicConfig(
    level = logging.DEBUG, 
    handlers=[handler]
)

log = logging.getLogger("coloured-logger")

def get_logger_obj(): 
    handler = logging.StreamHandler() 
    handler.setFormatter(CustomFormatter()) 
    logging.basicConfig(
        level = logging.DEBUG,
        handlers=[handler]
    )

    #return functioning logger object 
    return log 
