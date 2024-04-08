
import logging


def has_level_handler(logger: logging.Logger) -> bool:
    """Check if there is a handler in the logging chain that will handle the
    given logger's :meth:`effective level <~logging.Logger.getEffectiveLevel>`.
    """
    level = logger.getEffectiveLevel()
    current = logger

    while current:
        if any(handler.level <= level for handler in current.handlers):
            return True

        if not current.propagate:
            break

        current = current.parent

    return False


def create_logger(app) -> logging.Logger:
    """Get the Flask app's logger and configure it if needed.
    The logger name will be the same as
    :attr:`app.import_name <flask.Flask.name>`.
    When :attr:`~flask.Flask.debug` is enabled, set the logger level to
    :data:`logging.DEBUG` if it is not set.
    If there is no handler for the logger's effective level, add a
    :class:`~logging.StreamHandler` for
    :func:`~flask.logging.wsgi_errors_stream` with a basic format.
    """
    default_handler = logging.FileHandler(
        app.config['LOG_FILE_MAIN_NAME'])  # type: ignore
    default_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )

    logger = logging.getLogger(app.name)

    if app.debug and not logger.level:
        logger.setLevel(logging.DEBUG)

    if not has_level_handler(logger):
        logger.addHandler(default_handler)

    return




from threading import Timer as T

def main():
    a = 5

    def foo(ii:str):
        print(ii*5)
    
    tt = T(3, foo)

    tt.start()

main()

