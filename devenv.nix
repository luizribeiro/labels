{ pkgs, ... }:

{
  packages = with pkgs; [
    feh
    ptouch-print
  ];

  languages.python.enable = true;
  languages.python.poetry = {
    enable = true;
    activate.enable = true;
  };
}
