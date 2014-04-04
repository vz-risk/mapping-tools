import unittest

from mock import MagicMock, patch, sentinel

class CSVWriterTestCase(unittest.TestCase):
    
    def setUp(self):
        self._patch_csv()

    def _patch_csv(self):
        mock_DictWriter = self._patch_csv_DictWriter()
        self.mock_csv = MagicMock(
            DictWriter=mock_DictWriter)

    def _patch_csv_DictWriter(self):
        patcher = patch('csv.DictWriter')
        mock_DictWriter = patcher.start()
        self.addCleanup(patcher.stop)
        return mock_DictWriter()

class DefaultINIShouldMakeSTDOUTWriter(CSVWriterTestCase):
    pass

class AddAllShouldWriteHeaderAndObjs(CSVWriterTestCase):
    pass

class CommitShouldDoNothing(CSVWriterTestCase):
    pass
