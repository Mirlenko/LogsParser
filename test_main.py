import unittest
import os
from main import AbstractLogsParser

class TestLogParser(unittest.TestCase):
    
    # test initialization
    def setUp(self):
        self.parser = AbstractLogsParser('xml')

    ###################################################################
    # testing the AbstractLogsParser class initialization

    def test_init_extension_equals_xml(self):
        self.assertEqual(self.parser._logs_ext, '.xml')
        
    def test_init_lists_created(self):
        self.assertIsInstance(self.parser.suites, list)
        self.assertIsInstance(self.parser.envs, list)

    ###################################################################
    # testing the files scope

    def test_parse_gap_sec_001_xml_in_default_folder(self):
        self.parser.process_logs('test')
        self.assertIn('gap_sec_001.xml', self.parser.files)

    def test_parse_gap_conn_001_xml_in_test_gap_conn_folder(self):
        self.parser.process_logs('test/gap/conn')
        self.assertIn('gap_conn_001.xml', self.parser.files)

    def test_parse_gap_conn_001_xml_not_in_test_gap_rssi_folder(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertNotIn('gap_conn_001.xml', self.parser.files)

    ###################################################################
    # testing content of the logs parsed

    # gap_conn_001.xml
    def test_parse_gap_conn_001_xml_conn_bv_001(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.suites[0], 'GAP_CONN_001')
        self.assertEqual(self.parser.envs[0], 'LOCAL')
        self.assertEqual(self.parser.ids[0], 'conn_bv_001')
        self.assertEqual(self.parser.results[0], 'PASS')
        self.assertIsNone(self.parser.reasons[0])
        self.assertEqual(self.parser.debugs[0], 'Run 2 sequences')

    def test_parse_gap_conn_001_xml_conn_bv_002(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.ids[1], 'conn_bv_002')
        self.assertEqual(self.parser.results[1], 'FAIL')
        self.assertIsNone(self.parser.reasons[1])
        self.assertIsNone(self.parser.debugs[1])
        self.assertEqual(self.parser.suites[1], 'GAP_CONN_001')
        self.assertEqual(self.parser.envs[1], 'LOCAL')

    def test_parse_gap_conn_001_xml_conn_bv_003(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.ids[2], 'conn_bv_002')
        self.assertEqual(self.parser.results[2], 'PASS')
        self.assertIsNone(self.parser.reasons[2])
        self.assertIsNone(self.parser.debugs[2])
        self.assertEqual(self.parser.suites[2], 'GAP_CONN_001')
        self.assertEqual(self.parser.envs[2], 'LOCAL')

    def test_parse_gap_conn_001_xml_conn_bv_004(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.ids[3], 'conn_bv_004')
        self.assertEqual(self.parser.results[3], 'SKIP')
        self.assertEqual(self.parser.reasons[3], 'No pass criteria')
        self.assertIsNone(self.parser.debugs[3])
        self.assertEqual(self.parser.suites[3], 'GAP_CONN_001')
        self.assertEqual(self.parser.envs[3], 'LOCAL')

    # gap_sec_001.xml
    def test_parse_gap_sec_001_xml_sec_auth_001(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.assertEqual(self.parser.suites[0], 'GAP_SEC_001')
        self.assertEqual(self.parser.envs[0], 'SERVER002')
        self.assertEqual(self.parser.ids[0], 'sec_auth_001')
        self.assertEqual(self.parser.results[0], 'PASS')
        self.assertIsNone(self.parser.reasons[0])
        self.assertIsNone(self.parser.debugs[0])

    def test_parse_gap_sec_001_xml_sec_auth_002(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.assertEqual(self.parser.ids[1], 'sec_auth_002')
        self.assertEqual(self.parser.results[1], 'SKIP')
        self.assertEqual(self.parser.reasons[1], 'Unstable')
        self.assertIsNone(self.parser.debugs[1])
        self.assertEqual(self.parser.suites[1], 'GAP_SEC_001')
        self.assertEqual(self.parser.envs[1], 'SERVER002')

    def test_parse_gap_sec_001_xml_sec_auth_003(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.assertEqual(self.parser.ids[2], 'sec_auth_003')
        self.assertEqual(self.parser.results[2], 'PASS')
        self.assertIsNone(self.parser.reasons[2])
        self.assertEqual(self.parser.debugs[2], 'Auth on 2nd attempt')
        self.assertEqual(self.parser.suites[2], 'GAP_SEC_001')
        self.assertEqual(self.parser.envs[2], 'SERVER002')

    def test_parse_gap_sec_001_xml_sec_auth_004(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.assertEqual(self.parser.ids[3], 'sec_auth_004')
        self.assertEqual(self.parser.results[3], 'PASS')
        self.assertIsNone(self.parser.reasons[3])
        self.assertIsNone(self.parser.debugs[3])
        self.assertEqual(self.parser.suites[3], 'GAP_SEC_001')
        self.assertEqual(self.parser.envs[3], 'SERVER002')

    # gap_rssi_001.xml
    def test_parse_gap_rssi_001_xml_gap_rssi_001(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertEqual(self.parser.suites[0], 'GAP_RSSI_001')
        self.assertEqual(self.parser.envs[0], 'LOCAL')
        self.assertEqual(self.parser.ids[0], 'gap_rssi_001')
        self.assertEqual(self.parser.results[0], 'PASS')
        self.assertIsNone(self.parser.reasons[0])
        self.assertIsNone(self.parser.debugs[0])

    def test_parse_gap_rssi_001_xml_gap_rssi_002(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertEqual(self.parser.ids[1], 'gap_rssi_002')
        self.assertEqual(self.parser.results[1], 'FAIL')
        self.assertIsNone(self.parser.reasons[1])
        self.assertEqual(self.parser.debugs[1], 'RX 10 dBm')
        self.assertEqual(self.parser.suites[1], 'GAP_RSSI_001')
        self.assertEqual(self.parser.envs[1], 'LOCAL')

    def test_parse_gap_rssi_001_xml_gap_rssi_003(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertEqual(self.parser.ids[2], 'gap_rssi_003')
        self.assertEqual(self.parser.results[2], 'PASS')
        self.assertIsNone(self.parser.reasons[2])
        self.assertIsNone(self.parser.debugs[2])
        self.assertEqual(self.parser.suites[2], 'GAP_RSSI_001')
        self.assertEqual(self.parser.envs[2], 'LOCAL')

    def test_parse_gap_rssi_001_xml_gap_rssi_004(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertEqual(self.parser.ids[3], 'gap_rssi_004')
        self.assertEqual(self.parser.results[3], 'SKIP')
        self.assertEqual(self.parser.reasons[3], 'Not implemented')
        self.assertIsNone(self.parser.debugs[3])
        self.assertEqual(self.parser.suites[3], 'GAP_RSSI_001')
        self.assertEqual(self.parser.envs[3], 'LOCAL')

    def test_parse_gap_rssi_001_xml_gap_rssi_005(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertEqual(self.parser.ids[4], 'gap_rssi_005')
        self.assertEqual(self.parser.results[4], 'SKIP')
        self.assertEqual(self.parser.reasons[4], 'Not supported')
        self.assertIsNone(self.parser.debugs[4])
        self.assertEqual(self.parser.suites[4], 'GAP_RSSI_001')
        self.assertEqual(self.parser.envs[4], 'LOCAL')

    ###################################################################
    # testing report creation in the working directory

    def test_report_xlsx_is_in_work_dir(self):
        self.parser.process_logs('test')
        self.assertTrue(os.path.exists('report.xlsx'))

    ###################################################################
    # testing the dataframe correctness

    # gap_conn_001.xml
    def test_parse_df_gap_conn_001_xml_conn_bv_001(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.data['test_suite'][0], 'GAP_CONN_001')
        self.assertEqual(self.parser.data['environment'][0], 'LOCAL')
        self.assertEqual(self.parser.data['test_id'][0], 'conn_bv_001')
        self.assertEqual(self.parser.data['result'][0], 'PASS')
        self.assertIsNone(self.parser.data['reason'][0])
        self.assertEqual(self.parser.data['debug'][0], 'Run 2 sequences')

    def test_parse_df_gap_conn_001_xml_conn_bv_002(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.data['test_suite'][1], 'GAP_CONN_001')
        self.assertEqual(self.parser.data['environment'][1], 'LOCAL')
        self.assertEqual(self.parser.data['test_id'][1], 'conn_bv_002')
        self.assertEqual(self.parser.data['result'][1], 'FAIL')
        self.assertIsNone(self.parser.data['reason'][1])
        self.assertIsNone(self.parser.data['debug'][1])

    def test_parse_df_gap_conn_001_xml_conn_bv_003(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.data['test_suite'][2], 'GAP_CONN_001')
        self.assertEqual(self.parser.data['environment'][2], 'LOCAL')
        self.assertEqual(self.parser.data['test_id'][2], 'conn_bv_002')
        self.assertEqual(self.parser.data['result'][2], 'PASS')
        self.assertIsNone(self.parser.data['reason'][2])
        self.assertIsNone(self.parser.data['debug'][2])

    def test_parse_df_gap_conn_001_xml_conn_bv_004(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.data['test_suite'][3], 'GAP_CONN_001')
        self.assertEqual(self.parser.data['environment'][3], 'LOCAL')
        self.assertEqual(self.parser.data['test_id'][3], 'conn_bv_004')
        self.assertEqual(self.parser.data['result'][3], 'SKIP')
        self.assertEqual(self.parser.data['reason'][3], 'No pass criteria')
        self.assertIsNone(self.parser.data['debug'][3])

    # judging by the previous tests, parsing and transform to dataframe went without errors
    # for this reason, the gap_sec_001.xml and gap_rssi_001.xml files are tested only selectively

    # gap_sec_001.xml
    def test_parse_df_gap_sec_001_xml_sec_auth_001(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.assertEqual(self.parser.data['test_suite'][0], 'GAP_SEC_001')
        self.assertEqual(self.parser.data['environment'][0], 'SERVER002')
        self.assertEqual(self.parser.data['test_id'][0], 'sec_auth_001')
        self.assertEqual(self.parser.data['result'][0], 'PASS')
        self.assertIsNone(self.parser.data['reason'][0])
        self.assertIsNone(self.parser.data['debug'][0])

    # gap_rssi_001.xml
    def test_parse_df_gap_rssi_001_xml_gap_rssi_001(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertEqual(self.parser.data['test_id'][3], 'gap_rssi_004')
        self.assertEqual(self.parser.data['result'][3], 'SKIP')
        self.assertEqual(self.parser.data['reason'][3], 'Not implemented')
        self.assertIsNone(self.parser.data['debug'][3])
        self.assertEqual(self.parser.data['test_suite'][3], 'GAP_RSSI_001')
        self.assertEqual(self.parser.data['environment'][3], 'LOCAL')

    ###################################################################
    # testing the detailed report generation

    def test_report_gap_conn_folder_test_suite_equals_gap_conn_001(self):
        self.parser.process_logs('test/gap/conn')
        self.parser.generate_detailed_report()
        self.assertTrue('GAP_CONN' in self.parser.data['test_suite'][0])
        self.assertFalse('GAP_SEC' in self.parser.data['test_suite'][0])
        self.assertFalse('GAP_RSSI' in self.parser.data['test_suite'][0])

    # gap_conn_001.xml
    def test_report_gap_conn_001(self):
        self.parser.process_logs('test/gap/conn')
        self.parser.generate_detailed_report()
        self.assertEqual(self.parser.report_dict['PASS'], 2)
        self.assertEqual(self.parser.report_dict['FAIL'], 1)
        self.assertEqual(self.parser.report_dict['SKIP'], 1)

    def test_report_gap_conn_001_percent(self):
        self.parser.process_logs('test/gap/conn')
        self.parser.generate_detailed_report()
        
        pass_percentage = (self.parser.report_dict['PASS'] * 100 / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'] + self.parser.report_dict['FAIL']))
        fail_percentage = (self.parser.report_dict['FAIL'] * 100 / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'] + self.parser.report_dict['FAIL']))
        skip_percentage = (self.parser.report_dict['SKIP'] * 100 / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'] + self.parser.report_dict['FAIL']))
        
        self.assertEqual(self.parser.report_dict['PASS'], 2)
        self.assertEqual(pass_percentage, 50)
        self.assertEqual(self.parser.report_dict['FAIL'], 1)
        self.assertEqual(skip_percentage, 25)
        self.assertEqual(self.parser.report_dict['SKIP'], 1)
        self.assertEqual(skip_percentage, 25)

    # gap_sec_001.xml
    def test_report_gap_sec_001(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.parser.generate_detailed_report()
        self.assertEqual(self.parser.report_dict['PASS'], 3)
        self.assertEqual(self.parser.report_dict['SKIP'], 1)

    def test_report_gap_sec_001_percent(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.parser.generate_detailed_report()
        
        pass_percentage = (self.parser.report_dict['PASS'] / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'])) * 100
        skip_percentage = (self.parser.report_dict['SKIP'] / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'])) * 100
        self.assertEqual(self.parser.report_dict['PASS'], 3)
        self.assertEqual(pass_percentage, 75)
        self.assertEqual(self.parser.report_dict['SKIP'], 1)
        self.assertEqual(skip_percentage, 25)

    # gap_rssi_001.xml
    def test_report_gap_rssi_001(self):
        self.parser.process_logs('test/gap/rssi')
        self.parser.generate_detailed_report()
        self.assertEqual(self.parser.report_dict['PASS'], 2)
        self.assertEqual(self.parser.report_dict['FAIL'], 1)
        self.assertEqual(self.parser.report_dict['SKIP'], 2)

    def test_report_gap_rssi_001_percent(self):
        self.parser.process_logs('test/gap/rssi')
        self.parser.generate_detailed_report()
        
        pass_percentage = (self.parser.report_dict['PASS'] * 100 / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'] + self.parser.report_dict['FAIL']))
        fail_percentage = (self.parser.report_dict['FAIL'] * 100 / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'] + self.parser.report_dict['FAIL']))
        skip_percentage = (self.parser.report_dict['SKIP'] * 100 / 
                          (self.parser.report_dict['PASS'] + self.parser.report_dict['SKIP'] + self.parser.report_dict['FAIL']))
        
        self.assertEqual(self.parser.report_dict['PASS'], 2)
        self.assertEqual(pass_percentage, 40)
        self.assertEqual(self.parser.report_dict['FAIL'], 1)
        self.assertEqual(fail_percentage, 20)
        self.assertEqual(self.parser.report_dict['SKIP'], 2)
        self.assertEqual(skip_percentage, 40)
        
    ###################################################################
    # testing method 'get_result_by_type'

    # for general directory
    def test_result_default_dir(self):
        self.parser.process_logs('test')
        self.assertEqual(self.parser.get_result_by_type('PASS'), 7)
        self.assertEqual(self.parser.get_result_by_type('FAIL'), 2)
        self.assertEqual(self.parser.get_result_by_type('SKIP'), 4)
   
    # gap_conn_001.xml
    def test_result_gap_conn_001(self):
        self.parser.process_logs('test/gap/conn')
        self.assertEqual(self.parser.get_result_by_type('PASS'), 2)
        self.assertEqual(self.parser.get_result_by_type('FAIL'), 1)
        self.assertEqual(self.parser.get_result_by_type('SKIP'), 1)

    # gap_sec_001.xml
    def test_result_gap_sec_001(self):
        self.parser.process_logs('test/gap/sec/seci')
        self.assertEqual(self.parser.get_result_by_type('PASS'), 3)
        self.assertEqual(self.parser.get_result_by_type('SKIP'), 1)

    # gap_rssi_001.xml
    def test_result_gap_sec_001(self):
        self.parser.process_logs('test/gap/rssi')
        self.assertEqual(self.parser.get_result_by_type('PASS'), 2)
        self.assertEqual(self.parser.get_result_by_type('FAIL'), 1)
        self.assertEqual(self.parser.get_result_by_type('SKIP'), 2)


# running the tests implemented in the above class
if __name__ == "__main__":
    unittest.main()