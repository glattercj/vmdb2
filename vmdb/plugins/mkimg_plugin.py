# Copyright 2017  Lars Wirzenius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =*= License: GPL-3+ =*=



import os
import cliapp

import vmdb


class MkimgPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(MkimgStepRunner())
        self.app.settings.bytesize(
            ['size'],
            'size of output image',
            default='1GiB')


class MkimgStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['mkimg']

    def run(self, step, settings, state):
        size = step['size']
        state.filename = step['mkimg']
        state.fmt = step.get('format', 'raw')
        state.compress = step.get('compress', 'false')
        vmdb.runcmd(['qemu-img', 'create', '-f', 'raw', state.filename, size])

    def teardown(self, step, settings, state):
        coremelt = getattr(state, 'COREMELT', False)
        if not coremelt and state.fmt != 'raw':
            args = ['qemu-img', 'convert', '-p', '-W', '-m16']
            tag = ''
            if state.compress == 'true':
                args.append('-c')
                tag = '_c'
            path = os.path.dirname(state.filename) + "/"
            parts = os.path.splitext(os.path.basename(state.filename))
            name = parts[0]
            ext = parts[1]
            name = name + '.qc2' if state.fmt == 'qcow2' else name + tag + ext
            args.extend(['-O', state.fmt, state.filename, path + name])
            vmdb.runcmd(args)
            vmdb.runcmd(['rm', '-f', state.filename])
