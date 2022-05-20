import sys
import click
import json
from typing import List
from prometheus_client import start_http_server, Gauge
from dataclasses import dataclass
from collections import defaultdict


@dataclass(eq=True, frozen=True)
class ConfigItem:
    match: dict
    metric_name: str
    value_fields: List[str]
    label_fields: List[str]
    description: str

    def __hash__(self):
        return hash(frozenset(self.match.items()))

    def matches(self, data):
        return all(str(data.get(k)) == str(v) for k, v in self.match.items())

    def labels(self, data):
        return {label: data.get(label) for label in self.label_fields}


@click.command
@click.option("--port", type=int, default=8081)
@click.argument("config_file", type=click.File("r"))
def main(port, config_file):
    config = [ConfigItem(**ci) for ci in json.load(config_file)]
    metrics = {}
    start_http_server(port)
    for line in sys.stdin:
        data = json.loads(line)

        ci = None
        for item in config:
            if item.matches(data):
                ci = item
                break
        if not ci:
            continue

        labels = ci.labels(data)
        for value_field in ci.value_fields:
            if ci.metric_name not in metrics:
                metrics[ci.metric_name] = Gauge(
                    f"rtl_433_{ci.metric_name}",
                    ci.description,
                    ci.label_fields + ["metric"],
                )
            metrics[ci.metric_name].labels(metric=value_field, **labels).set(
                int(data[value_field])
            )


if __name__ == "__main__":
    main()
