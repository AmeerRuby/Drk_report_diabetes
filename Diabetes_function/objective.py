import polars as pl

from drk_report_helpers.primitives.Diabetes import last_measurement
from drk_report_helpers.utils.typings_diabetes import BPressure, MediateState, PatientData


def get_args(patient_data: PatientData, mediate_state: MediateState) -> dict:
    bg_measurements = mediate_state["bg_measurements"]
    last = last_measurement.get_args(mediate_state)

    if patient_data.get("bg_threshold").get("threshold_max") is not None:
        bg = percen_above_threshold(bg_measurements[BPressure.GLUCOSE], patient_data["bg_threshold"]["threshold_max"])
        bg_threshold_max = patient_data.get("bg_threshold").get("threshold_max")
    else:
        bg = 0.0
        bg_threshold_max = 0

    threshold_min_70 = 70

    # Check if there is a threshold for blood glucose < 70 mg/dL
    if patient_data.get("bg_threshold").get("threshold_min_70") is not None:
        bg_below_70 = percen_below_threshold(bg_measurements[BPressure.GLUCOSE], patient_data["bg_threshold"]["threshold_min_70"])
    else:
        bg_below_70 = 0.0
    return dict(
        last=last,
        percen_above=dict(blood_glucose=bg),
        percen_below=dict(blood_glucose_below_70=bg_below_70),
        num_measurement_days=mediate_state["num_measurement_days"],
        bg_threshold_max=bg_threshold_max,
    )


def percen_above_threshold(measurements: pl.Series, threshold_max: int):
    return (measurements > threshold_max).sum() / len(measurements)


def percen_below_threshold(measurements: pl.Series, threshold_min: int):
    return (measurements < threshold_min).sum() / len(measurements)
