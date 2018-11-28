# =*= License: GPL-3+ =*=

import cliapp

import vmdb


class OverlayPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(OverlayStepRunner())


class OverlayStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['overlay', 'paths']

    def run(self, step, settings, state):
        fs_tag = step['overlay']
        paths = step['paths']
        mount_point = state.tags.get_mount_point(fs_tag)
        for path in paths:
            vmdb.runcmd(['cp', '-av', path + '/.', mount_point])
