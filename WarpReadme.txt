Input files:

CASES: List of cases to process. The files must have the following structure: {dir}/{case}/{subdirectory}/{case}{suffix}
dir: directory in which the cases are
INPUT_SUB_DIR: subdirectory in the case diretory. If none, set it to .
AtlasDir: Directory in which the atlas and atlas parcellation are saved
Template_Image: Name of the template image used for registration
tempDir: Directory in which all the temporary files are stored
WARP_INPUT_SUFFIX: suffix and extension of the image to use for the registration
LabelMapsToWarp: List of images to warp. You can warp a parcellation map, a cortical thickness mask,...
  ie:${AtlasDir}/template_atlas.nrrd ${AtlasDir}/corticalthickness.nrrd
STAT_FILE_SUFFIX: Image files on which to compute statistics. Can contain multiple files.
NEW_MASK_TAG: Suffix of the mask created from the segmentation. The file must be in {dir}/{case}/${PROCESS_SUBDIR}
PROCESS_SUBDIR: subdirectory in the case directory in which the mask image is. New files will be saved in this directory.

Options:
extension: Extension of the output files

Output files:
PROCESS_SUBDIR: subdirectory in the case directory in which to save new case files (mask, parcellation and statistics). The image mask must be in this directory too.

Processus:
For each case:
	-Apply the brain mask on the image
	-Histogram match the case image with the atlas
	-Register affinely the case (fixed image) with the atlas (moving image)
	-Compute deformation field to transform atlas to image case
	-For each image to warp:
		-Warp image using computed deformation field
		-Computed statistics on the warped image
