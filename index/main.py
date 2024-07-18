# Resource
# --------
# id unique integer
# name text unique?
# path text
# length integer

# Metadata
# --------
# id unique integer
# resource_id integer foreign key
# metadata_type metadata type

# Metadata Types
# --------------


# import sys
import os
import pathlib
from dataclasses import dataclass


@dataclass
class ResourceFile:
    file_name: str
    full_path: str
    size: int


def get_file_list(directory: str) -> list[ResourceFile]:
    path = pathlib.Path(directory)
    resources = []
    for file in path.iterdir():
        # should find way to calculate
        # length of mp4
        resource = ResourceFile(
            file_name=file.name,
            full_path=str(file.absolute()),
            size=file.lstat().st_size,
        )
        resources.append(resource)
    return resources


def index_files(file_list: list[ResourceFile]):
    # insert into db
    pass


def main(directory):
    file_list = get_file_list(directory)
    index_files(file_list)


if __name__ == "__main__":
    try:
        directory = os.sys.argv[1]
        main(directory)
    except IndexError:
        print("Error: No directory provided")
        os.sys.exit(1)
