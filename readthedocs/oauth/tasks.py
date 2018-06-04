# -*- coding: utf-8 -*-
"""Tasks for OAuth services."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from django.contrib.auth.models import User

from readthedocs.core.utils.tasks import (
    PublicTask, permission_check, user_id_matches)

from .services import registry


@permission_check(user_id_matches)
class SyncRemoteRepositories(PublicTask):

    name = __name__ + '.sync_remote_repositories'
    public_name = 'sync_remote_repositories'
    queue = 'web'

    def run_public(self, user_id):
        user = User.objects.get(pk=user_id)
        for service_cls in registry:
            for service in service_cls.for_user(user):
                service.sync()


sync_remote_repositories = SyncRemoteRepositories()
