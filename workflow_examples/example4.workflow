JOB A ./cat -o ssh://localhost/tmp/hosts ssh://localhost/etc/hosts
JOB B ./exec -i ssh://localhost/tmp/hosts -o /tmp/hosts_grep -r ssh://localhost -- grep localhost
JOB C ./copy /tmp/hosts_grep ssh://localhost/tmp/grep
JOB D ./cat ssh://localhost/tmp/grep
JOB E ./rm ssh://localhost/tmp/hosts_grep ssh://localhost/tmp/hosts

PARENT B CHILD A
PARENT C CHILD B
PARENT D CHILD C
PARENT E CHILD D
