# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## 0.3.1 [2017-11-29]
### Added
- Added more required dependencies in the setup.py file. A fresh installation through pip will also install the required dependencies.

## 0.3 [2017-11-27]
### Added
- Major rewrite of the emission data included in this module. Went away from the JSON file and instead rewrote to use SQLite3 + sqlalchemy. Defined models for each table structure as well as util methods to properly lookup the correct emission for the vehicle choosen.

### Changed
- Changed our "sqlalchemy" to use a "scoped_session" to work in a threaded environment if neccesary.
- Fixed minor bugs here and there.
- Efforts to ensure a Python2 compatibility, while still primarily focus on Python 3.
- Better error handling for issues with the remote webservice (a36c9c42ee33c967a4bd609cb78051f0486913d4)

### Removed 
- dependency for the EmissionJSONReader (will be removed at a later stage)

## 0.2.3

A working module using a compressed JSON structure as its reference (database). The module will retrieve a list of positions (x,y,z) from the NPRA vegkart database and calculate the emission for the choosen vehicle based on that. All emissions are stored in the compressed JSON file.
