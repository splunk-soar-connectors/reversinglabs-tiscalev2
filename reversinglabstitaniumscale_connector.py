#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------
# Phantom sample App Connector python file
# -----------------------------------------

# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

import json

# Phantom App imports
import phantom.app as phantom
from phantom import vault
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector
from ReversingLabs.SDK.tiscale import TitaniumScale

# Our helper lib reversinglabs-sdk-py3 internally utilizes pypi requests (with named parameters) which is shadowed by Phantom
# requests (which has renamed parameters (url>>uri), hence this workarounds
old_get = phantom.requests.get


def new_get(url, **kwargs):
    return old_get(url, **kwargs)


phantom.requests.get = new_get

old_post = phantom.requests.post


def new_post(url, **kwargs):
    return old_post(url, **kwargs)


phantom.requests.post = new_post

old_delete = phantom.requests.delete


def new_delete(url, **kwargs):
    return old_delete(url, **kwargs)


phantom.requests.delete = new_delete


class ReversinglabsTitaniumScaleConnector(BaseConnector):
    USER_AGENT = "ReversingLabs Splunk SOAR TitaniumScale v1.0.0"

    # The actions supported by this connector
    ACTION_ID_TEST_CONNECTIVITY = "test_connectivity"
    ACTION_ID_DETONATE_FILE = "detonate"
    ACTION_ID_DETONATE_FILE_AND_GET_REPORT = "detonate_file_and_get_report"
    ACTION_ID_GET_REPORT = "get_report"

    def __init__(self):
        # Call the BaseConnectors init first
        super(ReversinglabsTitaniumScaleConnector, self).__init__()

        self.ACTIONS = {
            self.ACTION_ID_TEST_CONNECTIVITY: self._handle_test_connectivity,
            self.ACTION_ID_DETONATE_FILE: self._handle_detonate_file,
            self.ACTION_ID_DETONATE_FILE_AND_GET_REPORT: self._handle_detonate_file_and_get_report,
            self.ACTION_ID_GET_REPORT: self._handle_get_report,
        }

        self._state = None

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        self.tiscale_url = config["url"]
        self.tiscale_token = config["token"]
        self.wait_time = config["wait_time"]
        self.retries = config["retries"]

        self.tiscale = TitaniumScale(host=self.tiscale_url, token=self.tiscale_token,
                                     wait_time_seconds=self.wait_time, retries=self.retries,
                                     user_agent=self.USER_AGENT)

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS

    def handle_action(self, param):
        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()
        action = self.ACTIONS.get(action_id)
        if not action:
            return

        action_result = self.add_action_result(ActionResult(dict(param)))

        try:
            action(action_result, param)
        except Exception as err:
            return action_result.set_status(phantom.APP_ERROR, str(err))

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_detonate_file_and_get_report(self, action_result, param):
        self.debug_print("Action handler", self.get_action_identifier())

        file_vault_id = param["vault_id"]
        success, msg, files_array = vault.vault_info(container_id=self.get_container_id())
        if not success:
            raise Exception('Unable to get Vault item details. Error details: {0}'.format(msg))

        file = next(filter(lambda x: x["vault_id"] == file_vault_id, files_array), None)
        if not file:
            raise Exception('Unable to get Vault item details. Error details: {0}'.format(msg))

        response = self.tiscale.upload_sample_and_get_results(file_path=file["path"], full_report=param.get("full_report"))

        self.debug_print("Executed", self.get_action_identifier())

        action_result.add_data(response.json())

    def _handle_detonate_file(self, action_result, param):
        self.debug_print("Action handler", self.get_action_identifier())

        file_vault_id = param["vault_id"]
        success, msg, files_array = vault.vault_info(container_id=self.get_container_id())
        if not success:
            raise Exception('Unable to get Vault item details. Error details: {0}'.format(msg))

        file = next(filter(lambda x: x["vault_id"] == file_vault_id, files_array), None)
        if not file:
            raise Exception('Unable to get Vault item details. Error details: {0}'.format(msg))

        response = self.tiscale.upload_sample_from_path(file_path=file["path"])

        print(response.json())

        self.debug_print("Executed", self.get_action_identifier())

        action_result.add_data(response.json())

    def _handle_get_report(self, action_result, param):
        self.debug_print("Action handler", self.get_action_identifier())

        response = self.tiscale.get_results(task_url=param.get("task_url"), full_report=param.get("full_report"))

        print(response.json())

        self.debug_print("Executed", self.get_action_identifier())

        action_result.add_data(response.json())

    def _handle_test_connectivity(self, action_result, param):
        self.debug_print("Action handler", self.get_action_identifier())

        self.tiscale.test_connection()

        self.save_progress("Test Connectivity Passed")


def main():
    import argparse

    argparser = argparse.ArgumentParser()
    args = argparser.parse_args()
    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)

        connector = ReversinglabsTitaniumScaleConnector()
        connector.print_progress_message = True

        connector._handle_action(json.dumps(in_json), None)
    exit(0)


if __name__ == '__main__':
    main()
