from collections import UserDict
from os.path import join

import pytest
from archive_datasets import archive
from hdx.api.configuration import Configuration
from hdx.utilities.dateparse import parse_date
from hdx.utilities.useragent import UserAgent


class CutDownDataset(UserDict):
    def get_hdx_url(self):
        return f"https://data.humdata.org/dataset/{self.data['name']}"

    def update_in_hdx(self, **args):
        return


class TestDataset:
    @staticmethod
    def search_in_hdx(fq):
        if "unosat" in fq:
            datasets = [
                {
                    "name": "unosat-test-recent",
                    "title": "unosat test recent",
                    "last_modified": "2023-10-10T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "unosat-test-should_archive",
                    "title": "unosat test old",
                    "last_modified": "2023-04-11T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "unosat-test-should_not_archive",
                    "title": "unosat test old",
                    "last_modified": "2023-04-12T00:00:00",
                    "data_update_frequency": "-2",
                    "archived": False,
                },
            ]
        else:
            datasets = [
                {
                    "name": "wfp-adam-test-recent",
                    "title": "wfp adam test recent",
                    "last_modified": "2023-04-12T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "wfp-adam-test-should_archive",
                    "title": "wfp adam test old",
                    "last_modified": "2022-03-02T00:00:00",
                    "data_update_frequency": "-1",
                    "archived": False,
                },
                {
                    "name": "wfp-adam-test-should_not_archive",
                    "title": "wfp adam test old",
                    "last_modified": "2022-03-02T00:00:00",
                    "data_update_frequency": "365",
                    "archived": False,
                },
            ]
        datasets = [CutDownDataset(dataset) for dataset in datasets]
        return datasets


class TestDatasetArchiver:
    @pytest.fixture(scope="function")
    def configuration(self):
        Configuration._create(
            hdx_read_only=True,
            user_agent="test",
            project_config_yaml=join("config", "project_configuration.yml"),
        )
        UserAgent.set_global("test")
        return Configuration.read()

    def test_archive(self, configuration):
        today = parse_date("2023-10-12")
        datasets = archive(configuration, today, DatasetCls=TestDataset)
        for dataset in datasets:
            name = dataset["name"]
            if dataset["archived"]:
                assert "should_archive" in name
            else:
                update_frequency = dataset["data_update_frequency"]
                if update_frequency == "-1":
                    assert "recent" in name
                else:
                    assert "should_not_archive" in name
