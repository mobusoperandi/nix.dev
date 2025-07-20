(automatic-direnv)=
# Automatic environment activation with `direnv`

Instead of manually activating the environment for each project, you can reload a [declarative shell](declarative-reproducible-envs) every time you enter the project's directory or change the `shell.nix` inside it.

1. [Make nix-direnv available](https://github.com/nix-community/nix-direnv)
2. [Hook it into your shell](https://direnv.net/docs/hook.html)

For example, write a `shell.nix` with the following contents:

`myproject/shell.nix`:

```nix example="automatic-environment-direnv"
let
  pkgs = import <nixpkgs> { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    direnv
    which
    hello
  ];
}
```

From the top-level directory of your project run:

```shell-session example="automatic-environment-direnv"
$ cd myproject
$ echo "use nix" > .envrc
$ nix-shell
...
$ direnv allow
...
$ which hello
/nix/store/...-hello-...
```

The next time you launch your terminal and enter the top-level directory of your project, `direnv` will automatically launch the shell defined in `shell.nix`

```shell-session not-tested="nix-shell-is-not-persisted"
$ which hello
/nix/store/...-hello-...
```

`direnv` will also check for changes to the `shell.nix` file.

Changing the file as below:

`shell.nix`:

```nix example="automatic-environment-shell-hook"
let
  pkgs = import <nixpkgs> { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    hello
  ];

  # Add shellHook below
  shellHook = ''
    hello
  '';
}
```

The diff would be as follows:

```diff not-tested="documentation"
 let
   pkgs = import <nixpkgs> { config = {}; overlays = []; };
 in

 pkgs.mkShellNoCC {
   packages = with pkgs; [
     hello
   ];
+
+  shellHook = ''
+    hello
+  '';
 }
```

The running environment should reload itself after the first interaction (run any command or press `Enter`).

```shell-session example="automatic-environment-shell-hook"
$ nix-shell
Hello, world!
...
```
