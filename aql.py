from attr._make import fields

import related
import enum


class TypeEnum(enum.Enum):
    File = "file"
    Folder = "folder"
    Any = "any"


@related.immutable(strict=True)
class Item:
    repo = related.StringField(required=False)
    path = related.StringField(required=False)
    name = related.StringField(required=False)

    created = related.DateTimeField(required=False)
    modified = related.DateTimeField(required=False)
    updated = related.DateTimeField(required=False)

    created_by = related.StringField(required=False)
    modified_by = related.StringField(required=False)

    type = related.StringField(required=False)

    depth = related.IntegerField(required=False)

    original_md5 = related.StringField(required=False)
    actual_md5 = related.StringField(required=False)
    original_sha1 = related.StringField(required=False)
    actual_sha1 = related.StringField(required=False)
    sha256 = related.StringField(required=False)

    size = related.FloatField(required=False)

    virtual_repos = related.StringField(required=False)

    # Child fields
    properties = related.SequenceField("aql.Property", required=False)
    archives = related.SequenceField("aql.Archive", required=False)
    dependencies = related.SequenceField("aql.Dependency", required=False)
    releases = related.SequenceField("aql.ReleaseArtifact", required=False)
    stats = related.SequenceField("aql.Stat", required=False)
    artifacts = related.SequenceField("aql.Artifact", required=False)


@related.immutable(strict=True)
class Archive:
    # Child fields
    entries = related.SequenceField("aql.Entry", required=False)
    items = related.SequenceField("aql.Item", required=False)


@related.immutable(strict=True)
class Entry:
    name = related.StringField(required=False)
    path = related.StringField(required=False)

    # Child fields
    archives = related.SequenceField("aql.Archive", required=False)


@related.immutable(strict=True)
class Promotion:
    created = related.DateTimeField(required=False)
    created_by = related.StringField(required=False)
    status = related.StringField(required=False)
    repo = related.StringField(required=False)
    comment = related.StringField(required=False)
    user = related.StringField(required=False)

    # Child fields
    builds = related.SequenceField("aql.Build", required=False)


@related.immutable(strict=True)
class Build:
    url = related.StringField(required=False)
    name = related.StringField(required=False)
    number = related.StringField(required=False)

    created = related.DateTimeField(required=False)
    modified = related.DateTimeField(required=False)
    started = related.DateTimeField(required=False)

    modified_by = related.StringField(required=False)
    created_by = related.StringField(required=False)

    # Child fields
    modules = related.SequenceField("aql.Module", required=False)
    properties = related.SequenceField("aql.Property", required=False)


@related.immutable(strict=True)
class Property:
    key = related.StringField(required=False)
    value = related.StringField(required=False)

    # Child fields
    items = related.SequenceField("aql.Item", required=False)
    modules = related.SequenceField("aql.Module", required=False)
    builds = related.SequenceField("aql.Build", required=False)
    promotions = related.SequenceField("aql.Promotion", required=False)


@related.immutable(strict=True)
class Stat:
    downloaded = related.DateTimeField(required=False)
    downloads = related.IntegerField(required=False)
    downloaded_by = related.StringField(required=False)

    remote_downloads = related.IntegerField(required=False)
    remote_downloaded = related.DateTimeField(required=False)
    remote_downloaded_by = related.StringField(required=False)

    remote_origin = related.StringField(required=False)
    remote_path = related.StringField(required=False)

    # Child fields
    items = related.SequenceField("aql.Item", required=False)


@related.immutable(strict=True)
class Artifact:
    name = related.StringField(required=False)
    type = related.StringField(required=False)
    sha1 = related.StringField(required=False)
    md5 = related.StringField(required=False)

    # Child fields
    items = related.SequenceField("aql.Item", required=False)
    modules = related.SequenceField("aql.Module", required=False)
    dependencies = related.SequenceField("aql.Dependency", required=False)


@related.immutable(strict=True)
class Module:
    name: related.StringField(required=False)

    # Child fields
    artifacts = related.SequenceField("aql.Artifact", required=False)
    builds = related.SequenceField("aql.Build", required=False)


@related.immutable(strict=True)
class Dependency:
    name: related.StringField(required=False)
    scope: related.StringField(required=False)
    type: related.StringField(required=False)
    sha1: related.StringField(required=False)
    md5: related.StringField(required=False)

    # Child fields
    items = related.SequenceField("aql.Item", required=False)
    module = related.SequenceField("aql.Module", required=False)
    properties = related.SequenceField("aql.Property", required=False)


@related.immutable(strict=True)
class Release:
    name: related.StringField(required=False)
    version: related.StringField(required=False)
    status: related.StringField(required=False)
    created: related.DateTimeField(required=False)
    signature: related.StringField(required=False)

    # Child fields
    artifacts = related.SequenceField("aql.ReleaseArtifact", required=False)


@related.immutable(strict=True)
class ReleaseArtifact:
    path = related.StringField(required=False)

    # Child fields
    items = related.SequenceField("aql.Item", required=False)


def preprocess_keys(keys):
    orig = keys.copy()

    for key, value in orig.items():
        names = key.split(".")
        if len(names) > 1:
            name = names[-1]
            keys[name] = value
            del keys[key]
        if isinstance(value, dict):
            preprocess_keys(value)
        elif isinstance(value, list):
            for entry in value:
                preprocess_keys(entry)


def to_model(cls, value):
    # Preprocess keys
    preprocess_keys(value)
    return related.to_model(cls, value)
