import extendSysPath
import unittest
import ModuleBaseTestCase
import mock
import Queue
import Utils
import RegexParser

class TestRegexParser(ModuleBaseTestCase.ModuleBaseTestCase):

    raw_data= '192.168.2.20 - - [28/Jul/2006:10:27:10 -0300] "GET /cgi-bin/try/ HTTP/1.0" 200 3395'

    def setUp(self):
        super(TestRegexParser, self).setUp(RegexParser.RegexParser(gp=mock.Mock()))

    def testHandleData(self):
        self.test_object.configure({'source_field': 'event',
                                    'field_extraction_patterns': {'http_access_log': '(?P<remote_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<identd>\w+|-)\s+(?P<user>\w+|-)\s+\[(?P<datetime>\d+\/\w+\/\d+:\d+:\d+:\d+\s.\d+)\]\s+\"(?P<url>.*)\"\s+(?P<http_status>\d+)\s+(?P<bytes_send>\d+)'}})
        result = self.conf_validator.validateModuleInstance(self.test_object)
        self.assertFalse(result)
        event = Utils.getDefaultDataDict({'event': self.raw_data})
        for result in self.test_object.handleData(event):
            self.assert_('bytes_send' in result and result['bytes_send'] == '3395')

    def testQueueCommunication(self):
        self.test_object.configure({'field_extraction_patterns': {'http_access_log': '(?P<remote_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<identd>\w+|-)\s+(?P<user>\w+|-)\s+\[(?P<datetime>\d+\/\w+\/\d+:\d+:\d+:\d+\s.\d+)\]\s+\"(?P<url>.*)\"\s+(?P<http_status>\d+)\s+(?P<bytes_send>\d+)'}})
        result = self.conf_validator.validateModuleInstance(self.test_object)
        self.assertFalse(result)
        self.test_object.start()
        self.input_queue.put(Utils.getDefaultDataDict({}))
        queue_emtpy = False
        try:
            self.output_queue.get(timeout=1)
        except Queue.Empty:
            queue_emtpy = True
        self.assert_(queue_emtpy != True)

    def testQueueCommunication(self):
        config = {'field_extraction_patterns': {'http_access_log': '(?P<remote_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<identd>\w+|-)\s+(?P<user>\w+|-)\s+\[(?P<datetime>\d+\/\w+\/\d+:\d+:\d+:\d+\s.\d+)\]\s+\"(?P<url>.*)\"\s+(?P<http_status>\d+)\s+(?P<bytes_send>\d+)'}}
        super(TestRegexParser, self).testQueueCommunication(config)

    def testOutputQueueFilterNoMatch(self):
        config = {'field_extraction_patterns': {'http_access_log': '(?P<remote_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<identd>\w+|-)\s+(?P<user>\w+|-)\s+\[(?P<datetime>\d+\/\w+\/\d+:\d+:\d+:\d+\s.\d+)\]\s+\"(?P<url>.*)\"\s+(?P<http_status>\d+)\s+(?P<bytes_send>\d+)'}}
        super(TestRegexParser, self).testOutputQueueFilterNoMatch(config)

    def testOutputQueueFilterMatch(self):
        config = {'field_extraction_patterns': {'http_access_log': '(?P<remote_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<identd>\w+|-)\s+(?P<user>\w+|-)\s+\[(?P<datetime>\d+\/\w+\/\d+:\d+:\d+:\d+\s.\d+)\]\s+\"(?P<url>.*)\"\s+(?P<http_status>\d+)\s+(?P<bytes_send>\d+)'}}
        super(TestRegexParser, self).testOutputQueueFilterMatch(config)

    def testWorksOnCopy(self):
        config = {'field_extraction_patterns': {'http_access_log': '(?P<remote_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<identd>\w+|-)\s+(?P<user>\w+|-)\s+\[(?P<datetime>\d+\/\w+\/\d+:\d+:\d+:\d+\s.\d+)\]\s+\"(?P<url>.*)\"\s+(?P<http_status>\d+)\s+(?P<bytes_send>\d+)'}}
        super(TestRegexParser, self).testWorksOnCopy(config)

    def testWorksOnOriginal(self):
        config = {'field_extraction_patterns': {'http_access_log': '(?P<remote_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<identd>\w+|-)\s+(?P<user>\w+|-)\s+\[(?P<datetime>\d+\/\w+\/\d+:\d+:\d+:\d+\s.\d+)\]\s+\"(?P<url>.*)\"\s+(?P<http_status>\d+)\s+(?P<bytes_send>\d+)'}}
        super(TestRegexParser, self).testWorksOnOriginal(config)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()