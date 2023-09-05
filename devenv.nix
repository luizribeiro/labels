{ pkgs, ... }:

{
  packages = with pkgs; if pkgs.stdenv.isDarwin then [] else [
    feh
    ptouch-print
  ];

  languages.python.enable = true;
  languages.python.poetry = {
    enable = true;
    activate.enable = true;
  };
}
