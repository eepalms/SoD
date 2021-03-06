# Copyright 2014 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

from nova.tests.functional.api_sample_tests import test_servers

CONF = cfg.CONF
CONF.import_opt('osapi_compute_extension',
                'nova.api.openstack.compute.legacy_v2.extensions')


class ServerExternalEventsSamplesJsonTest(test_servers.ServersSampleBase):
    ADMIN_API = True
    extension_name = "os-server-external-events"

    def _get_flags(self):
        f = super(ServerExternalEventsSamplesJsonTest, self)._get_flags()
        f['osapi_compute_extension'] = CONF.osapi_compute_extension[:]
        f['osapi_compute_extension'].append(
            'nova.api.openstack.compute.contrib.server_external_events.'
            'Server_external_events')
        return f

    def setUp(self):
        """setUp Method for AdminActions api samples extension

        This method creates the server that will be used in each tests
        """
        super(ServerExternalEventsSamplesJsonTest, self).setUp()
        self.uuid = self._post_server()

    def test_create_event(self):
        subs = {
            'uuid': self.uuid,
            'name': 'network-changed',
            'status': 'completed',
            'tag': 'foo',
            }
        response = self._do_post('os-server-external-events',
                                 'event-create-req',
                                 subs)
        self._verify_response('event-create-resp', subs, response, 200)
