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

Check [detailled use cases](#use-cases) for a better idea of what can be achieved
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
pip install -r requirements.txt
```

In both cases, you have to run the script with Python 3+.
Note that you might need to [install pip](https://pip.pypa.io/en/stable/installing/) before.

If you plan to make HTTP requests to retrieve filtered data, we strongly recommend
using [httpie](https://httpie.org/) instead of curl, it should have been
installed through the load of the requirements.txt file.

You will need a running Redis server too. The installation and launch
depends on your OS. For instance for macOS:

```shell
brew install redis
redis-server
```


## Use cases

### Limiting the huge Sirene CSV file


### Working on a given domain only


### Quick and dirty export in CSV or JSON




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

* provide a dump of a Redis database with some default columns?
* load daily updates and provide a way to query that
* or at least visualize it? https://github.com/ZoomerAnalytics/jsondiff
* document default constants
* document use cases
* use file streaming for CSV output (and iterators for the server)


Readme initiated with [OpenSourceTemplate](https://github.com/davidbgk/open-source-template/).
