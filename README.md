# LogsParser

In the current project the XML Log parser is implemented. The language used is Python. For the scripts correct working, some additional frameworks and libraries might be useful; the detailed information can be found in requirements.txt.
The log parser is used to read all XML-files from a specified folder and generate a test report with statistics for the complete test execution.

The solution has the following features:
* the tool has a command line interface (CLI);
* the input parameter is the root folder containing XML-files in sub-folders;
* the parser itself is a class derived from AbstractLogsParser (from the technical description);
* the tool provides metrics for summary and detailed report;
* test cases are implemented to verify the implementation.

In the solution the following assumptions are made:
* as the solution is based on parsing log files, the log files structure is critical to remain the same as presented in the technical description;
* the root folders structure should remain the same as in the technical description;
* in case at least one of the structures discussed in the first two points is changed, small amendments are required to be made in the code. It can be tricky though;
* different test statuses (TEST_RES_PASS, TEST_RES_FAIL, TEST_RES_SKIP) proposed in the technical description are not used in the current solution. Its usage can be discussed directly;
* summary metrics and detailed report are based on the number and percentage values of the tests passed, failed and skipped. The more complicated metrics can be discussed directly.

The solution consits of 3 files:
* MAIN.PY
* TEST_MAIN.PY

__MAIN.PY__
In the file the log parser class, as well as CLI are implemented.
The AbstractLogParser class contains three methods, used for XML logs handling.
The __init__ method is used as a constructor for attributes creation.
The get_result_by_type method is used to return the number of test results of the type (result_type parameter) required (PASS, FAIL or SKIP). The value calculated is also printed to the console.
The generate_detailed_report method is used for printing the table with all the information parsed from the XML logs contained in the specific folder. The number and the percentage of passed, failed and skipped tests are outputed to the console as well.
The process_logs method is used to make a parsing of the XML logs located in the specific folder (folder parameter). The data from the logs is parsed using the BeautifulSoup library, and are stored in the corresponding lists and pandas dataframe created from them. The final dataframe is exported to the working directory in the .xlsx format.
CLI:
To get the most relevant information about the script, <py main.py -h> command should be run in the command prompt.
The script can be run from the command prompt by using the following commands:
* <py main.py parse> or <py main.py parse -folder=DIR> - where DIR is the folder required; the command is used to parse the XML log files (process_logs method is called, the default root folder is test, i.e. contains all the log files);
* <py main.py report> or <py main.py report -folder=DIR> - where DIR is the folder required; the command is used to parse XML logs filed from the directory and create a report based on the data parsed. 
* <py main.py result> or <py main.py result -folder=DIR -type=TYPE>, - where DIR is the folder required, and TYPE is the report type required (PASS, FAIL or SKIP); the default type of PASS is used; the command calls the parse and then get_result_by_type methods, and returns the number of tests with the result specified.

__TEST_MAIN.PY__
The file contains unit tests script for the MAIN.PY script. The testing script is based on the unittest framework.
The script contains 35 tests, that are used to check the main script behavior. The unit tests are implemented as methods of the TestLogParser class.
The tests cover the initialization method, parsing of the XML log files, different reports correctness. The CLI implementation is not covered with the unit tests; the manual testing to ensure the correct behavior was performed.
