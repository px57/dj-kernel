# Http

#### \[SUCCESS]

```python
from kernel.http import Response

def yourfunction(request):
    res = Response(request=request)
    return res.success()
```

#### \[ERROR]

```python
res.error(error=None, code_error=None, error_descr=None)
```

#### \[FORM\_ERROR]

```python
from kernel.http import Response

def forget_password(request):
    """
        @description: This function handles the forget password request
    """
    res = Response(request=request)
    form = ForgotPasswordForm(request.POST)

    if not form.is_valid():
        return res.form_error(form)
```

#### \[SET\_VALUE\_WITH\_METHOD]

```python
res.injectdata = 21
```

#### \[SET\_VALUE\_WITH\_DICT]

```python
res.update({
    'injectdict': 21 
})
```

#### \[GET\_INTERFACE]

```python
res.get_interface()
```

#### \[GET\_SITE]

```python
res.get_site()
```

#### \[GET\_HOST]

```python
res.get_host()
```

#### \[GET\_REQUEST\_PROTOCOL]

```python
res.get_request_protocol()
```

#### \[GET\_REQUEST]

```
res.get_request()
```

#### \[CREATE\_CLIENT\_URL]

```python
res.create_client_url()
```
