import logging
import os
from datetime import datetime

class LoggerUtil:

    @staticmethod
    def get_logger(name):

        logger=logging.getLogger(name)
        if logger.handlers:
            return logger
        
        logger.setLevel(logging.INFO)#默认等级

        log_format=logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

        #控制台
        console_handler=logging.StreamHandler()
        console_handler.setFormatter(log_format)

        #文件
        log_dir="../temp/logs"
        os.makedirs(log_dir,exist_ok=True)
        log_file=os.path.join(log_dir,f"test_{datetime.now().strftime('%Y%m%d')}.log")

        file_handler=logging.FileHandler(log_file,encoding="utf-8")
        file_handler.setFormatter(log_format)

        #添加到logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger