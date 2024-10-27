let
  pkgs = import <nixpkgs> {};
  options = {
    age = pkgs.lib.mkOption { type = pkgs.lib.types.str; };
  };
  config = import <nixpkgs/nixos> {
    configuration = {
      age = "23";
    };
  };
in config 
