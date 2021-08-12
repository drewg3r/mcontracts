import random
from loguru import logger


def generate_ids(filename: str, min_id: int, max_id: int):
    ids = [i for i in range(min_id, max_id)]
    random.shuffle(ids)

    with open(filename, "w") as f:
        for num in ids:
            f.write("{}\n".format(num))


def load_ids(filename: str):
    logger.info("Loading random ids")
    id_to_rdi = {}
    rid_to_id = {}
    with open(filename, "r") as f:
        for i, num in enumerate(f):
            num = num.split()[0]
            id_to_rdi[i] = int(num)
            rid_to_id[int(num)] = i
    return id_to_rdi, rid_to_id

