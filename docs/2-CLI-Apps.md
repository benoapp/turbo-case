# CLI Apps and Agile

## CLI Apps

1. Use a library such as `Click` to:
    1. Reduce String manipulation
    2. Hustle free `--help` option support
2. CLI apps will usually follow a pattern:
```shell
ls -l -a

find -name -n

cliapp --long-name -l command --command-option -c file.txt

<cmd> [--flags] command [--flags-command] mandatoryArg [optionalArgs]

find -h

find --help

find

find help

fined --version

find -v // -v ? version ? verbose

find version

cliapp --source='./src/'
cliapp --source ./src/  images  --help
cliapp --source ./src/  images --name=hello --help
```

## Agile Kanban in GitHub

1. Use Kanban board to know who is working on what
2. Convert Kanban board to issue if it needs coding
3. Link code with issue number by commenting in the footer of the commit "resolves #123"
4. Push changes to a new branch for review

