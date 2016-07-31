# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s ploneorg.releasesecurityinfo -t test_plonerelease.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src ploneorg.releasesecurityinfo.testing.PLONEORG_RELEASESECURITYINFO_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_plonerelease.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a PloneRelease
  Given a logged-in site administrator
    and an add plonerelease form
   When I type 'My PloneRelease' into the title field
    and I submit the form
   Then a plonerelease with the title 'My PloneRelease' has been created

Scenario: As a site administrator I can view a PloneRelease
  Given a logged-in site administrator
    and a plonerelease 'My PloneRelease'
   When I go to the plonerelease view
   Then I can see the plonerelease title 'My PloneRelease'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add plonerelease form
  Go To  ${PLONE_URL}/++add++PloneRelease

a plonerelease 'My PloneRelease'
  Create content  type=PloneRelease  id=my-plonerelease  title=My PloneRelease


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the plonerelease view
  Go To  ${PLONE_URL}/my-plonerelease
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a plonerelease with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the plonerelease title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
