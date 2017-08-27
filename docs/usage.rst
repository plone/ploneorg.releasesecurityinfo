Usage
=====

The following are the basic content types:

* Release
* ReleaseSeries
* ReleaseFolder
* Hotfix
* HotfixFolder
* Vulnerability

The Release team/manager can update the releasefolder with launchpad data by ruuning /update from releasefolder view.
It can also be done via command line script as following:

.. code-block:: console

   bin/instance -O <portal_id> update_releasefolder <Path to releasefolder relative to Zope root>

The update would add releaseseries inside releasefolder and releases within corresponding releaseseries.

The release team/manager can add a hotfixfolder to releasefolder. 
Multiple hotfixes can be added to a hotfixfolder and
multiple vulnerabilities can be added to their corresponding hotfix.

When /hotfix_json is run on a hotfixfolder, a list of releases along with their corresponding hotfixes are displayed in json view.