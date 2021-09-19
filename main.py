import logging
import ssl
import os

from kmip.services.server import KmipServer
from kmip.services.server.auth import get_certificate_from_connection, get_client_identity_from_certificate 
import kmip

logger = logging.getLogger(__name__)

logging_level = os.getenv("LOGGING_LEVEL", "INFO")

get_certificate_from_connection_orig = get_certificate_from_connection
get_client_identity_from_certificate_orig = get_client_identity_from_certificate

magic_cert = '000'

def get_certificate_from_connection_new(connect):
    return get_certificate_from_connection_orig(connect) or magic_cert

def get_client_identity_from_certificate_new(cert):
    if cert == magic_cert:
        return 'VMWare Inc.'
    return get_client_identity_from_certificate_orig(cert)


kmip.services.server.auth.get_certificate_from_connection = get_certificate_from_connection_new
kmip.services.server.auth.get_client_identity_from_certificate = get_client_identity_from_certificate_new

class KmipServerNoVerify(KmipServer):
    def _setup_connection_handler(self, connection:ssl.SSLSocket, address):
        connection.context.verify_mode = 0
        super()._setup_connection_handler(connection, address)

if __name__ == '__main__':
    server = KmipServerNoVerify(
        config_path='./config/server.conf',
        log_path='./server.log',
        logging_level=logging_level,
        database_path='./storage/pykmip.db'
    )
    logger.info('Starting the KMIP server')
    
    try:
        server.start()
        server.serve()
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt received while serving')
        logger.debug("Exception", exc_info=True)
    except Exception as e:
        logger.exception('Exception received while serving: {0}'.format(e))
    finally:
        server.close()

    logger.info('Shutting down KMIP server')