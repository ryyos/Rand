import logging
from datetime import datetime as time
from icecream import ic

class Logs:
    def __init__(self) -> None:

        logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p', encoding="utf-8", level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        console = logging.StreamHandler()
        console.setLevel(level=logging.INFO) 
        console.setFormatter(formatter)

        file_log = logging.FileHandler(filename="logs/logging.log", encoding="utf-8")
        file_log.setLevel(level=logging.DEBUG)
        file_log.setFormatter(formatter)

        logger = logging.getLogger()
        for existing_handler in logger.handlers[:]:
            logger.removeHandler(existing_handler)

        logger.addHandler(console)
        logger.addHandler(file_log)

    def info(self, offset: int, status: int, requests: str, response: any) -> None:
        logger = logging.getLogger()
        logger.info(f"requests: {requests}")
        logger.info(f"offset: {offset}")
        logger.info(f"status: {status}")
        logger.info(f"locations: {response['location'].get('name')}")
        logger.info(f"type: {response['location'].get('type')}")
        logger.info(f"Latitude: {response['location'].get('lat')}")
        logger.info(f"longitude : {response['location'].get('lon')}")

    def err(self,response: any, requests: str) -> None:
        logger = logging.getLogger()
        logger.error(f"requests: {requests}")
        logger.error(f"code: {response.get('code')}")
        logger.error(f"type: {response.get('type')}")
        logger.error(f"message: {response.get('message')}")