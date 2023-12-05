
{ pkgs ? import <nixpkgs> {} }:

with pkgs;



let



in mkShell {

  packages = [
    (pkgs.python311.withPackages (ps: [
      ps.numpy
      ps.scipy
      ps.matplotlib
      ps.pyyaml
      ps.imageio
    ]))
    imagemagick
  ];
}
