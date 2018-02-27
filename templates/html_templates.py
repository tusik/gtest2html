# Template parameters:
#   test_navbar                 : The navigation bar.
#   tmpl_test_sidebar           : The sidebar.
#   total_test_result           : HTML for total test results.
#   single_test_result_listing  : HTML for single test result listing.
tmpl_main_html = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <!-- Icons -->
    <link href="open-iconic/font/css/open-iconic-bootstrap.css" rel="stylesheet">
    <!-- Stacktable CSS ->
    <link href="stacktable/css/stacktable.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="css/gtest-report.css" rel="stylesheet">
    <title>Googletest HTML-Report</title>
  </head>
  <body>

    {test_navbar}

    <div class="container-fluid">

      <div class="row">

        <nav class="col-md-4 col-md-mw-230 col-xl-mw-300 bg-light sidebar">
          {test_sidebar}
        </nav>

        <main role="main" class="col col-md-8 col-lg-8 mx-auto pt-3">
          {total_test_result}

          <h4 id="single_test_results">Single Test Results</h4>
          {single_test_result_listing}
        </main>

      </div>
    </div>
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <!-- Stacktable -->
    <script src="stacktable/js/stacktable.js"></script>
    <!-- Custom javascript -->
    <script src="js/gtest-report.js"></script>
  </body>
</html>
'''

# Template parameters:
#   project_name                : Name of the project.
tmpl_test_navbar = '''
<nav class="navbar navbar-dark sticky-top bg-dark">
  <span class="navbar-brand">{project_name}</a>
</nav>
'''

# Template parameters:
#   single_testsuite_links           : HTML code with links to single testsuites.
tmpl_test_sidebar = '''
<h3 class="md-sidebar-header">Content</h3>
<div class="sidebar-sticky">
  <ul class="nav flex-column">
    <li class="nav-item">
      <a class="nav-link" href="#total-test-summary">
        <span class="oi oi-graph"></span>Test Summary
      </a>
    </li>
    <hr/>
    <li>
      <a class="nav-link" href="#single_test_results">
        <span class="oi oi-list"></span>Single Test Results
      </a>
      <ul class="nav flex-column" id="testcase-sidebar-list">
          {single_testsuite_links}
      </ul>
    </li>
    <hr/>
    <li class="nav-item">
      <a class="nav-link">
        <span class="oi oi-tags"></span>Tags
      </a>
      <ul class="nav flex-column">
        <li class="tags-container"></li>
      </ul>
    </li>
  </ul>
</div>
'''

# Template parameters:
#   testsuite_html_id       : html id
#   testsuite_name          : name of the testsuite
tmpl_single_testsuite_link = '''
<small>
    <a class="nav-link" href="#{testsuite_html_id}">
      <span class="oi oi-magnifying-glass"></span>{testsuite_name}
    </a>
</small>
'''

# Template parameters:
#   html_class      : HTML class, one of ['success', 'danger', 'warning']
#   percentage_rate : The percentage rate.
#   absolute_value  : The absolute value.
tmpl_progress_bar = '''
<div class="progress-bar bg-{html_class}" role="progressbar" style="width: {percentage_rate}%" aria-valuenow="{percentage_rate}" aria-valuemin="0" aria-valuemax="100">{percentage_rate}% ({absolute_value})</div>
'''

# Template paramters:
#   report_file_path           : Path to the report file.
#   testsuite_name             : Name of the testsuite
#   total_abs_test_count       : Total number of tests (absolute).
#   total_abs_success_count    : Total number of succeeded tests (absolute).
#   total_abs_fail_count       : Total number of failed tests (absolute).
#   total_abs_disabled_count   : Total number of disabled tests (absolute).
#   html_progress_bars         : HTML code with progress bars to show.
#   total_execution_time       : The execution time of all test suites.
#   test_timestamp             : Timestamp of the test.
#   test_author                : The author of the test.
tmpl_total_test_result = '''
<!-- Total Test Result Begin -->
<div style="margin-bottom:50px;" class="card" id="total-test-summary">
  <h4 class="card-header">Test Summary of {testsuite_name}</h4>
  <div class="card-body">
    <div class="row">
      <div class="col-12">
        <div class="progress" style="margin-bottom: 20px; height: 20px;">
          {html_progress_bars}
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-12 col-xl-4">
        <p class="font-weight-bold">Report file:</p>
        <p>{report_file_path}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Tests:</p>
        <p class="text-primary">{total_abs_test_count}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Fails:</p>
        <p class="text-danger">{total_abs_fail_count}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Disabled:</p>
        <p class="text-warning">{total_abs_disabled_count}</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Execution time:</p>
        <p>{total_execution_time} sec</p>
      </div>
      <div class="col-md-auto">
        <p class="font-weight-bold">Timestamp:</p>
        <p>{test_timestamp}</p>
      </div>
    </div>
    <div class="row">
        <div class="col-12">
            <small class="text-secondary">Test author: {test_author}</small>
        </div>
    </div>
  </div>
