from typing import List

import polars as pl

from drk_report_helpers.constraints import default
from drk_report_helpers.utils.typings_diabetes import BPressure, PatientData


def get_args(patient_data: PatientData, bg_measurements: pl.DataFrame) -> bool:

    if patient_data.get("bg_threshold").get("threshold_max") is None:
        return dict(has_outliers=False, bg_threshold_max=0)

    return dict(
        has_outliers=has_outliers(
            bg_measurements[BPressure.GLUCOSE].to_list(),
            patient_data["bg_threshold"]["threshold_max"],
        ),
        bg_threshold_max=patient_data["bg_threshold"]["threshold_max"],
    )


def has_outliers(bg_measurements: List[int], threshold) -> bool:

    temp = default.default()["OUTLIER_CNT_THRESHOLD"]
    glucose_greater_than_180 = 0
    glucose_greater_than_140_less_than_180 = 0
    glucose_greater_than_140 = 0
    glucose_less_than_100 = 0

    for glucose in bg_measurements:
        if glucose > 180:
            glucose_greater_than_180 += 1
        elif 140 < glucose <= 180:
            glucose_greater_than_140_less_than_180 += 1
        elif glucose > 140:
            glucose_greater_than_140 += 1
        elif glucose < 100:
            glucose_less_than_100 += 1

        if glucose > threshold + default.default()["OUTLIER_CNT_THRESHOLD"]:
            temp -= 1

        if temp == 0:
            return True

    total_measurements = len(bg_measurements)
    glucose_180_percentage = glucose_greater_than_180 / total_measurements
    glucose_140_180_percentage = glucose_greater_than_140_less_than_180 / total_measurements
    glucose_140_percentage = glucose_greater_than_140 / total_measurements
    glucose_100_percentage = glucose_less_than_100 / total_measurements

    result = {
        "glucose_greater_than_180_reading_80_percent": glucose_180_percentage >= 0.8,
        "glucose_greater_than_140_less_than_180_reading_80_percent": glucose_140_180_percentage >= 0.8,
        "glucose_greater_than_140_reading_30_percent": glucose_140_percentage >= 0.3,
        "glucose_less_than_100_reading_30_percent": glucose_100_percentage >= 0.3,
    }

    if temp == 0:
        result["has_outliers"] = True
        result["outliers"] = {
            "blood_glucose_less_than_100": glucose_less_than_100 > 0,
            "blood_glucose_greater_than_300": glucose_greater_than_180 > 0,
        }
    else:
        result["has_outliers"] = False
        result["outliers"] = {}

    return result
