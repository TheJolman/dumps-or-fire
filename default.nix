with import <nixpkgs> {};
mkShell {
  nativeBuildInputs = [
    python314
    uv
  ];
}
