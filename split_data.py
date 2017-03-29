import os
import numpy as np
import random as rnd
import pandas as pd

import input_dicoms as ind
import compress_dicoms as cd


LABELS_INPUT_DIR = cd.INPUT_DIR + '/input/stage1_labels.csv'
EXACT_TEST_IDS = cd.INPUT_DIR + '/input/stage1_sample_submission.csv'
COLUMN_NAME = 'cancer'
VALIDATION_IDS = cd.INPUT_DIR + '/input/validation_data.csv'
TRAINING_IDS = cd.INPUT_DIR + '/input/training_data.csv'
ALL_IMGS = 'D:/Fil/stage1'

CANCER_CLS = 1
NO_CANCER_CLS = 0


def load_labels():
    return ind.read_csv(LABELS_INPUT_DIR)


def load_test_ids():
    return ind.read_csv_column(EXACT_TEST_IDS)


def get_patient_name(patient_file):
    return os.path.basename(patient_file).split('.')[0]


def load_patient_ids():
    test_ids = set(load_test_ids())
    patient_ids = [get_patient_name(patient_id)
                   for patient_id in os.listdir(ALL_IMGS)
                   if get_patient_name(patient_id) not in test_ids]
                   
    return patient_ids

def get_class(labels, patient_id):
    return labels.get_value(patient_id, COLUMN_NAME)


def count_patients_from_class(patient_ids, labels, clazz):
    return len([patient for patient in patient_ids 
                if get_class(labels, patient) == clazz])


def store_to_csv(patients, labels, csv_file_path):
    df = pd.DataFrame(data={'id': patients, 'cancer': labels}, 
                      columns=['id', 'cancer'])
    df.to_csv(csv_file_path)


def split_data():
    labels = load_labels()
    total = len(labels)
    print("Total labels loaded: ", total)
    patient_ids = load_patient_ids()
    print("Total patient ids loaded: ", len(patient_ids))
    print("Patient with cancer are: ", count_patients_from_class(patient_ids, labels, CANCER_CLS))

    validation_size = int(0.15 * total)

    validation_set = rnd.sample(patient_ids, validation_size)
    train_set = [patient for patient in patient_ids if patient not in validation_set]

    print("Patients for training: ", len(train_set))
    print("Patients for validation: ", len(validation_set))

    print("Patients with cancer in validation set {}, no cancer {}.".format(
        count_patients_from_class(validation_set, labels, CANCER_CLS),
        count_patients_from_class(validation_set, labels, NO_CANCER_CLS)))
    print("Patients with cancer in training set {}, no cancer {}.".format(
        count_patients_from_class(train_set, labels, CANCER_CLS),
        count_patients_from_class(train_set, labels, NO_CANCER_CLS)))

    validation_labels = [get_class(labels, p) for p in validation_set]
    store_to_csv(validation_set, validation_labels, VALIDATION_IDS)
    
    train_labels = [get_class(labels, p) for p in train_set]
    store_to_csv(train_set, train_labels, TRAINING_IDS)


if __name__ == '__main__':
    split_data()
