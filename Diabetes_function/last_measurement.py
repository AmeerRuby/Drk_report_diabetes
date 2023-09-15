import polars as pl

from drk_report_helpers.utils.typings_diabetes import BPressure, MediateState, PatientData


def get_args(mediate_state: MediateState) -> dict:

    last_bg = mediate_state["last_bg"]

    return dict(
        timestamp=last_bg[0],
        blood_glucose=last_bg[1],
    )
