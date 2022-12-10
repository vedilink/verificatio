# Verificatio

A domain possession verification library for everyone written in Python featuring a Martini-like API with much better performance. If you need to validate the ownership of a domains, start doing some [Verificatio](https://translate.google.com/?sl=lv&tl=en&text=verific%C4%81ti%C5%8D%20&op=translate).


### Supported strategies

All strategies takes 3 arguments: the domain to verify, a static DNS safe `prefix` like "yourservice-domain-verification" and a randomly generated `code`. Domains can be verified by either adding a DNS record (CNAME or a TXT record) or by adding content to the existing website (a meta tag or uploading an empty file with the specified name).

More specifically,

- **DNS TXT record**: checks for the `{prefix}={code}` string present in one of the `TXT` records on the domain name.

- **DNS CNAME record**: checks for the existence of `CNAME` record composed on the static `{prefix}-{code}` on the domain pointing to domain (usually yours) which the host is {prefix} (i.e.: {prefix}.yourdomain.com). **NOTE:** you may want to make sure that {prefix}.yourdomain.com resolves to something as some zone editors may check that.

- **Meta Tag**: Checks for the presence of a `<meta name="{prefix}" content="{code}">` tag in the `<head>` part of the domain's home page using either HTTP or HTTPS protocol.

- **File**: Checks for the presence of a file named `{code}.html` at the root of the domain's website using either HTTP or HTTPS protocol.


#### Installation

To install verificatio, simply:

```zsh
pi@K47CH22 ~ % git clone https://github.com/vedilink/verificatio.git
pi@K47CH22 ~ % python setup.py install
```


#### Running tests

```zsh
pi@K47CH22 ~ % pip install tox
pi@K47CH22 ~ % tox
```


#### Usage

Verificatio will check the domain with the selected strategy and return `True` in case of a successful verification.

```python
import verificatio

# user has access to alter the DNS records of the domain

verificatio.generate('example.com', 'CNAME') 
# ask the user to add the CNAME record
verified = verificatio.verify('example.com', 'CNAME') # returns a bool
if verified:
    print("This domain is verified")

# user has access to the content hosted on the domain

verificatio.generate('example.com', 'META') 
# ask the user to add the meta tag
verified = verificatio.verify('example.com', 'META') # returns a bool
if verified:
    print("This domain is verified")
```


### Configuration

The library by default uses [SQLite](https://www.sqlite.org/index.html) to store and match generated verification payloads, which can be easily swapped with any database backend by passing the database connection url to `DATABASE_URL` environment variable.


### Licenses

All source code is licensed under the [MIT License](LICENSE).
