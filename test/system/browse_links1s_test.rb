# browse_links1s_test.rb

# This script should help me run a system test.

# Demo shell command:
# bin/rails test:system

require "application_system_test_case"

class BrowseLinks1sTest < ApplicationSystemTestCase
  test "visiting the index" do
    visit pages_about_url
  
    assert_selector "h1", text: "Regression For Us"
  end
end
