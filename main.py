import os.path
from bs4 import BeautifulSoup # XML log files parsing
import pandas as pd
import argparse # CLI

class AbstractLogsParser(object):
    # Different test statuses
    TEST_RES_PASS = 0
    TEST_RES_FAIL = 1
    TEST_RES_SKIP = 2

    def __init__(self, logs_extension):
        """
        Base class constructor.
        @param logs_extension Extension of log files to parse.
        """
        self._logs_ext = '.'+logs_extension

        # lists to store parsed data
        self.files = []
        self.suites = []
        self.envs = []
        self.ids = []
        self.results = []
        self.reasons = []
        self.debugs = []

        # dataFrame for neat reporting
        self.data = pd.DataFrame()

        # dictionary for detailed report 
        self.report_dict = {}

    def get_result_by_type(self, result_type):
        """
        Returns number of passed, failed or skipped tests.
        @param result_type Type of results to return.
        """
        
        print('-'*107)
        #counting results for type required - PASS, FAIL or SKIP
        result = self.results.count(result_type)
        print('Tests with {} result:'.format(result_type), result)
        return result


    def generate_detailed_report(self):
        """
        Generates detailed report on each test suite.
        """
        print('-'*107)
        print('Generating general report...')

        # printing the dataframe built on parsed lists
        print(self.data)
        print('-'*107)
        print('Generating detailed reports for each test suite...')

        # for each test suite - results from dataframe transformed into dictionary
        for suite in set(self.suites):
            self.report_dict = self.data[self.data['test_suite'] == suite]['result'].value_counts().to_dict()
            tests_num = float(self.data[self.data['test_suite'] == suite].shape[0])
            print(suite, ':')

            # printing results from the dictionary + calculated percentage
            for key in self.report_dict:
                val = self.report_dict[key]
                print(key, ':', val , '('+str(val/tests_num*100)+'%)')
     

    def process_logs(self, folder):
        """
        Parses all log files with target extension in the specified folder.
        @param folder Folder to look up for log files.
        """
        
        print('Processing logs...')

        # scanning the folder required 
        for dirpath, dirnames, filenames in os.walk(folder):

            # opening each file using BeautifulSoup library
            for filename in filenames:
                fd = open(os.path.join(dirpath, filename), 'r')
                xml_file = fd.read()
                soup = BeautifulSoup(xml_file, 'lxml')

                # parsing - results are stored in lists
                for tag in soup.findAll('test_results'):
                    suite = tag['test_suite'] 
                    env = tag.find('environment').text
                    for tag in soup.findAll('tc_result'):
                        self.files.append(filename) # filename
                        self.suites.append(suite)  # test_suite
                        self.envs.append(env) # environment
                        self.ids.append(tag['id']) # test_id
                        self.results.append(tag['result']) #result - PASS, SKIP, FAIL

                        # reason - None, Unstable, etc
                        try:
                            self.reasons.append(tag.find('reason').text)
                        except AttributeError:
                            self.reasons.append(None)

                        # debug - None, etc
                        try:
                            self.debugs.append(tag.find('debug').text)
                        except AttributeError:
                            self.debugs.append(None)
        
        # creating pandas dataframe by combining lists
        self.data = pd.DataFrame({'test_id':self.ids, 'result':self.results, 'reason':self.reasons, 'debug':self.debugs,
                            'test_suite':self.suites, 'environment':self.envs, 'file':self.files})


        # importing the dataframe to local folder
        report_name = 'report.xlsx'
        self.data.to_excel(report_name)
        print('The \'{}\' document is imported to the current folder.'.format(report_name))


if __name__ == '__main__':

    # Command Line Interface

    # creating arguments
    parser = argparse.ArgumentParser(description = 'Log Parser')
    parser.add_argument('cmd', help = 'insert the command -> parse, report or result', type = str)
    parser.add_argument('-folder', default = 'test', help = 'insert folder name (for parse or report cmds)', type = str)
    parser.add_argument('-type', default = 'PASS', help = 'insert report type -> PASS, SKIP or FAIL', type = str)
    parser.add_argument('-ext', '-logs_extension', default = 'xml', help = 'insert the logs extension', type = str)
    args = parser.parse_args()

    # handling arguments
    LogParser = AbstractLogsParser(args.ext)
    if args.cmd == 'parse':
        LogParser.process_logs(args.folder)
    elif args.cmd == 'report':
        LogParser.process_logs(args.folder)
        LogParser.generate_detailed_report()
    elif args.cmd == 'result':
        LogParser.process_logs(args.folder)
        LogParser.get_result_by_type(args.type)
    else:
        print('Please read -help carefully!')
