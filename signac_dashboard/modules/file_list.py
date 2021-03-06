# Copyright (c) 2018 The Regents of the University of Michigan
# All rights reserved.
# This software is licensed under the BSD 3-Clause License.
from signac_dashboard.module import Module
from flask import render_template, url_for
import os


class FileList(Module):

    def __init__(self, prefix_jobid=True, **kwargs):
        super().__init__(name='File List',
                         context='JobContext',
                         template='cards/file_list.html',
                         **kwargs)
        self.prefix_jobid = prefix_jobid

    def download_name(self, job, filename):
        if self.prefix_jobid:
            return '{}_{}'.format(str(job), filename)
        else:
            return filename

    def get_cards(self, job):
        files = sorted([{
                'name': filename,
                'url': url_for('get_file', jobid=str(job), filename=filename),
                'download': self.download_name(job, filename)
            } for filename in os.listdir(job.workspace())],
            key=lambda filedata: filedata['name'])
        return [{'name': self.name,
                 'content': render_template(self.template, files=files)}]
