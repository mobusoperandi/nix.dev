(python-dev-environment)=
# Setting up a Python development environment

In this example you will build a Python web application using the [Flask](https://flask.palletsprojects.com) web framework as an exercise.
To make best use of it you should be familiar with [defining declarative shell environments](declarative-reproducible-envs).

Create a new file called `myapp.py` and add the following code:

`myapp.py`:

```python example="python-environment"
#!/usr/bin/env python
from multiprocessing import Process
import time
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {
        "message": "Hello, Nix!"
    }

def run():
    server = Process(target=app.run)
    return server


if __name__ == "__main__":
    server = run()
    server.start()
    time.sleep(1)
    server.terminate()
    server.join()
```

This is a simple Flask application which serves a JSON document with the message `"Hello, Nix!"`.

Create a new file `shell.nix` to declare the development environment:

`shell.nix`:

```nix example="python-environment"
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python3.withPackages (ps: [ ps.flask ]))
    curl
    jq
  ];
}
```

This describes a shell environment with an instance of `python3` that includes the `flask` package using [`python3.withPackages`](https://nixos.org/manual/nixpkgs/stable/#python.withpackages-function).
It also contains [`curl`], a utility to perform web requests, and [`jq`], a tool to parse and format JSON documents.

[`curl`]: https://search.nixos.org/packages?show=curl
[`jq`]: https://search.nixos.org/packages?show=jq

Both of them are not Python packages.
If you went with Python's [virtualenv](https://virtualenv.pypa.io/en/latest/), it would not be possible to add these utilities to the development environment without additional manual steps.

Run `nix-shell` to enter the environment you just declared:

```shell-session example="python-environment"
$ NIX_SHELL_PRESERVE_PROMPT=1 nix-shell
...
$ python ./myapp.py
...
```

Start the web application within this shell environment:

```shell-session not-tested="hangs-due-to-no-user-interaction"
[nix-shell:~]$ python ./myapp.py
 * Serving Flask app 'myapp'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000
Press CTRL+C to quit
```

You now have a running Python web application.
Try it out!

Open a new terminal to start another session of the shell environment and follow the commands below:

```shell-session not-tested="nix-shell-is-not-persisted"
$ nix-shell

[nix-shell:~]$ curl 127.0.0.1:5000
{"message":"Hello, Nix!"}

[nix-shell:~]$ curl 127.0.0.1:5000 | jq '.message'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    26  100    26    0     0  13785      0 --:--:-- --:--:-- --:--:-- 26000
"Hello, Nix!"
```

As demonstrated, you can use both `curl` and `jq` to test the running web application without any manual installation.

You can commit the files we created to version control and share them with other people.
Others can now use the same shell environment as long as they have [Nix installed](install-nix).

## Next steps

- [](packaging-tutorial)
- [](file-sets-tutorial)
- [](automatic-direnv)
- [](./dependency-management.md)
