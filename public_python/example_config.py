
SECRET_KEY = 'sample_key'

DB_USER = 'db_user_login'
DB_PASSWORD = 'db_password'


class EmailConfigData:
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.example.com'
    EMAIL_PORT = 000
    EMAIL_HOST_USER = 'example@domain.com'
    EMAIL_HOST_PASSWORD = 'email_password'

    # Recipients list
    WAREHOUSE_RECIPIENTS = []
    SERVICE_RECIPIENTS = []
    OFFICE_RECIPIENTS = []