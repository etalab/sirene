# Changelog

## 2.3.1 — 2017-01-04 — 👻 Deal with manual inserts/removals in flux2stock

* Some people explictely want to be inserted/removed from the SIRENE file.


## 2.3.0 — 2016-12-29 — 👪 Flux2stock script

* This script converts a stock + flux into a new updated stock.


## 2.2.0 — 2016-11-11 — 🛍 Display diffs

* Serve the differences between two states for a given SIRET


## 2.1.0 — 2016-11-11 — ♨️ Load all

* Ability to load every columns of the source files


## 2.0.0 — 2016-11-05 — 🗄 History

* Ability to load incremental updates
* **Breaking-change**: use SIREN + NIC (SIRET) as key for storing data
* **Breaking-change**: the undocumented low-level API has been refactored
* **Breaking-change**: returned JSON has now one more level with DATEMAJ


## 1.0.1 — 2016-11-01 — 🐞 Fix parameters parsing

* Better handling of list parameters


## 1.0.0 — 2016-11-01 — ✨ Initialization

* Ability to load a given number of lines/columns into Redis
* Ability to serve and filter that data in CSV or JSON
