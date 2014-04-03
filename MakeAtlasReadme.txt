Input files:

CASES: List of cases to process. The files must have the following structure: {dir}/{case}/{subdirectory}/{case}{suffix}
dir: directory in which the cases are
INPUT_SUB_DIR: subdirectory in the case diretory. If none, set it to .
DTI_SUFFIX: Suffix of the DTI image, if scalar images, set to ''
TRANSFORM_SUFFIX: Only used for DTI images. If set to '', not used. Set DTI_SUFFIX accordingly (Not used for scalar images)
ATLAS_DIR: Directory in which to find a template and a corresponding parcellation map. This will be use to warp the parcellation map to the newly computed template.
ATLAS_INPUT_SUFFIX: Input suffix of files used to create new template
TEMPLATE: template file name
PARCELLATION_FILE_NAME: parcellation (atlas) file name
IMAGE_GRID: If images were scaled to 1,1,1, name of the grid file.

Options:

IS_SCALAR: TRUE if the input images are scalar images. FALSE if they are DTIs
IS_SCALED: If the transform given was computed with image spacing set to 1,1,1 and centered, set to TRUE (Not used for scalar images)
RESCALE_CENTER_VERSION: In case of a rescaling: OLD (to use with Shonagh's pipeline, NEW: To use with DWIResamplingSlicer3Module if scaling option is activated
extension: Output and temporary files extension
TRANSF_TYPE: 0 for a fluid transformation, 1 for a B-Splines transformation

Output files:

PROCESS_SUBDIR: Subdirectory in the case directory in which to save new case files (mask and parcellation)
outputDir: Directory in which the computed atlas and atlas parcellation are saved.
_hFieldToAtlas.mha: Suffix of the hField that transforms the input image to the new atlas space
NEW_MASK_TAG: Suffix of the mask created from the segmentation

Temporary files:

tempDir: Directory in which all the temporary files are stored

Processus:

Sets some variables with 010SetUp.bms
For each case, the mask is applied to the input image to create a skull-stripped image.
All cases are registered to the first case (fixed image):
	-First, the intensity of the fixed image is rescaled so that its values are between 0 and 10000
	-Then each case is histogram match to the fixed image
	-Each case is affinely registered to the fixed image
An average image is computed from all the affinely registered images
All the cases are registered to the average image (same process as just described)
An atlas is computed using GreedyAtlas:
	-The input images are the histogram matched images (not affinely transformed)
	-We give the list of affine transforms to GreedyAtlas
	-GreedyAtlas creates an average image and hFields to transform each case to this average image
We save each hField in its corresponding case directory
If the input images are DTIs:
	We compute the average of the DTIs
	We compute the scalar images (MD, FA, colorFA, RD, AD) from the mean DTI
If the input images are scalar images:
	We compute the average image from the scalar images before they are histogram matched
We register the new atlas (if scalar images) or the new MD image (if DTIs) to an old atlas (affinely and fluidly) to transform the parcellation map to the new atlas space.

