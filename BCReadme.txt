Input files:

CASES: List of cases to process. The files must have the following structure: {dir}/{case}/{subdirectory}/{case}{suffix}
dir: directory in which the cases are
INPUT_SUB_DIR: subdirectory in the case diretory. If none, set it to .
BIAS_INPUT_SUFFIX: Suffix of the input cases

Options:
extension: Extension of the output files

Output files:

PROCESS_SUBDIR: Directory in which the output files are stored (mask and ABC bias corrected image). {dir}/{case}/{PROCESS_SUBDIR}
OUTPUT_TAG: Suffix of the bias corrected image

Processus:

Applies ITKBiasFieldCorrection to correct the bias in the images. Save the result in the selected subdirectory.
The only parameter that is not set to default is: --bsplineorder 4
