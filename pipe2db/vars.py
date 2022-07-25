METHOD_GET = 'get'
METHOD_CREATE = 'create'
METHOD_UPDATE = 'update'

MODEL = 'model'
UNIQUE_KEY = 'unique_key'
METHOD = 'method'
FOREIGIN_KEY_FIELDS = 'foreignkey_fields'
MANYTOMANY_FIELDS = 'manytomany_fields'
SOURCE_URL_FIELDS = 'source_url_field'
CONTENT_FILE_FIELDS = 'contentfile_fields'
RENAME_FIELDS = 'rename_fields'
EXCLUDE_FIELDS = 'exclude_fields'

VALIDATE_KEYS = [
    MODEL, UNIQUE_KEY, FOREIGIN_KEY_FIELDS,
    MANYTOMANY_FIELDS, SOURCE_URL_FIELDS,
    CONTENT_FILE_FIELDS, RENAME_FIELDS, EXCLUDE_FIELDS,
    METHOD,
]

DEFAULT_DB_NAME = 'pipe2db.sqlite3'