</div>
<!-- Total Test Result End -->
'''

# Template paramters:
#   html_progress_bars             : HTML code with progress bars to show.
#   testsuite_name                 : Name of the testsuite.
#   testsuite_tags                 : Tags for this testsuite.
#   testsuite_html_id              : ID to create site links.
#   testsuite_abs_test_count       : Count of all tests of this testsuite (absolute).
#   testsuite_abs_fails_count      : Count of all fails of this testsuite (absolute).
#   testsuite_abs_disabled_count   : Count of all disabled tests of this testsuite (absolute).
#   testsuite_execution_time       : Execution time of the testsuite.
#   html_single_test_rows          : The html code with table rows for each test.
tmpl_single_test_result_listing = '''
<!-- Single Test Result Listing Begin -->
<div id="{testsuite_html_id}" class="card single-testsuite-container" style="margin-top:20px; margin-bottom: 60px;" data-tags="{testsuite_tags}">
  <h5 class="card-header">Testsuite: {testsuite_name}</h5>
  <div class="card-body">
    <div class="single-test-summary">
      <h5 class="font-weight-bold">Summary:</h5>
      <div class="row">
        <div class="col-12">
          <div class="progress" style="margin-bottom: 20px; height: 20px;">
            {html_progress_bars}
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-auto">
          <p class="font-weight-bold">Tests:</p>
          <p class="text-primary">{testsuite_abs_test_count}</p>
        </div>
        <div class="col-sm-auto">
          <p class="font-weight-bold">Fails:</p>
          <p class="text-danger">{testsuite_abs_fails_count}</p>
        </div>
        <div class="col-sm-auto">
          <p class="font-weight-bold">Disabled:</p>
          <p class="text-warning">{testsuite_abs_disabled_count}</p>
        </div>
        <div class="col-sm-auto">
          <p class="font-weight-bold">Execution time:</p>
          <p>{testsuite_execution_time} sec</p>
        </div>
      </div>
      <hr/>
    </div>
    <h5 class="font-weight-bold">Testcases:</h5>
    <div class="container">
      <div class="table-responsive">
        <table class="testcase-table table table-bordered">
          <thead class="testcase-header">
            <tr class="table-active text-center testcase-header-row">
              <th scope="col" class="testcase-header-id">#</th>
              <th scope="col" class="testcase-header-name">Name</th>
              <th scope="col" class="testcase-header-time">Time (sec)</th>
              <th scope="col" class="textcase-header-status">Status</th>
            </tr>
          </thead>
          <tbody>
            {html_single_test_rows}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<!-- Single Test Result Listing End -->
'''

# Template paramters:
#   test_number                : Number of the test.
#   test_classname             : The classname of the test.
#   test_name                  : Name of the test.
#   test_tags                  : Tags for this testcase.
#   test_execution_time        : Execution time of the test.
#   test_html_class            : The HTML class to colorize the row ['success', 'danger', 'warning']
#   test_icon_name             : Name of the icon to use ['check', 'x', 'warning']
#   html_error_message_list    : HTML code with error message list.
tmpl_single_test_row = '''
<!-- Single Test Row Begin -->
<tr class="table-{test_html_class} testcase-row" data-tags="{test_tags}">
  <th class="text-center testcase-id" scope="row">{test_number}</th>
  <td class="testcase-name">
    {test_classname}::{test_name}<span class="testcase-badges"></span><br>
    {html_error_message_list}
  </td>
  <td class="text-right testcase-time">{test_execution_time}</td>
  <td class="text-center testcase-icon"><span class="oi oi-{test_icon_name}"/></td>
</tr>
<!-- Single Test Row End -->
'''

# Template parameters:
#   html_error_message_items : HTML code with list items
tmpl_error_message_listing = '''
<!-- Error Message Listing Begin -->
<small>
  <ul style="margin-top: 10px;">
    {html_error_message_items}
  </ul>
</small>
<!-- Error Message Listing End -->
'''

# Template parameters:
#   error_message : The error message
#   error_type    : Error type. Leave empty if type is empty.
tmpl_error_message_item = '''
<li>{error_message} {error_type}</li>
'''
