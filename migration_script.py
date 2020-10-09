from collector.models import CollectorModel


def migrate():

    if not CollectorModel.exists():
        CollectorModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


if __name__ == "__main__":
    migrate()
