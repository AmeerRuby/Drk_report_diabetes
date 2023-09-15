from drk_report_helpers.primitives.Diabetes import outlier, slope_bg, threshold, variations
from drk_report_helpers.utils.typings_diabetes import MediateState, PatientData


def get_args(patient_data: PatientData, mediate_state: MediateState) -> dict:

    return dict(
        num_measurement_days=mediate_state["num_measurement_days"],
        elevated_percen=threshold.get_args(patient_data, mediate_state)["elevated_percen"],
        has_outliers=outlier.get_args(patient_data, mediate_state["bg_measurements"])["has_outliers"],
        slopes=slope_bg.get_args(mediate_state)["slopes"],
        range=variations.get_args(mediate_state)["range"],
        deviation=variations.get_args(mediate_state)["deviation"],
    )
