import validators

if not validators.url("http://google"):
    print("not valid")
