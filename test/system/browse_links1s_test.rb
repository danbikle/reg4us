# browse_links1s_test.rb

# This script should help me run a system test.

# Demo shell command:
# bin/rails test:system

require "application_system_test_case"

class BrowseLinks1sTest < ApplicationSystemTestCase
  test "browse links" do
    visit '/pages/about'
    sleep 1
    visit '/pages/backtests'
    sleep 1
    visit '/pages/blog'
    sleep 1
    visit '/pages/compare'
    sleep 1
    visit '/pages/contact'
    sleep 1
    visit '/pages/whatif'
    sleep 1
    visit '/'  
    sleep 1
    assert_selector "h1", text: "Regression For Us"
  end
end
