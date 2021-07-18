import os

if os.environ.get("ENVIRONMENT") == 'prod':
    from .prod_config import *
else:
    from .dev_config import *