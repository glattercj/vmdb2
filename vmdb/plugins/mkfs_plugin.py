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


import cliapp

import vmdb


class MkfsPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(MkfsStepRunner())


class MkfsStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['mkfs', 'partition']

    def run(self, step, settings, state):
        fstype = step['mkfs']
        tag = step['partition']
        device = state.tags.get_dev(tag)
        # Optional: make UUID tmp file unique
        name = f"-{step['name']}" if 'name' in step else ""

        cmd = ['/sbin/mkfs', '-t', fstype]
        if 'label' in step:
            if fstype == 'vfat':
                cmd.append('-n')
            elif fstype == 'f2fs':
                cmd.append('-l')
            else:
                cmd.append('-L')
            cmd.append(step['label'])
        cmd.append(device)
        output = vmdb.runcmd(cmd)
        output = output.split()
        idx = output.index(b'UUID:')
        uuid = output[idx+1].decode('utf-8')
        vmdb.runcmd(['echo', uuid], ['tee', f'/tmp/grub-uuid{name}'])

        state.tags.set_fstype(tag, fstype)
