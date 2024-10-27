o = let
  pkgs = import <nixpkgs>;
  options = {
    age = pkgs.lib.mkOption { type = pkgs.lib.types.str; };
  };
in { config = { options.age = "23"; }; } 
