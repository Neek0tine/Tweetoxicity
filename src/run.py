from scripts import app
import os
from scripts.errors import defaultHandler

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 33507)), debug=True)
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.register_error_handler(Exception, defaultHandler)
    
    
