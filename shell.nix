{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = with pkgs; [
    python312
    uv
  ];

  shellHook = ''

  '';
}
