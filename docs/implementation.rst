Implementation
===============

ploneorg.releasesecurityinfo consists of 6 Content Types:

* ReleaseFolder (reflects Launchpad Project)
* ReleaseSeries (reflects Launchpad Series)
* Release (reflects Launchpad Milestone + Release)
* HotfixFolder
* Hotfix
* Vulnerability

note: * indicates required fields

ReleaseFolder
~~~~~~~~~~~~~~~
maps to Launchpad Project, container for ReleaseSeries

* project_name


ReleaseSeries
~~~~~~~~~~~~~~~
maps to Series in Launchpad, container for Release

* title* 
* display_name*
* description 
* status(EXPERIMENTAL, DEVELOPMENT, FROZEN, CURRENT, SUPPORTED, OBSOLETE, FUTURE) 
* is_development_focus
* is_security_supported
* is_active_maintained
* branch 
* url_pattern


Release
~~~~~~~~~~
maps Milestone + Release which is a 1:1 Connection

* title*
* codename
* target date
* release date*
* tags
* summary
* release notes
* change log


HotfixFolder
~~~~~~~~~~~~~~
container for hotfixes and added to a ReleaseFolder

* title*


Hotfix
~~~~~~~~
container for vulnerability

* description
* release_date*
* text
* preannounce_text


vulnerability
~~~~~~~~~~~~~~~

* vulnerability_type
* details
* current_status
* date_reported
* date_patched
* reported_by
* fixed_by
* coordinated_by
* cve_id
* affected_versions
