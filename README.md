# Ulysse

## Vision

The aim of that project is to ease and speed up the kick off when the
[#OpenSirene hackathon](https://www.etalab.gouv.fr/opensirene-un-hackathon-pour-preparer-louverture-du-registre-des-entreprises-sirene)
starts as of November, 15th.

With that small Python script you will be able to load a subset of the huge CSV
file provided during the hackathon to only work on a given domain. Additionally,
you can export a part of the loaded data as JSON or CSV.

Technically, the CSV is loaded within Redis and then served with Sanic. It
should not be necessary to be a Python developer to use the project. Please
please please report any issue you encounter to improve the project.

Check [detailed use cases](#use-cases) for a better idea of what can be achieved
and then follow the [installation instructions](#installation) if it finally
fits your needs.


## Ethics

This project operates under the W3C's
[Code of Ethics and Professional Conduct](https://www.w3.org/Consortium/cepc):

> W3C is a growing and global community where participants choose to work
> together, and in that process experience differences in language, location,
> nationality, and experience. In such a diverse environment, misunderstandings
> and disagreements happen, which in most cases can be resolved informally. In
> rare cases, however, behavior can intimidate, harass, or otherwise disrupt one
> or more people in the community, which W3C will not tolerate.
>
> A Code of Ethics and Professional Conduct is useful to define accepted and
> acceptable behaviors and to promote high standards of professional
> practice. It also provides a benchmark for self evaluation and acts as a
> vehicle for better identity of the organization.

We hope that our community group act according to these guidelines, and that
participants hold each other to these high standards. If you have any questions
or are worried that the code isn't being followed, please contact the owner of the repository.


## Language

The development language is English. All comments and documentation should be written in English, so that we don't end up with “franglais” methods, and so we can share our learnings with developers around the world.

However, the domain language is French. We consider each tax, collecting organism and French regulation as a domain-specific term. In the same fashion, well-known abbreviations of these domain-specific terms are accepted.


## Installation

Retrieve the current repository, then either make a dedicated virtualenv
or just type that command if you are not a Python developer:

```shell
$ pip install -r requirements.txt
```

In both cases, you have to run the script with Python 3.5+.

Note that you might need to [install pip](https://pip.pypa.io/en/stable/installing/) before.

If you plan to make HTTP requests to retrieve filtered data, we strongly recommend
using [httpie](https://httpie.org/) instead of curl, it should have been
installed through the load of the requirements.txt file.

You will need a running Redis server too. The installation and launch
depends on your OS. For instance for macOS:

```shell
$ brew install redis
$ redis-server
```


## Use cases

First of all, you can have access to the help of the module at any given time:

```shell
$ python -m ulysse --help
```

### Limiting the huge Sirene CSV file

Before starting, you need to define the number of lines you want to load within
the local database. Default is 1000 to be able to try fast, the whole stock
file is about 12 millions lines. It takes about 9 minutes to load 500000
lines with a dozen of keys.

Next, you choose which columns you want to work on, loading all columns is
probably irrelevant for the scope of a hackathon. Focus on a given domain
and iterate quickly. If you miss one column, it should not be too long to load
a new database.

Once you did that, it is time to call the script with these given parameters
(add `--columns SIREN NIC etc` if you do not want default ones which are
`SIREN NIC L1_NORMALISEE TEFET DEFET DEPCOMEN APEN700 CATEGORIE DCREN DATEMAJ`):

```shell
$ python -m ulysse load_stock --filename path/to/sirc.csv --lines 20000
INFO:ulysse.database:👌 Connected to Redis
INFO:ulysse.loaders:👉 Loading 20000 lines from path/to/sirc.csv
INFO:ulysse.loaders:💧 Already 10000 lines loaded
INFO:ulysse.loaders:💧 Already 20000 lines loaded
INFO:ulysse.loaders:💦 Storing correspondences (last step!)
INFO:ulysse.loaders:🌊 20000 lines loaded with success
```

The beautifully emoji-ed log will hopefully help you to understand what is
happening. Do not forget to launch your Redis server first!


### Playing with data (optional/advanced)

At that point, you should have a loaded Redis database.

If you are familiar with Python and/or Redis, you can start querying that
subset. For instance:

```shell
$ python
>>> from ulysse.database import db
INFO:ulysse.database:👌 Connected to Redis
>>> from ulysse.database import retrieve_sirets
INFO:ulysse.database:👌 Connected to Redis
>>> sirets = retrieve_sirets('NIC', '00056', limit=3)
>>> print(sirets)
['00542002100056', '00664182300056', '00735020000056']
>>> from ulysse.database import retrieve_siret
>>> retrieve_siret(sirets[0])
{'20110719': '{"DATEMAJ": "20110719", "L1_NORMALISEE": "ETABLISSEMENTS LUCIEN BIQUEZ", "APEN700": "4669B", "DEPCOMEN": "80001", "SIREN": "005420021", "DCREN": "195401", "NIC": "00056", "DEFET": "2009", "TEFET": "11", "CATEGORIE": "PME"}'}
>>> from ulysse.database import decode_siret
>>> decode_siret(retrieve_siret(sirets[0]), ['SIREN', 'L1_NORMALISEE'])
{'20110719': {'L1_NORMALISEE': 'ETABLISSEMENTS LUCIEN BIQUEZ', 'SIREN': '005420021'}}
```

The low-level API gives you the more modular and customizable way to retrieve
data but it can be a bit tedious to do that by hand. If you are totally lost,
the next section will hopefully help you!


### Quick and dirty export in CSV or JSON

You can serve your data through HTTP for an easier access.

You have to launch the local server:

```shell
$ python -m ulysse serve --columns SIREN NIC L1_NORMALISEE
INFO:ulysse.database:👌 Connected to Redis
INFO:sanic.log:Goin' Fast @ http://0.0.0.0:8000
```

Now you will be able to issue HTTP requests from another command-line
to retrieve data as CSV:

```shell
$ http :8000/NIC/00056 limit==2 format==csv columns==SIREN,NIC,L1_NORMALISEE
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 108
Content-Type: text/plain; charset=utf-8
Keep-Alive: timeout=60

SIREN;NIC;L1_NORMALISEE
005420021;00056;ETABLISSEMENTS LUCIEN BIQUEZ
006641823;00056;MONSIEUR PHILIPPE PLOGE
```

And/or JSON:

```shell
http :8000/NIC/00056 limit==3 format==json columns==SIREN,L1_NORMALISEE
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 232
Content-Type: application/json; charset=utf-8
Keep-Alive: timeout=60

[
    {
        "20110719": {
            "L1_NORMALISEE": "ETABLISSEMENTS LUCIEN BIQUEZ",
            "SIREN": "005420021"
        }
    },
    {
        "20150902": {
            "L1_NORMALISEE": "MONSIEUR PHILIPPE PLOGE",
            "SIREN": "006641823"
        }
    },
    {
        "20120120": {
            "L1_NORMALISEE": "ENTREPRISE MINETTO",
            "SIREN": "007350200"
        }
    }
]
```

You can play with GET parameters (`limit`, `format` and `columns`) to
retrieve the pertinent data for your use-case.


### Dealing with history (optional)

You can load updates from daily files generated (here again, you can pass
a `--columns` parameter to customize extra columns loaded,
default are `VMAJ DATEMAJ EVE DATEVE`:

```shell
$ python -m ulysse load_updates --folder path/to/MisesajourQuotidiennes/
INFO:ulysse.database:👌 Connected to Redis
INFO:ulysse.loaders:👉 Loading data from path/to/MisesajourQuotidiennes/sirc-..._124141890.csv
INFO:ulysse.loaders:💧 Already 3000 lines loaded
INFO:ulysse.loaders:💧 Already 6000 lines loaded
INFO:ulysse.loaders:💧 Already 9000 lines loaded
INFO:ulysse.loaders:💧 Already 12000 lines loaded
INFO:ulysse.loaders:🐣 Creations: 4678 — 👥 Modifications: 2759 — 💀 Deletions: 3357 — 🤑 Commercial: 4 — 💸 Non commercial: 8
[…]
INFO:ulysse.loaders:🌊 475065 items loaded with success
```

The full load takes about 12 minutes to complete with default columns.
Once it's achieved, you will have more information when you perform
a query against the server (note the use of the `offset` parameter
useful for pagination):

```shell
$ http :8000/NIC/00056 limit==2 offset==44 format==json columns==SIREN,L1_NORMALISEE,DATEMAJ,EVE
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 781
Content-Type: application/json; charset=utf-8
Keep-Alive: timeout=60

[
    {
        "20140607": {
            "DATEMAJ": "20140607",
            "L1_NORMALISEE": "SERVICE INSTALLATION DEPANNAGE ELECTRO",
            "SIREN": "070801659"
        },
        "20160725": {
            "DATEMAJ": "20160725",
            "EVE": "MS",
            "L1_NORMALISEE": "SERVICE INSTALLATION DEPANNAGE ELECTRO",
            "SIREN": "070801659"
        },
        "20160726": {
            "DATEMAJ": "20160726",
            "EVE": "MS",
            "L1_NORMALISEE": "SERVICE INSTALLATION DEPANNAGE ELECTRO",
            "SIREN": "070801659"
        },
        "20160817": {
            "DATEMAJ": "20160817",
            "EVE": "MS",
            "L1_NORMALISEE": "SERVICE INSTALLATION DEPANNAGE ELECTRO",
            "SIREN": "070801659"
        },
        "20160818": {
            "DATEMAJ": "20160818",
            "EVE": "MS",
            "L1_NORMALISEE": "SID ELECTRONIQUE",
            "SIREN": "070801659"
        },
        "20160826": {
            "DATEMAJ": "20160826",
            "EVE": "SS",
            "L1_NORMALISEE": "SID ELECTRONIQUE",
            "SIREN": "070801659"
        }
    },
    {
        "19981126": {
            "DATEMAJ": "19981126",
            "L1_NORMALISEE": "BETON CONTROLE COTE D AZUR",
            "SIREN": "071503569"
        }
    }
]
```

Here the company with `SIREN` "070801659" issued a `MS` (headquarter change)
as of 2016-07-26 and 2016-08-17 (?!) and then a `SS` (headquarter close)
as of 2016-08-26.

Another example:

```shell
$ http :8000/SIREN/024049124 limit==25 format==csv columns==SIREN,NIC,L1_NORMALISEE,DATEMAJ,EVE   239ms
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 1035
Content-Type: text/plain; charset=utf-8
Keep-Alive: timeout=60

SIREN;NIC;L1_NORMALISEE;DATEMAJ;EVE
024049124;00027;DOUKA BE;20131125;
024049124;00035;BOURBON DISTRIBUTION MAYOTTE;20131125;
024049124;00043;ENTREPOT BAZAR;20131128;
024049124;00050;SNIE;20120922;
024049124;00068;BOURBON DISTRIBUTION MAYOTTE;20120922;
024049124;00076;SNIE COMBANI;20131125;
024049124;00084;DOUKA BE;20131125;
024049124;00092;BOURBON DISTRIBUTION MAYOTTE;20131125;
024049124;00100;BOURBON DISTRIBUTION MAYOTTE;20131125;
024049124;00118;SNIE;20131104;
024049124;00126;SNIE;20131125;
024049124;00134;UTV;20131107;
024049124;00142;JUMBO SCORE;20141028;
024049124;00159;BOURBON DISTRIBUTION MAYOTTE;20150320;
024049124;00167;DOUKA BE;20151009;
024049124;00175;DOUKA BE;20151009;
024049124;00183;DOUKA BE;20151106;
024049124;00191;DOUKA BE;20160120;
024049124;00209;DOUKA BE;20160216;
024049124;00217;BOURBON DISTRIBUTION MAYOTTE;20160318;
024049124;00225;BOURBON DISTRIBUTION MAYOTTE;20160318;
024049124;00233;BOURBON DISTRIBUTION MAYOTTE;20160318;
024049124;00241;DOUKA BE;20160701;CE
024049124;00258;DOUKA BE;20160701;CE
```

You can see that as of 2016-07-01, the company with `NIC` "00258"
created new establishments (`CE` for `EVE`nement column).


## Contributing

We’re really happy to accept contributions from the community, that’s the main reason why we open-sourced it! There are many ways to contribute, even if you’re not a technical person.

We’re using the infamous [simplified Github workflow](http://scottchacon.com/2011/08/31/github-flow.html) to accept modifications (even internally), basically you’ll have to:

* create an issue related to the problem you want to fix (good for traceability and cross-reference)
* fork the repository
* create a branch (optionally with the reference to the issue in the name)
* hack hack hack
* commit incrementally with readable and detailed commit messages
* submit a pull-request against the master branch of this repository

We’ll take care of tagging your issue with the appropriated labels and answer within a week (hopefully less!) to the problem you encounter.

If you’re not familiar with open-source workflows or our set of technologies, do not hesitate to ask for help! We can mentor you or propose good first bugs (as labeled in our issues).


### Submitting bugs

You can report issues directly on Github, that would be a really useful contribution given that we lack some user testing on the project. Please document as much as possible the steps to reproduce your problem.


### Adding documentation

We’re doing our best to document each usage of the project but you can improve it or add you own sections.


### Hacking

Commit messages should be formatted using [AngularJS conventions](http://goo.gl/QpbS7) (one-liners are OK for now but body and footer may be required as the project matures).

Comments follow [Google's style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Comments).


## License

We’re using the [MIT license](https://tldrlegal.com/license/mit-license).


## Changelog

See the [dedicated file](CHANGELOG.md).


## TODO

* provide a dump of a Redis database with default columns?
* document the low-level API?
* visualize [diffs](https://github.com/ZoomerAnalytics/jsondiff)?
* use file streaming for CSV output (and iterators for the server - Falcon?)


Readme initiated with [OpenSourceTemplate](https://github.com/davidbgk/open-source-template/).
