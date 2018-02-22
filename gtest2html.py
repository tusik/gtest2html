import sys
import os
import shutil
import glob
import math

import xml.etree.ElementTree as ET

from templates.html_templates import *

# Template scheme.
# -> tmpl_main_html[]


def usage():
    print('Usage:')
    print('  python Gtest2Html.py <REPORT_FILE> <OUTPUT_FILE>')
    print('  Args:')
    print('    REPORT_FILE: Gtest xml report.')
    print('    OUTPUT_FILE: Path to the output file, e.g. "index.html"')


def error_gen(actual, rounded):
    divisor = math.sqrt(1.0 if actual < 1.0 else actual)
    return abs(rounded - actual) ** 2 / divisor


def round_to_100(percents):
    if not math.isclose(sum(percents), 100):
        raise ValueError
    n = len(percents)
    rounded = [int(x) for x in percents]
    up_count = 100 - sum(rounded)
    errors = [(error_gen(percents[i], rounded[i] + 1) - error_gen(percents[i], rounded[i]), i)
              for i in range(n)]
    rank = sorted(errors)
    for i in range(up_count):
        rounded[rank[i][1]] += 1
    return rounded


def check_for_unkown_attributes(xml_node, known_attributes, include_empty_attributes=False):
    # Print warning for each unknown attribute inside the xml node.
    for unknown_attribute in list(filter(lambda x: x not in known_attributes, xml_node.attrib)):
        if not xml_node.attrib[unknown_attribute].strip() or include_empty_attributes:
            print('Warning: Unknown attribute {!r} found in node {!s}[{!r}] which is not parsed.'.format(
                unknown_attribute, xml_node.tag, xml_node.attrib))


def generate_progress_bars(abs_total, abs_success, abs_fail, abs_disabled):
    html_progressbars = ''
    if abs_total > 0:
        html_class_list = ['success', 'danger', 'warning']
        abs_value_list = [abs_success, abs_fail, abs_disabled]
        percentage_list = list(
            map(lambda x: 100.0 * x / float(abs_total), abs_value_list))
        rounded_percentage_list = round_to_100(percentage_list)

        for idx in range(len(abs_value_list)):
            abs_value = abs_value_list[idx]
            percentage_rate = rounded_percentage_list[idx]
            html_class = html_class_list[idx]

            if abs_value == 0:
                continue

            html_progressbars += tmpl_progress_bar.format(
                html_class=html_class,
                percentage_rate=percentage_rate,
                absolute_value=abs_value
            )
    else:
        html_progressbars = tmpl_progress_bar.format(
            html_class='success',
            percentage_rate=100,
            absolute_value=0
        )
    return html_progressbars


def get_xml_attribute(convert_func, xml_node, attribute_name, default_value, print_warning=True):
    if not attribute_name in xml_node.attrib and print_warning:
        print('Warning: Attribute {!r} was not found inside xml node {!s}[{!r}]. Set it to its default value {!r}.'.format(
            attribute_name, xml_node.tag, xml_node.attrib, default_value))
        return default_value
    return convert_func(xml_node.attrib[attribute_name])


def generate_total_test_summary(xml_testsuites_node):
    # Parse the testsuites node attributes.
    total_abs_test_count = get_xml_attribute(int, xml_testsuites_node, 'tests', 0)
    total_abs_fail_count = get_xml_attribute(int, xml_testsuites_node, 'failures', 0)
    total_abs_disabled_count = get_xml_attribute(int, xml_testsuites_node, 'disabled', 0)
    total_abs_success_count = total_abs_test_count - total_abs_fail_count - total_abs_disabled_count
    total_execution_time = get_xml_attribute(str, xml_testsuites_node, 'time', 0)
    test_timestamp = get_xml_attribute(str, xml_testsuites_node, 'timestamp', 0)
    test_project_name = get_xml_attribute(str, xml_testsuites_node, 'project', 'undefined')
    testsuite_name = get_xml_attribute(str, xml_testsuites_node, 'name', 'undefined')
    test_author = get_xml_attribute(str, xml_testsuites_node, 'author', 'undefined')

    # Print warning for each unknown attribute inside the node testsuites.
    check_for_unkown_attributes(xml_testsuites_node, ['tests', 'failures',
                                                      'disabled', 'time', 'timestamp', 'author', 'name', 'project'])

    # Generate HTML for the navigation bar.
    test_navbar = tmpl_test_navbar.format(
        project_name=test_project_name
    )

    # Generate HTML for the prograss bar for the test summary.
    total_test_result_progressbars = generate_progress_bars(
        abs_total=total_abs_test_count,
        abs_success=total_abs_success_count,
        abs_fail=total_abs_fail_count,
        abs_disabled=total_abs_disabled_count
    )

    # Generate HTML for the test summary.
    total_test_result = tmpl_total_test_result.format(
        report_file_path=report_file,
        testsuite_name=testsuite_name,
        total_abs_test_count=total_abs_test_count,
        total_abs_success_count=total_abs_success_count,
        total_abs_fail_count=total_abs_fail_count,
        total_abs_disabled_count=total_abs_disabled_count,
        html_progress_bars=total_test_result_progressbars,
        total_execution_time=total_execution_time,
        test_timestamp=test_timestamp,
        test_author=test_author
    )
    return test_navbar, total_test_result_progressbars, total_test_result


