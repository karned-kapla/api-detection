from typing import Type

from common_api.services.v0 import Logger
from repositories.detection_repository_mongo import DetectionRepositoryMongo

logger = Logger()


class Repositories:
    def __init__(self, detection_repo=None):
        self.detection_repo = detection_repo


class BucketRepositories:
    def __init__(self, detection_bucket_repo=None):
        self.detection_bucket_repo = detection_bucket_repo


def get_repositories(uri: str) -> Repositories | Type[Repositories]:
    if uri.startswith("mongodb"):
        logger.info("Using MongoDB repositories")
        return Repositories(
            detection_repo = DetectionRepositoryMongo(uri)
        )

    return Repositories


def get_bucket_repositories(credentials) -> BucketRepositories | Type[BucketRepositories]:

    return BucketRepositories
