import logging

log = logging.getLogger()

log.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)