def generate_single_testcase_rows(xml_testsuite_node):
    html_single_testcase_rows = ''

    xml_testcase_nodes = xml_testsuite_node.findall('./testcase')
    if len(xml_testcase_nodes) == 0:
        print("Warning: No nodes {!r} found in testsuite element with name {!r}.".format(
            'testcase', test_name))

    for idx, xml_testcase_node in enumerate(xml_testcase_nodes):
        test_number = idx + 1
        test_name = get_xml_attribute(str, xml_testcase_node, 'name', '-undefined-')
        test_execution_time = get_xml_attribute(str, xml_testcase_node, 'time', '-undefined-')
        test_status = get_xml_attribute(str, xml_testcase_node, 'status', '-undefined-')
        test_classname = get_xml_attribute(str, xml_testcase_node, 'classname', '-undefined-')
        test_tags = get_xml_attribute(str, xml_testcase_node, 'tags', '')

        test_icon_name = ''
        test_html_class = 'primary'
        html_error_message_list = ''

        # Print warning for each unknown attribute inside the node testcase.
        check_for_unkown_attributes(
            xml_testcase_node, ['name', 'time', 'status', 'classname', 'tags'])

        # Select icon name and html class considering the number of failure-children and the test status.
        xml_failure_nodes = xml_testcase_node.findall('./failure')

        if len(xml_failure_nodes) == 0 and test_status == 'run':
            test_icon_name = 'check'
            test_html_class = 'success'
        elif test_status == 'notrun':
            test_icon_name = 'warning'
            test_html_class = 'warning'
        else:
            test_icon_name = 'x'
            test_html_class = 'danger'

        # If failures occurs, generate the listing with error messages.
        if len(xml_failure_nodes) > 0:
            html_error_message_items = ''
            for xml_failure_node in xml_failure_nodes:
                error_message = get_xml_attribute(
                    str, xml_failure_node, 'message', '-undefined-')
                error_type = get_xml_attribute(str, xml_failure_node, 'type', '-undefined-')
                error_type = '' if not error_type else ' (type = {})'.format(error_type)

                # Print warning for each unknown attribute inside the node failure.
                check_for_unkown_attributes(xml_failure_node, ['message', 'type'])

                html_error_message_items += tmpl_error_message_item.format(
                    error_message=error_message,
                    error_type=error_type
                )

            html_error_message_list = tmpl_error_message_listing.format(
                html_error_message_items=html_error_message_items
            )

        # Create the HTML code for this single testcase.
        html_single_testcase_rows += tmpl_single_test_row.format(
            test_number=test_number,
            test_classname=test_classname,
            test_name=test_name,
            test_tags=test_tags,
            html_error_message_list=html_error_message_list,
            test_execution_time=test_execution_time,
            test_icon_name=test_icon_name,
            test_html_class=test_html_class
        )
    return html_single_testcase_rows


