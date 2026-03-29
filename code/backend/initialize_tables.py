#! /usr/bin/env python3
import inspect
from importlib import import_module
from argparse import ArgumentParser
from pynamodb.constants import PROVISIONED_BILLING_MODE


def _custom_model_tables():
    """app.models 内で CustomModel を継承した具象クラスだけを列挙する。"""
    models = import_module("app.models")
    base = models.CustomModel
    out = []
    for _, cls in inspect.getmembers(models, inspect.isclass):
        if cls is base:
            continue
        if not issubclass(cls, base):
            continue
        if cls.__module__ != models.__name__:
            continue
        out.append(cls)
    return sorted(out, key=lambda c: c.__name__)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--stage', type=str, default='local', help='Stage to create tables')
    return parser.parse_args()

def create_tables(args):
    tables = _custom_model_tables()
    if args.stage == 'local':
        # LocalStack は PAY_PER_REQUEST 対応だが、一部環境では PROVISIONED_BILLING_MODE の方が安定する
        print("Creating tables in local stage")
        for table in tables:
            print(f"Creating table {table.__name__}")
            table.create_table(wait=True,
                billing_mode=PROVISIONED_BILLING_MODE,
                read_capacity_units=1,
                write_capacity_units=1
            )
    else:
        print("Creating tables in non-local stage")
        for table in tables:
            print(f"Creating table {table.__name__}")
            table.create_table(wait=True,
                billing_mode=PROVISIONED_BILLING_MODE,
                read_capacity_units=10,
                write_capacity_units=1
            )

if __name__ == "__main__":
    args = parse_args()
    create_tables(args)
