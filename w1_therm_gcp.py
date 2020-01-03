#!/usr/bin/python3
import sys, getopt
import logging
from w1_therm_gcp.w1 import W1ThermGCP

log_levels = {
    'CRITICAL' : logging.CRITICAL,
    'FATAL' : logging.FATAL,
    'ERROR' : logging.ERROR, 
    'WARNING' : logging.WARNING,
    'WARN' : logging.WARN,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG,
    'NOTSET' : logging.NOTSET
}

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'c:l:',)
    except getopt.GetoptError:
        print("Usage:", sys.argv[0], "-c <configuration_file> -l <log_level>")
        sys.exit(2)
    configuration_file = None
    for opt, arg in opts:
        if opt == "-c":
            configuration_file = arg
        if opt == "-l":
            logging.basicConfig(level=log_levels[arg])
    W1ThermGCP(configuration_file).run()

if __name__ == "__main__":
    main()
