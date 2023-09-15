from datetime import datetime
from typing import List

import numpy as np
import polars as pl

from drk_report_helpers.utils.typings_diabetes import BPressure, MediateState, PatientData


def split_cols(bg_measurements: pl.DataFrame, type: str) -> pl.DataFrame:
    return bg_measurements.select([BPressure.TIMESTAMP, type]).drop_nulls()


def x(measurements: pl.DataFrame) -> List[int]:
    epoch_time = datetime(1970, 1, 1)
    return [(timestamp - epoch_time).total_seconds() / (24 * 3600) for timestamp in measurements[BPressure.TIMESTAMP].to_list()]


def slope(bg_measurements: pl.DataFrame, type: str):

    measurements: pl.DataFrame = split_cols(bg_measurements, type)
    X = x(measurements)

    return np.polyfit(X, measurements[type].to_list(), 1)[0]


def calc_slopes(bg_measurements: pl.DataFrame):

    return dict(
        glucose=slope(bg_measurements, BPressure.GLUCOSE),
    )


def get_args(mediate_state: MediateState):
    slopes = calc_slopes(mediate_state["bg_measurements"])
    stats = dict(
        glucose_max=mediate_state["glucose"]["max"]["value"],
        glucose_min=mediate_state["glucose"]["min"]["value"],
    )

    return dict(slopes=slopes, stats=stats)
