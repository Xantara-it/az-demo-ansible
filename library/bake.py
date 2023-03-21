#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2022, Robin Gierse <robin.gierse@tribe29.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_url=dict(type="str", required=True),
        site=dict(type="str", required=True),
        automation_user=dict(type="str", required=True),
        automation_secret=dict(type="str", required=True, no_log=True),
        sites=dict(type="raw", default=[]),
    )

    result = dict(changed=False, failed=False, http_code="", msg="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    changed = False
    failed = False
    http_code = ""
    sites = module.params["sites"]
    if sites == {}:
        sites = []

    http_code_mapping = {
        # http_code: (changed, failed, "Message")
        200: (True, False, "Changes activated."),
        204: (True, False, "Changes activated."),
        302: (True, False, "Redirected."),
        422: (False, False, "There are no changes to be activated."),
        400: (False, True, "Bad Request."),
        401: (
            False,
            True,
            "Unauthorized: There are foreign changes, which you may not activate, or you did not use <force_foreign_changes>.",
        ),
        403: (False, True, "Forbidden: Configuration via WATO is disabled."),
        406: (False, True, "Not Acceptable."),
        409: (False, True, "Conflict: Some sites could not be activated."),
        415: (False, True, "Unsupported Media Type."),
        423: (False, True, "Locked: There is already an activation running."),
    }

    # Declare headers including authentication to send to the Checkmk API
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer %s %s"
        % (
            module.params.get("automation_user", ""),
            module.params.get("automation_secret", ""),
        ),
    }

    params = {
        "redirect": False,
        "sites": sites,
    }

    base_url = "%s/%s/check_mk/api/1.0" % (
        module.params.get("server_url", ""),
        module.params.get("site", ""),
    )

    api_endpoint = "/domain-types/agent/actions/bake/invoke"
    url = base_url + api_endpoint
    response, info = fetch_url(
        module, url, module.jsonify(params), headers=headers, method="POST"
    )
    http_code = info["status"]

    # Kudos to Lars G.!
    if http_code in http_code_mapping.keys():
        changed, failed, msg = http_code_mapping[http_code]
    else:
        changed, failed, msg = (False, True, "Error calling API")

    result["msg"] = msg
    result["changed"] = changed
    result["failed"] = failed
    result["http_code"] = http_code

    if result["failed"]:
        module.fail_json(**result)

    # Work around a possible race condition in the activation process.
    # The sleep can be removed, once this is stable on Checkmk's and.
    time.sleep(3)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
