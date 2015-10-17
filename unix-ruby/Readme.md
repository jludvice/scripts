## bomizer
=======

This is helper script for migrating Maven dependencies using BOM (build of materials).

It goes through all pom.xml files in given path and removes version from project/dependencies/dependency element.
```
usage: bomizer.rb -p path-to-sources
```

_Useful for migrating bigger maven project to usage of BOM._