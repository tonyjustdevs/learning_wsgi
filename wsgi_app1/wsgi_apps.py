# wsgi_app_v1_echo                

def wsgi_app_v1_echo(environ: dict[str, bytes], start_response: function):
    # wsgi requirements
    # 1. calls start_response()
    # 2. return iterable[byte_strings]
    start_response(status="200 OK", headers=[(None,None)])
    # environ["wsgi.input"] = buffer (type: bytes_string)  its only echo only app 
    data_bytes: bytes = environ["wsgi.input"]  # since its already in byte form
    print(f"[internal] data_bytes: {data_bytes} inside wsgi_app_v1_echo() from file:{__file__} name:{__name__}")
    # version 1: just one single bytes string
    # version 2: data_bytes elements? like [b"first", b"second", "third"]
 
    return list(data_bytes) # version 1
    # Handling WSGI Lazy Execution
    # - A parsed element directly (x_wsgiorg_parsed_response)
    # - Or write to the writer (manual chunks)
    # - Or yield strings from the iterator