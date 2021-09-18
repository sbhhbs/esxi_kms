import logging
import ssl
from kmip.services.server import KmipServer
from kmip.services.server.auth import get_certificate_from_connection, get_client_identity_from_certificate 
import kmip

logger = logging.getLogger(__name__)

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

class KmipServerBob(KmipServer):
    def _setup_connection_handler(self, connection:ssl.SSLSocket, address):
        connection.context.verify_mode = 0
        super()._setup_connection_handler(connection, address)

if __name__ == '__main__':
    server = KmipServerBob(
        # hostname='127.0.0.1',
        # port=5696,
        # certificate_path='./cert.key',
        # key_path='./key.key',
        # ca_path='./cert.key',
        # auth_suite='Basic',
        config_path='./config/server.conf',
        log_path='./server.log',
        # policy_path='./policies/',
        # enable_tls_client_auth=True,
        # tls_cipher_suites=[
        #     'TLS_RSA_WITH_AES_128_CBC_SHA256',
        #     'TLS_RSA_WITH_AES_256_CBC_SHA256',
        #     'TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384'
        # ],
        # ssl_version='PROTOCOL_SSLv23',
        logging_level='DEBUG',
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
    # finally:
        # server.close()

    logger.info('Shutting down KMIP server')