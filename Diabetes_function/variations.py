import numpy as np
import polars as pl

from drk_report_helpers.utils.typings_diabetes import BPressure, MediateState


def get_args(mediate_state: MediateState):

    bg_measurements = mediate_state["bg_measurements"]

    range = dict(
        systolic=(mediate_state["glucose"]["max"]["value"] - mediate_state["glucose"]["min"]["value"]),
    )

    deviation = dict(
        glucose=np.std(bg_measurements[BPressure.GLUCOSE].filter(bg_measurements[BPressure.GLUCOSE].is_not_null()).to_list()),
    )

    stats = dict(
        glucose_max=mediate_state["glucose"]["max"]["value"],
        glucose_min=mediate_state["glucose"]["min"]["value"],
    )

    return dict(range=range, deviation=deviation, stats=stats)
