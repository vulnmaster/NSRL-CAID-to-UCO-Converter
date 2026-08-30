# UCO validation graph

`uco-1.5.0.ttl` is a monolithic RDF/Turtle validation graph generated from
the ontology modules in the official
[UCO 1.5.0 release](https://github.com/ucoProject/UCO/releases/tag/1.5.0),
commit `7ebb3957e9e9a2e1bb9c66cd1ede8c912a726344`.

It was generated with RDFLib's `rdfpipe` using the same module set as UCO's
`tests/uco_monolithic.ttl` build target:

```bash
rdfpipe --input-format ttl --output-format ttl \
  ontology/*/*.ttl ontology/*/*/*.ttl > uco-1.5.0.ttl
```

SHA-256: `1e8b358abb4cee9f06738338951866186a4da1aef3d36358a2312d86e9992171`

The upstream UCO work is licensed under Apache License 2.0. A copy is in
`LICENSE` in this directory.
