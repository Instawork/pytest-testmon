import os
import sys
import pytest
from test.coveragepy.coveragetest import CoverageTest

class TestCoverageSubprocess(CoverageTest):

    def test_basic_run(self):
        path1 = self.make_file("subprocesstest.py", """\
        print("hello world")
        """)
        output = self.run_command('{} {}'.format(sys.executable, path1))
        assert output == "hello world\n"

    def test_pass_environ(self):
        path1 = self.make_file("subprocesstest.py", """\
        import os
        print(os.environ['TEST_NAME'])
        """)
        os.environ['TEST_NAME'] = 'TEST_VALUE'
        output = self.run_command('{} {}'.format(sys.executable, path1))
        assert output == "{}\n".format('TEST_VALUE')

    def test_coverage_expected_fail(self):
        path1 = self.make_file("subprocesstest.py", """\
        a=1
        """)
        os.environ['COV_CORE_SOURCE'] = 'yes'
        os.environ['COV_CORE_CONFIG'] = 'nonexistent_file'
        os.environ['COV_CORE_DATAFILE'] = 'bla'
        output = self.run_command('python {}'.format(path1))
        del os.environ['COV_CORE_SOURCE']
        del os.environ['COV_CORE_CONFIG']
        del os.environ['COV_CORE_DATAFILE']

        assert "Couldn't read 'nonexistent_file' as a config file" in output

    def test_subprocess(self):
        path1 = self.make_file("subprocesstest.py", """\
        a=1
        """)
        self.make_file('.testmoncoveragerc', """\
            [run]

            data_file = {}/.testmoncoverage
        """.format(os.getcwd()))
        os.environ['COV_CORE_SOURCE'] = 'yes'
        os.environ['COV_CORE_CONFIG']='{}/.testmoncoveragerc'.format(os.getcwd())
        os.environ['COV_CORE_DATAFILE'] = '.testmoncoverage'
        self.run_command('python {}'.format(path1))
        assert '.testmoncoverage' in "{}".format(os.listdir(os.getcwd())), os.listdir(os.getcwd())
        del os.environ['COV_CORE_SOURCE']
        del os.environ['COV_CORE_CONFIG']
        del os.environ['COV_CORE_DATAFILE']
