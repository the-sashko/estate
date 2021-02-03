from os import getcwd, path, remove, mkdir, chmod

import datetime

from tools.telegram import Telegram

class Logger:
    __LOG_DIR_PATH  = '%s/logs/%s'
    __LOG_FILE_PATH = '%s/%s.log'

    __DEFAULT_LOG_TYPE = 'info'

    __LOG_MESSAGE_FORMAT = '[%s] %s\n'

    __telegram = None

    def __init__(self):
        self.__telegram = Telegram()

    def log(self, message: str, logType: str = 'info') -> bool:
        if len(logType) < 1:
            return False

        if len(logType) < 1:
            logType = self.__DEFAULT_LOG_TYPE

        print('[%s] %s\n' % (logType.upper(), message))

        logType = logType.lower()

        logFilePath = self.__getLogFilePath(logType)

        self.__createLogDir(logType)
        self.__createLogFile(logFilePath)
        self.__removeOldLogFile(logType)

        currentTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        message     = self.__LOG_MESSAGE_FORMAT % (currentTime, message)

        logFile = open(logFilePath, 'a')

        logFile.write(message)
        logFile.close()

        return True

    def logError(self, exp: Exception):
        if hasattr(exp, 'message'):
            errorMessage = exp.message
        else:
            errorMessage = str(exp)

        self.log(errorMessage, 'error')

        self.__telegram.sendToBot(errorMessage)

    def __getLogDirPath(self, logType: str) -> str:
        return self.__LOG_DIR_PATH % (getcwd(), logType)

    def __createLogDir(self, logType: str):
        logDirPath = self.__getLogDirPath(logType)

        if not path.exists(logDirPath) or not path.isdir(logDirPath):
            mkdir(logDirPath)
            chmod(logDirPath, 0o755)

    def __getOldLogName(self, logType: str) -> str:
        oldYear = str(int(datetime.datetime.today().strftime('%Y')) - 1)
        month   = datetime.datetime.today().strftime('%m')
        day     = datetime.datetime.today().strftime('%d')

        return '%s-%s-%s-%s' % (logType, oldYear, month, day)

    def __getOldLogFilePath(self, logType: str) -> str:
        logDirPath = self.__getLogDirPath(logType)
        oldLogName = self.__getOldLogName(logType)

        return self.__LOG_FILE_PATH % (logDirPath, oldLogName)

    def __removeOldLogFile(self, logType: str):
        oldLogFilePath = self.__getOldLogFilePath(logType)

        if path.exists(oldLogFilePath) and path.isfile(oldLogFilePath):
            remove(oldLogFilePath)

    def __getLogName(self, logType: str) -> str:
        year  = datetime.datetime.today().strftime('%Y')
        month = datetime.datetime.today().strftime('%m')
        day   = datetime.datetime.today().strftime('%d')

        return '%s-%s-%s-%s' % (logType, year, month, day)

    def __getLogFilePath(self, logType: str) -> str:
        logDirPath = self.__getLogDirPath(logType)
        logName    = self.__getLogName(logType)

        return self.__LOG_FILE_PATH % (logDirPath, logName)

    def __createLogFile(self, logFilePath: str):
        if not path.exists(logFilePath) or not path.isfile(logFilePath):
            with open(logFilePath, 'a'):
                pass

        chmod(logFilePath, 0o755)
