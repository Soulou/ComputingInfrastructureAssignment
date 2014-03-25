Computing Infrastructure Assignment @ Cranfield
===============================================

This project gathers different tool to use over the SAGA API.

You can find the completete documentation on the wiki of the project:

https://github.com/Soulou/ComputingInfrastructureAssignment/wiki


Summary
-------

```sh
$ ls <directory> 
$ cat [--outfile/-o outfile] file [file …]
$ rm file [file …]
$ copy [--force/-f] [--verbose/-v] file [file …] dest
$ exec [--infile/-i file] [--outfile/-o] -r connect_string -- <command> [args …]
$ run_workflow [--verbose/-v] <workflow_file>
```

### Common flags

```
--user|-u <user>
--identify|-i <ssh_private_key>
--certificate|-c <X509_certificate>
```

Please look at the [documentation](https://github.com/Soulou/ComputingInfrastructureAssignment/wiki) for more details