def generate_single_test_result_listings(xml_testsuites_node):
    html_single_test_result_listing = ''
    collected_testsuite_ids = []

    # Generate HTML for the single test result listings.
    xml_testsuite_nodes = xml_testsuites_node.findall('./testsuite')
    if len(xml_testsuite_nodes) == 0:
        print('Warning: No nodes {!r} found in {!r}. Nothing is listed inisde the single test_result listing.'.format(
            'testsuite', report_file))

    id_counter = 0
    for xml_testsuite_node in xml_testsuite_nodes:
        # Parse XML.
        testsuite_name = get_xml_attribute(str, xml_testsuite_node, 'name', '-undefined-')
        testsuite_abs_test_count = get_xml_attribute(int, xml_testsuite_node, 'tests', 0)
        testsuite_abs_fails_count = get_xml_attribute(int, xml_testsuite_node, 'failures', 0)
        testsuite_abs_disabled_count = get_xml_attribute(int, xml_testsuite_node, 'disabled', 0)
        testsuite_abs_success_count = testsuite_abs_test_count - \
            testsuite_abs_fails_count - testsuite_abs_disabled_count
        testsuite_execution_time = get_xml_attribute(
            str, xml_testsuite_node, 'time', '-undefined-')
        testsuite_tags = get_xml_attribute(str, xml_testsuite_node, 'tags', '')

        # Print warning for each unknown attribute inside the node testsuite.
        check_for_unkown_attributes(xml_testsuite_node, ['name', 'tests',
                                                         'failures',  'disabled', 'time', 'tags'])

        # Generate HTML for single test cases.
        html_single_testcase_rows = generate_single_testcase_rows(xml_testsuite_node)

        html_testsuites_progress_bars = generate_progress_bars(
            abs_total=testsuite_abs_test_count,
            abs_success=testsuite_abs_success_count,
            abs_fail=testsuite_abs_fails_count,
            abs_disabled=testsuite_abs_disabled_count
        )

        html_testsuite = tmpl_single_test_result_listing.format(
            html_progress_bars=html_testsuites_progress_bars,
            testsuite_name=testsuite_name,
            testsuite_tags=testsuite_tags,
            testsuite_html_id=id_counter,
            testsuite_abs_test_count=testsuite_abs_test_count,
            testsuite_abs_fails_count=testsuite_abs_fails_count,
            testsuite_abs_disabled_count=testsuite_abs_disabled_count,
            testsuite_execution_time=testsuite_execution_time,
            html_single_test_rows=html_single_testcase_rows
        )

        collected_testsuite_ids.append((testsuite_name, id_counter))
        id_counter += 1

        html_single_test_result_listing += html_testsuite

    return html_single_test_result_listing, collected_testsuite_ids


def generate_test_sidebar(collected_testsuite_ids):
    html_single_testsuite_links = ''
    for name_id_pair in collected_testsuite_ids:
        html_single_testsuite_links += tmpl_single_testsuite_link.format(
            testsuite_name=name_id_pair[0],
            testsuite_html_id=name_id_pair[1]
        )

    html_test_sidebar = tmpl_test_sidebar.format(
        single_testsuite_links=html_single_testsuite_links
    )

    return html_test_sidebar


def generate_html(report_file, destination_file):
    # Parse XML.
    xml_tree = ET.parse(report_file)
    xml_root = xml_tree.getroot()

    # Check if the root element 'testsuites' exists.
    xml_testsuites_nodes = xml_root.findall('.')
    if len(xml_testsuites_nodes) == 0:
        print('Error: The xml file {!r} has no root node.'.format(report_file))
        exit(-1)
    xml_testsuites_node = xml_testsuites_nodes[0]
    if xml_testsuites_node.tag != 'testsuites':
        print('Error: The xml file {!r} has an invalid root node tag (found: {!r}, expected: {!r})'.format(
            report_file, xml_testsuites_node.tag, 'testsuites'))
        exit(-1)

    html_single_test_result_listing, collected_testsuite_ids = generate_single_test_result_listings(
        xml_testsuites_node)

    test_navbar, total_test_result_progressbars, total_test_result = generate_total_test_summary(
        xml_testsuites_node)
    test_sidebar = generate_test_sidebar(collected_testsuite_ids)

    html_code = tmpl_main_html.format(
        test_navbar=test_navbar,
        test_sidebar=test_sidebar,
        total_test_result=total_test_result,
        single_test_result_listing=html_single_test_result_listing
    )

    with open(destination_file, 'w') as fout:
        fout.write(html_code)

    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        exit(0)

    # Get the source and destination directories.
    source_directory = os.path.dirname(os.path.realpath(__file__))
    destination_directory = os.path.dirname(sys.argv[2])
    report_file = os.path.realpath(sys.argv[1])
    destination_file = os.path.realpath(sys.argv[2])

    if not os.path.exists(report_file):
        print('ERROR: The report file {} does not exists.'.format(report_file))
        usage()
        exit(1)

    # Create the destination directory if not exists.
    if not os.path.isdir(destination_directory):
        os.makedirs(destination_directory)

    # Copy files from html_resources.
    resource_files = glob.glob(os.sep.join([source_directory, 'html_resources/*']))
    for rs in resource_files:
        print(rs)
        if os.path.isfile(rs):
            shutil.copy(rs, destination_directory)
        else:
            dirname = os.path.split(rs)[-1]
            target = os.sep.join([destination_directory, dirname])

            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.copytree(rs, os.sep.join([destination_directory, dirname]))

    # Generate html.
    print('Start generation:')
    print('  input  : {}'.format(report_file))
    print('  output : {}'.format(destination_file))
    if generate_html(report_file, destination_file):
        print('Html was generated successful.')
