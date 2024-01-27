# CHANGELOG



## v0.3.0 (2024-01-19)

### Build

* build: update preview image when building the package ([`2a8f7ca`](https://github.com/benoapp/turbo-case/commit/2a8f7ca327eae223862bb4bca22a8840cae72444))

### Documentation

* docs(readme.md): update `README.md` to match specs of the `project` command ([`1297f96`](https://github.com/benoapp/turbo-case/commit/1297f96daba714735364c3cab4bd5c12b6311eb3))

### Feature

* feat(upsert): support multiple files in the `upsert` command

resolves #20 ([`aef3553`](https://github.com/benoapp/turbo-case/commit/aef3553fd5c6a426426859132254d3c872cb19d3))

* feat: create `project` command that initializes a project

This command initializes a project by creating the below folder structure. The command will get the projects IDs by promting the user for the full projects names in Testiny, and then an API call will be made to get the project IDs. Note that I have made some changes to requirements in `README.md`. Eg: I am creating `.project.toml` instead of `_config.yaml` to be consistent with other parts of the project. I am also using slightly different folder names than the ones in the README.md. Also, most notably, I named the command `project` instead of `init`. However, those changes are minor and could be changed easily if needed.

```shell

path/to/project/project_name
├── .project.toml
└── app
    ├── Web
    └── mobile
        ├── Android
        └── iOS
```

resolves #24 ([`0d2a75d`](https://github.com/benoapp/turbo-case/commit/0d2a75d246d65d56e1888768996697c4b23e6bb1))

### Refactor

* refactor(print_banner): using rich.console instead of manually centering the text ([`97ecbcd`](https://github.com/benoapp/turbo-case/commit/97ecbcd27c6089cbe78112a3498600e87c2b0510))

### Style

* style(upsert): fix typo in `upsert` help message ([`fd34ca6`](https://github.com/benoapp/turbo-case/commit/fd34ca6cec780fd7f990459d7d7cb3e45c2b7c5f))

* style: use RGB colors for `upsert` &amp; `create` results

If all files were successful, then the result will be show in green. If none is successful, red will
be used. Yellow, otherwise. ([`dad7ef0`](https://github.com/benoapp/turbo-case/commit/dad7ef0d14e0c480f650284e5b7f0e7a147d48ca))

* style: using lowercase folder names in `project` command ([`2da52d0`](https://github.com/benoapp/turbo-case/commit/2da52d0a2d0a4983c45948d2d74ac90da572d143))

* style(read): modify `read` command to print in a YAML format not JSON

The `read` command now prints the test case in a more human readable way. It used to be print all
information, even non relavent one. Now, only important info is printed. Also, the old
`read_test_case` function is now renamed to `__get_test_case_json`

resolves #29 ([`e62e410`](https://github.com/benoapp/turbo-case/commit/e62e4103ed8d4844ef66d64a3cf407290520544a))

* style: print usage when `turbocase` is used with no commands ([`0438735`](https://github.com/benoapp/turbo-case/commit/043873541a189fa85d455fd1f233f826169a65f1))

* style: change the order of commands in `turbocase --help` ([`6312d8a`](https://github.com/benoapp/turbo-case/commit/6312d8a6e43199ad0a16310596f56bcffe378f0b))

### Unknown

* deploy: add Dockerfile ([`4d4f6e3`](https://github.com/benoapp/turbo-case/commit/4d4f6e3a15809b80163524693f3c3e85586f9547))


## v0.2.0 (2024-01-17)

### Breaking

* feat(.turbocase.toml): use a config file to store API key and other information

The user no longer needs to pass --api-key. Instead, the API key will be retrieved from the config
file. The user needs to run `turbocase config --api-key &lt;KEY&gt;` the first time he uses `turbocase` or
if he needs to reconfigure `turbocase` to use a new API key.

BREAKING CHANGE: The user no longer needs to pass --api-key. The user needs to run `turbocase config
--api-key &lt;KEY&gt;` the first time `turbocase` is used.

closes #10 ([`dd5765b`](https://github.com/benoapp/turbo-case/commit/dd5765b059a53518316541007e2884a8edc0cee3))

* refactor: remove abstract class and factory pattern

Turbocase now only supports Testiny. The factory pattern was completely removed from the source
code, simplifying the code and removing any constraints when designing the package.

BREAKING CHANGE: The factoy pattern and the abstract TestManagementSystem class are removed. ([`bafb7be`](https://github.com/benoapp/turbo-case/commit/bafb7bea349324066162e78bdde405cdca0a14a4))

* refactor: move `--api-key` and `--system` to main parser

The `--api-key` and `--system` flags are common between all subparser (commands). So, I moved them
to the main parser, ie: they will be specified right after `turbocase`. Eg: `turbocase --api-key
&lt;KEY&gt; --system &lt;SYSTEM&gt; [commands] [options]`

BREAKING CHANGE: The `--api-key` and `--system` flags should now be passed right after the main
command in the CLI (eg: `turbocase --api-key &lt;KEY&gt; create ...`). Previously, those flags were passed
after the subcommand (eg: `turbocase create --api-key &lt;KEY&gt; ...`). ([`79a087f`](https://github.com/benoapp/turbo-case/commit/79a087f7fd4e7f57c6bdba35706f62cd55d2f265))

### Build

* build: setup semantic release ([`07a2cea`](https://github.com/benoapp/turbo-case/commit/07a2cea11a7db8f9f02edc4782d72abc3ec72865))

* build: move `generate-preview.sh` to `scripts/` ([`7a2eb67`](https://github.com/benoapp/turbo-case/commit/7a2eb67522c741d4983e24fa0872b2ba35e45b93))

* build: add script to bump version and publish a release to GH ([`666d800`](https://github.com/benoapp/turbo-case/commit/666d800be3121cee977f7bb1370b8823b36069a7))

* build: add `jsonschema` to `requirements.txt` ([`c736272`](https://github.com/benoapp/turbo-case/commit/c736272039139977a4e6582ad7bf562b566c3937))

* build: remove pylint.yml GitHub Action ([`4e26f6a`](https://github.com/benoapp/turbo-case/commit/4e26f6abb281fe1505edd97a15b19817735b7a58))

* build: add GitHub Action to generate preview img when main is pushed ([`a930443`](https://github.com/benoapp/turbo-case/commit/a9304434824d566be53b0a9430f7648077f66544))

* build: creating the config file in the home directory ([`8afc69f`](https://github.com/benoapp/turbo-case/commit/8afc69fd7269a4d9eeba19493ac6afb0e17adac9))

* build: update package dependencies and package data ([`f8f0675`](https://github.com/benoapp/turbo-case/commit/f8f0675be0d5eb36abd480b194eef8c72b285fdd))

* build: move `requirements.txt` to root directory ([`db35438`](https://github.com/benoapp/turbo-case/commit/db354384c81828afd5784f88159805b31e2022ff))

### Chore

* chore: bump version to 2.0.0 ([`16dc1b3`](https://github.com/benoapp/turbo-case/commit/16dc1b3ac8849385afd28bafecb72f2e256531a2))

* chore: remove `toml` from requirements.txt ([`cee3509`](https://github.com/benoapp/turbo-case/commit/cee35091dd763e23a2911d3e4bdb2ecba8fa391b))

### Ci

* ci: remove GHA workflow that generates preview image ([`6cfd22e`](https://github.com/benoapp/turbo-case/commit/6cfd22ee7f5d2c1c3ad648cbfdacc00d4dce521a))

* ci: update pylint.yml to install requirements.txt ([`e1ac92f`](https://github.com/benoapp/turbo-case/commit/e1ac92f5a53a5b8cccc2cc0089ff618c32a98c1f))

* ci: create pylint.yml ([`d93feff`](https://github.com/benoapp/turbo-case/commit/d93feff62d83105b8a08b78eae240610877cf9c5))

### Documentation

* docs: improve example ([`c89bfc3`](https://github.com/benoapp/turbo-case/commit/c89bfc3a1da9efe9dba9903db4f866ec007f4cf8))

* docs: add requirements for generate command ([`25446e0`](https://github.com/benoapp/turbo-case/commit/25446e0e149ceebef6a72c64201f7db381690ae6))

* docs: add requirements for generate command ([`5ca9e97`](https://github.com/benoapp/turbo-case/commit/5ca9e9746a258acbeb26d1c056319ebfc3be2916))

* docs: update README.md with installation and usage guides

README.md now contains clear guides on how to install, configure, and use `turbocase` CLI tool

closes #8 ([`833df4f`](https://github.com/benoapp/turbo-case/commit/833df4f8c187a0a639b7c52cc83bb7367c3b59ca))

* docs: add docs to get_version ([`dd323c0`](https://github.com/benoapp/turbo-case/commit/dd323c0cc3e771951908452c35dc9e01e7002b3b))

* docs: add todo message to use `.env` to get the test system ([`6f742f7`](https://github.com/benoapp/turbo-case/commit/6f742f7db1e265078f7bbef1eb1364c66504bb36))

* docs(todo): add todo to find a better way to get the version ([`0793d7f`](https://github.com/benoapp/turbo-case/commit/0793d7fb714bfeb05f82421866b9416d070afec1))

### Feature

* feat: use more useful and colorful help and error messages

A status spinner is now displayed to the user while waiting for the command to finish running. Also,
rich_argparse is used to display more colorful help messages. ([`6ae022d`](https://github.com/benoapp/turbo-case/commit/6ae022d48b313e8d8ceaedbdb705c34269ba815e))

* feat: add functionality for config file ([`f0962a5`](https://github.com/benoapp/turbo-case/commit/f0962a5dd40a8948569e149163b494d4492166ce))

* feat: upsert_test_case returns `_tage` or `ID` instead of `None` ([`7aea3c9`](https://github.com/benoapp/turbo-case/commit/7aea3c9bff6df3ea8a548fa715f9ed0e93455d6f))

* feat: `update_test_case` returns `_etag` instead of `None` ([`e155ed0`](https://github.com/benoapp/turbo-case/commit/e155ed05bb0d3c4f82e37d4c30acbbbdb832a617))

* feat: `insert_test_case` returns `ID` instead of `None` ([`caacf01`](https://github.com/benoapp/turbo-case/commit/caacf015a15cb9b2971be98f51950d0d33439cab))

* feat: add the `upsert` command

Resolves #14 ([`7200677`](https://github.com/benoapp/turbo-case/commit/7200677dd1514a4d4353c51947b8501093f948ae))

* feat: add functionality of the update command in the CLI App ([`28d9b47`](https://github.com/benoapp/turbo-case/commit/28d9b47e47e6730a7082c5777f3943cf3f05560c))

* feat: handle the `read` command in the CLI app ([`20c9721`](https://github.com/benoapp/turbo-case/commit/20c97211d5e0d4c3e0c48b19fb54a6e6473069ed))

* feat: add `read` parser to the CLI app ([`26446b0`](https://github.com/benoapp/turbo-case/commit/26446b041ac03be8bbdf9b50b95c795268b63fce))

* feat: create `read_test_case()` function ([`2436aae`](https://github.com/benoapp/turbo-case/commit/2436aaecb211d3f0200fbf5307544f8a028b174b))

* feat: add funcitonality to update a test case ([`01fb894`](https://github.com/benoapp/turbo-case/commit/01fb89475d5bfae7d3f524fb4d1aa095d0f560c6))

* feat: add client code to update an existing test case

Only the function of the feature is written, the CLI app does not support it yet. ([`596e55e`](https://github.com/benoapp/turbo-case/commit/596e55ece1b1ddae8f5d426eacc128fa3397652d))

### Fix

* fix: fix API URL issue for Windows

I replaced `os.path.join` with `urllib.parse.urljoin`. The former uses backslashed in Windows which
is problomatic when joining URLs ([`8f8d9a6`](https://github.com/benoapp/turbo-case/commit/8f8d9a615f5552880576173db58bc6175644ab8c))

* fix: including package data when building the package

The file `Testiny_schema.json` is now included when building `turbocase`. ([`3194078`](https://github.com/benoapp/turbo-case/commit/31940786808c600d50cef3929d0cc2dfc8f5d471))

* fix: correct import paths of the Factory method ([`18f148e`](https://github.com/benoapp/turbo-case/commit/18f148e52af631f4f8d60c9328fa607931e985d6))

* fix: remove `--api-key` &amp; `--system` from upsert_parser ([`2b7ab38`](https://github.com/benoapp/turbo-case/commit/2b7ab389239fdb1fa759b031d06a65f4ee63e780))

* fix: handle case when the same test case is updated twice

resolves #11 ([`90e1ea4`](https://github.com/benoapp/turbo-case/commit/90e1ea403c9678a357eff43121d1f989dd569b33))

* fix: make the update command accept one file at a time ([`5249614`](https://github.com/benoapp/turbo-case/commit/524961482ed32162bc4ef1315a58a8acab3746fb))

### Performance

* perf: call factory method once in `handle_create_command()`

This change avoids creating a new (and identical) test management system in every iteration when
creating multiple test cases ([`b17e0bc`](https://github.com/benoapp/turbo-case/commit/b17e0bca39094b9720e5944e8db676bf94ee7646))

### Refactor

* refactor: remove unnecessary files ([`c772e1c`](https://github.com/benoapp/turbo-case/commit/c772e1c2689cf5f2e4ccdc4f4e83646610a4cda3))

* refactor(__version__): single-sourcing the package version in the __init__ file ([`bc3de50`](https://github.com/benoapp/turbo-case/commit/bc3de503baf90a5ee24c7e8a3053d71f3f311c46))

* refactor: set `__version__` to 1.0.0 ([`8754afd`](https://github.com/benoapp/turbo-case/commit/8754afd46312d050d056d8b3d78e36179d0b2739))

* refactor: change project structure to match a package structure ([`7af34d7`](https://github.com/benoapp/turbo-case/commit/7af34d712cf9c71b1322d4c1ffed0dd69f0cbf81))

* refactor: use factory method without the `Factory` class ([`b36de8f`](https://github.com/benoapp/turbo-case/commit/b36de8f7a1374e90647b922eec72d4f3d3f312ef))

* refactor: remove unneeded `handle_setup()` function

This function will be used later in a separate branch ([`47139c5`](https://github.com/benoapp/turbo-case/commit/47139c543ced85c9c25ab9cba735672a7d8602b7))

* refactor: add default user_id and etag args to `update_test_case()`

Those args can help preventing extra API requests

resolves #11 ([`d68fed2`](https://github.com/benoapp/turbo-case/commit/d68fed251e82b9ee8edd3f18929c0f2bafa3b902))

* refactor: add type hints to `handle_create_command()` &amp; `handle_read_command()` ([`6fd841c`](https://github.com/benoapp/turbo-case/commit/6fd841c1446b517e6254671358c08ae04625f31d))

* refactor: add `update_test_case()` to the abstract class `TestManagementSystem` ([`7d5ad85`](https://github.com/benoapp/turbo-case/commit/7d5ad85297200931f059b08ea649aff82199221c))

* refactor: add `@override` decorator ([`4e8fa27`](https://github.com/benoapp/turbo-case/commit/4e8fa27cb949b6a0823cdc5e98628333c1cbb2be))

* refactor: exported code that creates the parser to functions ([`79373dc`](https://github.com/benoapp/turbo-case/commit/79373dc6bae133a830a836e64ca01a49dfe5d87a))

### Style

* style: better hint messages

When an HTTP error is raised with status code 404, user is aksed to check the project ID in the
(YAML) test case file. ([`9072891`](https://github.com/benoapp/turbo-case/commit/9072891e61304b1e813b2de2e55d6c661afd2317))

* style: fix most PyLint issues, mainly documentations ([`125afd5`](https://github.com/benoapp/turbo-case/commit/125afd5e6107edf684f7410b5a13322f962abda9))

* style: update help messages printed to the user ([`5c40750`](https://github.com/benoapp/turbo-case/commit/5c407505766bb5f8a6e53dfe95ed6db38819311a))

* style: change help msgs for the `update` &amp; `upsert` commands ([`b5eaff2`](https://github.com/benoapp/turbo-case/commit/b5eaff23103c6c537f4eed4600cdf0172a472e2d))

* style: fix typo in help msg of the `update` command ([`f5075ea`](https://github.com/benoapp/turbo-case/commit/f5075eaf7759b92b4897d12cf9eb370de93b6a42))

* style: add color to error messages when creating new test cases ([`025d9b8`](https://github.com/benoapp/turbo-case/commit/025d9b85619f73907b6c17bbd7e0017ba1c4bc0c))

* style: add bold style to error messages ([`0127aaa`](https://github.com/benoapp/turbo-case/commit/0127aaad3a9da28b8207b1f3722cd7626aa4dfcb))

* style: rename `__read_test_case()` to `__read_test_case_schema()` ([`1e04688`](https://github.com/benoapp/turbo-case/commit/1e04688ef76ddcd34e2e447f3519cd72b8deeb72))

* style: change main help message ([`1965568`](https://github.com/benoapp/turbo-case/commit/1965568fcba6237427ed7f47d38cacabe32ec9cb))

* style: add hints when creating test cases ([`279b2be`](https://github.com/benoapp/turbo-case/commit/279b2be27bee7cfc6e29f90ee18f34784a87d6f4))

* style: change help message for `add` command in the CLI App ([`deb83a4`](https://github.com/benoapp/turbo-case/commit/deb83a4c38367bfe0717f925ecc293dc2917adcb))

* style: change CLI APP desc and usage msg ([`d965ff4`](https://github.com/benoapp/turbo-case/commit/d965ff4ef25baa7d1395103588dcebc032119c9a))


## v0.1.0 (2023-12-28)

### Build

* build: Add .gitignore and requirements.txt, delete .gitkeep

feat: add simple entry-level CLI functionality

The main functionality available right now is creating test cases from YAML files.

build: added commitizen to incorporate conventional commits

Now contributors can use `git cz` instead of `git commit` and an interactive session will appear to
help in writing better commits.

refactor: moved custom help formatter class to utility

refactor: change -f a positional arg and removed choices from -s

refactor: remove arguments specific to Testiny

Arguments such as —project and —owner have been removed from the create command and should now be
passed to the YAML file of the test case. This step ensures generalization when implementing logic
for management systems other than Testiny.

feat: implement the logic of the create command

The factory method pattern is used to customize the logic of each test management system.
Currently, Testiny is only supported.

resolves #6

build: add requirements.txt

Note: I am using pipreqs to automate the process of creating this file

build: remove node_modules, package.json and package-lock.json

resolves #6

feat: make Testiny the default for --system option

feat: infer owner ID from API key instead of the YAML file

build: Add .gitignore and requirements.txt, delete .gitkeep

feat: add simple entry-level CLI functionality

The main functionality available right now is creating test cases from YAML files. ([`2578ec4`](https://github.com/benoapp/turbo-case/commit/2578ec48e8b6c35ef66625e5bb6bb1294886d07b))

### Chore

* chore: add TODO.md to .gitignore ([`e65e200`](https://github.com/benoapp/turbo-case/commit/e65e200bd8b14003294780e73b336f8c433a0e35))

* chore: add temp/ to .gitignore

The temp/ direcotry holds temporary files to allow me test some mini features while developing ([`c5c327e`](https://github.com/benoapp/turbo-case/commit/c5c327e4f4ec5d269421e7e7493af982fdd99f65))

* chore: add .env file ([`598d815`](https://github.com/benoapp/turbo-case/commit/598d815e715cf77463a7dea75a377c8d7ea90a7c))

* chore: replace current .gitignore with an online template ([`afa9e37`](https://github.com/benoapp/turbo-case/commit/afa9e3742228c6f9dd7d4a5b45a845761f433f18))

* chore: add venv to .gitignore ([`5f5d6e0`](https://github.com/benoapp/turbo-case/commit/5f5d6e06fe920415c845cd61dcde28409c36e3a6))

### Documentation

* docs(todo): add todo to rewrite code that reads JSON Schema ([`f334aba`](https://github.com/benoapp/turbo-case/commit/f334aba4037b220eba5bdbc54fed5c800ea152ca))

* docs: modify sample test files to reflect the leatest changes ([`a44d96b`](https://github.com/benoapp/turbo-case/commit/a44d96bf891bd4a73f6eb52b0acad52f53b00d18))

* docs(readme.md): replace conventional commits badge

Replaced `commitizen friendly` badge with `Conventional Commits`. ([`d3dedd4`](https://github.com/benoapp/turbo-case/commit/d3dedd486db61c77e6da726d699257ed57936446))

* docs: add example project ([`5a06c6b`](https://github.com/benoapp/turbo-case/commit/5a06c6b25262ff09b31dd38e1d5a2d25000240aa))

* docs: updated refs and fixed style issues in README.md ([`3f642f9`](https://github.com/benoapp/turbo-case/commit/3f642f9fb615af1c2a6f2cd14da4008f96e52116))

* docs: add contribution guide and second session notes ([`14e7c23`](https://github.com/benoapp/turbo-case/commit/14e7c236173c05741c1d55b2dbe1846fd6701352))

* docs: add README as the application definition

Resolves #1 ([`0c9fc84`](https://github.com/benoapp/turbo-case/commit/0c9fc840f0013ff759b8f5c38c99b3995cd1793d))

### Feature

* feat: add client code to update an existing test case

Only the function of the feature is written, the CLI app does not support it yet. ([`2d60484`](https://github.com/benoapp/turbo-case/commit/2d60484819635ec88c1624612e70767219b7c269))

### Fix

* fix: raise error if API key is invalid ([`d2381f5`](https://github.com/benoapp/turbo-case/commit/d2381f59ca52751d0a7805c7aec400e17e09e01e))

* fix: validate test case YAML files using JSON Schema ([`76957e5`](https://github.com/benoapp/turbo-case/commit/76957e56929bcff77ef1aee52b89527ec9393fbe))

### Refactor

* refactor: put each test management system class in it&#39;s own file

Testiny class now lives in it&#39;s own python file. This helps in organising the src code, especially
when more test management systems are added later. ([`087d020`](https://github.com/benoapp/turbo-case/commit/087d020aafcdc39bc199c15c1aef4e9d7abe0f9c))

* refactor: rename TestSystem to TestManagementSystem ([`a57965b`](https://github.com/benoapp/turbo-case/commit/a57965bc47b4dd38bc65a4cdf6ab54e9e3ee8a61))

### Test

* test: add a bad test case example ([`2314889`](https://github.com/benoapp/turbo-case/commit/23148896e51db04f55fbc26813eb1ed82cd3a504))

* test: correct typo in `preconditions` in partial.feature.yaml ([`334fa46`](https://github.com/benoapp/turbo-case/commit/334fa461c4d70b8b9f4f3549ae95c659b9065aed))
