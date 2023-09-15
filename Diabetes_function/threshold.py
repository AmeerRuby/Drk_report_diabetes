import polars as pl

from drk_report_helpers.utils.typings_diabetes import BPressure, MediateState, PatientData


def get_args(patient_data: PatientData, mediate_state: MediateState) -> dict:

    if patient_data.get("bg_threshold").get("threshold_max") is None:
        return dict(
            elevated_percen=0,
            glucose_max=mediate_state["glucose"]["max"]["value"],
            glucose_timestamp=mediate_state["glucose"]["max"]["timestamp"],
            patient_threshold_glucose_max=0,
        )

    elevated_percen = get_elevated_percen(mediate_state["bg_measurements"], patient_data["bg_threshold"]["threshold_max"])

    return dict(
        elevated_percen=elevated_percen,
        glucose_max=mediate_state["glucose"]["max"]["value"],
        glucose_timestamp=mediate_state["glucose"]["max"]["timestamp"],
        patient_threshold_glucose_max=patient_data["bg_threshold"]["threshold_max"],
    )


def get_elevated_percen(measurements: pl.DataFrame, threshold: int) -> int:

    above_threshold = measurements.filter(measurements[BPressure.GLUCOSE] > threshold)
    return (above_threshold.shape[0] / measurements.height) * 100
