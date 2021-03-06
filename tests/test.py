# Copyright (c) 2018 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
import unittest
import tempfile
import shutil
from urllib.parse import quote as urlquote
import json

from signac_dashboard import Dashboard
from signac import init_project


class DashboardTestCase(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        self.project = init_project('dashboard-test-project',
                                    root=self._tmp_dir,
                                    make_dir=False)
        # Set up some fake jobs
        for a in range(3):
            for b in range(2):
                job = self.project.open_job({'a': a, 'b': b})
                with job:
                    job.document['sum'] = a + b
        self.config = {}
        self.modules = []
        self.dashboard = Dashboard(config=self.config,
                                   project=self.project,
                                   modules=self.modules)
        self.test_client = self.dashboard.app.test_client()
        self.addCleanup(shutil.rmtree, self._tmp_dir)

    def tearDown(self):
        pass

    def test_get_jobs(self):
        rv = self.test_client.get('/jobs', follow_redirects=True)
        response = str(rv.get_data())
        assert 'dashboard-test-project' in response

    def test_job_count(self):
        rv = self.test_client.get('/jobs', follow_redirects=True)
        response = str(rv.get_data())
        assert '{} jobs'.format(self.project.num_jobs()) in response

    def test_sp_search(self):
        dictquery = {'a': 0}
        true_num_jobs = len(list(self.project.find_jobs(dictquery)))
        query = urlquote(json.dumps(dictquery))
        rv = self.test_client.get('/search?q={}'.format(query),
                                  follow_redirects=True)
        response = str(rv.get_data())
        assert '{} jobs'.format(true_num_jobs) in response

    def test_doc_search(self):
        dictquery = {'sum': 1}
        true_num_jobs = len(list(self.project.find_jobs(doc_filter=dictquery)))
        query = urlquote('doc:'+json.dumps(dictquery))
        rv = self.test_client.get('/search?q={}'.format(query),
                                  follow_redirects=True)
        response = str(rv.get_data())
        assert '{} jobs'.format(true_num_jobs) in response


if __name__ == '__main__':
    unittest.main()
