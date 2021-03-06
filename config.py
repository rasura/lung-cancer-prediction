import os

# The path points to the original images and is
# used if a preprocessing step needs to be executed
ALL_IMGS = 'D:/stage1'

LABELS_INPUT_DIR = './input'

PATIENT_LABELS_CSV = LABELS_INPUT_DIR + '/stage1_labels.csv'
TEST_PATIENTS_IDS = LABELS_INPUT_DIR + '/stage1_sample_submission.csv'

VALIDATION_PATINETS_IDS = LABELS_INPUT_DIR + '/validation_data.csv'
TRAINING_PATIENTS_IDS = LABELS_INPUT_DIR + '/training_data.csv'

MODELS_STORE_DIR = './models'
SOLUTION_FILE_PATH = './solution_last.csv'
REAL_SOLUTION_CSV = './input/stage1_solution.csv'
RESTORE_MODEL_CKPT = 'model_best_sensitivity.ckpt'
SUMMARIES_DIR = './summaries/model_summary'
RESTORE = False
START_STEP = 1

COLUMN_NAME = 'cancer'
ID_COLUMN_NAME = 'id'

CANCER_CLS = 1
NO_CANCER_CLS = 0

# Image properties
OUT_SCAN = -2000
MIN_BOUND = -1000.0
MAX_BOUND = 400.0

BACKGROUND = 0
BATCH_SIZE = 1
NUM_CHANNELS = 1
N_CLASSES = 2

# Preprocessing options used for the defined models
BASELINE_PREPROCESS = 0
MORPHOLOGICAL_OPERATIONS = 1
WATERSHED = 2

FETCHED_DATA_DIR = './fetch_data'

# Configuration for the buckets with preprocessed images
# to download the data from
bucket_names = {
    BASELINE_PREPROCESS: 'baseline-preprocess',
    MORPHOLOGICAL_OPERATIONS: 'segmented-lungs',
    WATERSHED: 'segmented-lungs-watershed'  
}

# construct the path using the object name in the buckets, since
# by default images are stored in directories with the object name
preprocessed_imgs = {
    BASELINE_PREPROCESS: os.path.join(FETCHED_DATA_DIR, 'baseline_preprocessing'),
    MORPHOLOGICAL_OPERATIONS: os.path.join(FETCHED_DATA_DIR, 'segmented_morph_op'),
    WATERSHED: os.path.join(FETCHED_DATA_DIR, 'segmented_watershed')  
}


# Defined models
BASELINE = 'baseline'
BASELINE_WITH_SEGMENTATION = 'baseline_with_segmentation'
NO_REGULARIZATION = 'no_regularization'
NO_REGULARIZATION_WATERSHED = 'no_regularization_watershed'
DROPOUT_L2NORM_REGULARIZARION = 'with_regularization'
REGULARIZATION_MORE_SLICES = 'regularization_more_slices'
WITH_DATA_AUGMENTATION = 'more_slices_augmentation'


model_to_img_shape = { 
    BASELINE: (100, 128, 128),
    BASELINE_WITH_SEGMENTATION: (100, 128, 128),
    NO_REGULARIZATION: (140, 256, 256),
    NO_REGULARIZATION_WATERSHED: (140, 256, 256),
    DROPOUT_L2NORM_REGULARIZARION: (140, 256, 256),
    REGULARIZATION_MORE_SLICES: (180, 256, 256),
    WITH_DATA_AUGMENTATION: (180, 256, 256)
}

model_to_preprocessing = {
    BASELINE: BASELINE_PREPROCESS,
    BASELINE_WITH_SEGMENTATION: MORPHOLOGICAL_OPERATIONS,
    NO_REGULARIZATION: MORPHOLOGICAL_OPERATIONS,
    NO_REGULARIZATION_WATERSHED: WATERSHED,
    DROPOUT_L2NORM_REGULARIZARION: WATERSHED,
    REGULARIZATION_MORE_SLICES: WATERSHED,
    WITH_DATA_AUGMENTATION: WATERSHED
}

# This configuration must be changed in order to select other
# predefined model for training
SELECTED_MODEL = WITH_DATA_AUGMENTATION

SEGMENTATION_ALGO = model_to_preprocessing.get(SELECTED_MODEL, 
    model_to_preprocessing[WITH_DATA_AUGMENTATION]) 

IMG_SHAPE = model_to_img_shape.get(SELECTED_MODEL, 
                                   model_to_img_shape[WITH_DATA_AUGMENTATION])

SLICES, IMAGE_PXL_SIZE_X, IMAGE_PXL_SIZE_Y = IMG_SHAPE

SEGMENTED_LUNGS_DIR = preprocessed_imgs[SEGMENTATION_ALGO]

BUCKET_IN_USE = bucket_names[SEGMENTATION_ALGO]

REQUIRED_IMGS_COUNT = 1595

# Google cloud API client related
# Use for downloading preprocessed images from the
# cloud buckets
PROJECT_NAME = 'lung-cancer-tests'
CREDENTIALS_DIR = './fetch_data'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  os.path.join(CREDENTIALS_DIR,
    'lung-cancer-tests-168b7b36ab99.json')