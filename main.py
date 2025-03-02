from logger.logger import initialize_logger

logger = initialize_logger()

def main() -> None:
    logger.info('Main application started')
    logger.info('Main application finished')


if __name__ == '__main__':
    main()