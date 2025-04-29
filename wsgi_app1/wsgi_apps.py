# wsgi_app_v1_echo                
def wsgi_app_v1_echo(environ, start_response):
    # wsgi requirements
    # 1. calls start_response()
    # 2. return iterable[byte_strings]
    
    # environ["wsgi.input"] = buffer (type: bytes_string)  its only echo only app 
    data_bytes = environ["wsgi.input"]  # since its already in byte form
    
    # version 1: just one single bytes string
    # version 2: data_bytes elements? like [b"first", b"second", "third"]
 
    return [data_bytes] # version 1