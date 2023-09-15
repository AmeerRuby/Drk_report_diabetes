from drk_report_helpers.utils.typings_diabetes import PatientData


def get_args(patient_data: PatientData) -> dict:

    symptoms_list = patient_data["symptoms_data"]
    dmp = list(patient_data["symptoms_data"].keys())
    age = patient_data["age"]
    gender = patient_data["gender"]

    is_dmp = set(dmp).intersection(set(["Type 1", "Type 2"]))

    return dict(symptoms_list=symptoms_list, is_dmp=is_dmp, age=age, gender=gender.lower())
