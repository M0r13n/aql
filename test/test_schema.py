import datetime
import unittest

from aql import to_model, Item, Build


class SchemaTestCase(unittest.TestCase):

    def test_item_search_query_simple(self):
        response = {
            "repo": "docker-remote-repo-cache",
            "path": "alpine/latest",
            "name": "manifest.json",
            "type": "file",
            "size": 528,
            "created": "2021-03-21T13:54:52.383",
            "created_by": "admin",
            "modified": "2021-03-21T13:54:32.000",
            "modified_by": "admin",
            "updated": "2021-03-21T13:54:52.384"
        }

        item = to_model(Item, response)

        self.assertIsInstance(item, Item)
        self.assertEqual(item.repo, "docker-remote-repo-cache")
        self.assertEqual(item.path, "alpine/latest")
        self.assertEqual(item.name, "manifest.json")
        self.assertEqual(item.type, "file")
        self.assertEqual(item.size, 528)
        self.assertEqual(item.created, datetime.datetime(2021, 3, 21, 13, 54, 52, 383000))
        self.assertEqual(item.created_by, "admin")
        self.assertEqual(item.modified, datetime.datetime(2021, 3, 21, 13, 54, 32))
        self.assertEqual(item.modified_by, "admin")
        self.assertEqual(item.updated, datetime.datetime(2021, 3, 21, 13, 54, 52, 384000))

    def test_schema_item_reduced(self):
        responses = [
            {
                "name": "manifest.json"
            },
            {
                "name": "sha256__4c0d98bf9879488e0407f897d9dd4bf758555a78e39675e72b5124ccf12c2580"
            },
            {
                "name": "sha256__e50c909a8df2b7c8b92a6e8730e210ebe98e5082871e66edd8ef4d90838cbd25.marker"
            },
            {
                "repo": "docker-remote-repo",
                "name": "manifest.json"
            },
            {
                "repo": "docker-remote-repo",
                "name": "repository.catalog"
            },
            {
                "repo": "docker-remote-repo",
                "name": "sha256__4c0d98bf9879488e0407f897d9dd4bf758555a78e39675e72b5124ccf12c2580"
            },
            {
                "repo": "docker-remote-repo",
                "name": "sha256__e50c909a8df2b7c8b92a6e8730e210ebe98e5082871e66edd8ef4d90838cbd25"
            }
        ]

        items = [to_model(Item, response) for response in responses]

        self.assertEqual(
            [item.name for item in items],
            ['manifest.json',
             'sha256__4c0d98bf9879488e0407f897d9dd4bf758555a78e39675e72b5124ccf12c2580',
             'sha256__e50c909a8df2b7c8b92a6e8730e210ebe98e5082871e66edd8ef4d90838cbd25.marker',
             'manifest.json',
             'repository.catalog',
             'sha256__4c0d98bf9879488e0407f897d9dd4bf758555a78e39675e72b5124ccf12c2580',
             'sha256__e50c909a8df2b7c8b92a6e8730e210ebe98e5082871e66edd8ef4d90838cbd25'])

    def test_item_schema_complex(self):
        response = {
            "repo": "ext-snapshot-local",
            "path": "org/jfrog/test/multi2/3.0.0-SNAPSHOT",
            "name": "multi2-3.0.0-20151012.205507-1.jar",
            "type": "file",
            "size": 1015,
            "created": "2015-10-12T22:55:23.022+02:00",
            "created_by": "admin",
            "modified": "2015-10-12T22:55:23.013+02:00",
            "modified_by": "admin",
            "updated": "2015-10-12T22:55:23.013+02:00",
            "archives": [{
                "entries": [{
                    "entry.name": "App.class",
                    "entry.path": "artifactory/test"
                }, {
                    "entry.name": "MANIFEST.MF",
                    "entry.path": "META-INF"
                }]
            }]
        }
        item = to_model(Item, response)
        tzinfo = datetime.timezone(datetime.timedelta(seconds=7200))

        self.assertEqual(item.path, "org/jfrog/test/multi2/3.0.0-SNAPSHOT")
        self.assertEqual(item.repo, "ext-snapshot-local")
        self.assertEqual(item.name, "multi2-3.0.0-20151012.205507-1.jar")
        self.assertEqual(item.type, "file")
        self.assertEqual(item.size, 1015)
        self.assertEqual(item.created, datetime.datetime(2015, 10, 12, 22, 55, 23, 22000, tzinfo=tzinfo))
        self.assertEqual(item.created_by, "admin")
        self.assertEqual(item.modified, datetime.datetime(2015, 10, 12, 22, 55, 23, 13000, tzinfo=tzinfo))
        self.assertEqual(item.modified_by, "admin")
        self.assertEqual(item.updated, datetime.datetime(2015, 10, 12, 22, 55, 23, 13000, tzinfo=tzinfo))
        self.assertEqual(len(item.archives), 1)
        self.assertEqual(len(item.archives[0].entries), 2)
        self.assertEqual(item.archives[0].entries[0].name, "App.class")
        self.assertEqual(item.archives[0].entries[0].path, "artifactory/test")

    def test_schema_build_simple(self):
        response = {
            "build.created": "2015-09-06T15:49:01.156",
            "build.created_by": "admin",
            "build.name": "maven+example",
            "build.number": "313",
            "build.url": "http://localhost:9595/jenkins/job/maven+example/313/",
            "modules": [{
                "artifacts": [{
                    "items": [{
                        "name": "multi-3.0.0-20150906.124843-1.pom"
                    }]
                }]
            }]
        }

        build = to_model(Build, response)

        self.assertIsInstance(build, Build)
        self.assertEqual(build.created, datetime.datetime(2015, 9, 6, 15, 49, 1, 156000))
        self.assertEqual(build.created_by, "admin")
        self.assertEqual(build.name, "maven+example")
        self.assertEqual(build.number, "313")
        self.assertEqual(build.url, "http://localhost:9595/jenkins/job/maven+example/313/")
        self.assertEqual(len(build.modules), 1)
        self.assertEqual(len(build.modules[0].artifacts), 1)
        self.assertEqual(len(build.modules[0].artifacts[0].items), 1)
        self.assertEqual(build.modules[0].artifacts[0].items[0].name, "multi-3.0.0-20150906.124843-1.pom")
