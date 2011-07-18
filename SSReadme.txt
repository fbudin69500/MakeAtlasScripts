Input files:

CASES: List of cases to process. The files must have the following structure: {dir}/{case}/{subdirectory}/{case}{suffix}
dir: directory in which the cases are
INPUT_SUB_DIR: subdirectory in the case diretory. If none, set it to .
RIGID_REGISTRATION_IMAGE_SUFFIX: suffix and extension of the image to use for the registration
ABC_IMAGE_SUFFIX: suffix of the image used by ABC to compute the tissue segmentation (EM segmentation). It may contain multiple suffixes, separated by a space
ATLAS_DIR: Directory in which the atlas files are stored
ATLAS_FILES: Name of the atlas files. One of them should be called template.*

Options:

IS_SCALAR: option to set if the image is a scalar image or a DTI image. For this skull-stripping script, it makes the MD_TAG and the FA_TAG irrelevant if set to FALSE. The image used for registration has to be integers. If the RIGID_REGISTRATION_IMAGE_SUFFIX matches either the MD_TAG or the FA_TAG, it multiplies it 
MD_SUFFIX: Suffix of the MD image. Useless if the image used for the registration is not derived from a DTI, but must be not empty
FA_SUFFIX: Same as above but for FA
IS_SCALED: Was the input image scaled to 1,1,1. If set to TRUE, ATLAS_GRID must be set to the grid that was computed to upscale the atlas.
sequence(seq 0 0 1): Change le next to the last number to change the number of loops (ie. sequence(seq 0 NB_LOOPS 1) ). If NB_LOOPS > 0 , a first mask will be computed, then it will be applied to the original image to process the image again and try to find a better mask.
ATLAS_GRID: Set if the image has been upscaled (spacing set to 1,1,1, IS_SCALAR set to TRUE). This should contain the name of the grid image that was used to make the atlas isotropic before being upscaled
CONFIGDIR: directory that contains the scripts
MASK_CLOSING_RADIUS: Closing radius to smooth mask computed from segmentation
extension: Extension of the output files
ABCSUFFIX: suffix of segmentation files (temporary files)
PRIORS: Priors used by ABC. The number of priors should match the number of probability maps.

Output files:

PROCESS_SUBDIR: Directory in which the output files are stored (mask and ABC bias corrected image). {dir}/{case}/{PROCESS_SUBDIR}
NEW_MASK_TAG: suffix of the mask created from the segmentation. The file will be saved in {PROCESS_SUBDIR}
{Case}{First_SUFFIX_in ABC_SUFFIX_list}_corrected.{extension}: bias corrected image by ABC
{Case}{NEW_MASK_TAG}.{extension}: Mask

Temporary files:

tempDir: Directory in which all the temporary files are stored
If image not upscaled: All template and probability map files are copied and converted in gipl.gz in the temporary directory
All other temporary images are saved under a subdirectory with the case name.
{Case}{RIGID_REGISTRATION_IMAGE_TAG}.gipl.gz: image used for rigid registration is converted to gipl.gz
{Case}{RIGID_REGISTRATION_IMAGE_TAG}_hm{i}.gipl.gz: i is the loop number. Histogram match image with the template
{Case}_rigid{i}.dof: rigid transformation file (from case to template)
{Case}{RIGID_REGISTRATION_IMAGE_TAG}_rigid{i}.gipl.gz: Rigidly aligned file
{Case}_affine{i}.dof: affine transformation (from template to rigidly aligned image)
{ATLAS_TAG}.gipl.gz: template and probability maps tranformed to the case space (rigid and affine transformation)
{Case}{First_SUFFIX_in ABC_SUFFIX_list}_labels_{ABCSUFFIX}.${extension}: tissue segmentation image. Output image of ABC
{Case}{NEW_MASK_TAG}_orig{i}.{extension}: i is the loop number. Brain mask computed from the output of ABC, before smoothing
{Case}{NEW_MASK_TAG}_eroded{i}.{extension}: i is the loop number. Eroded brain mask
{Case}{NEW_MASK_TAG}{i}.${extension}: Brain mask after i loops

Processus:

Sets some variables with 010SetUp.bms 
If the image is not scaled, prepares the atlas images, converting them into gipl.gz for the registration program [021PrepareGeneral.bms]
Then, for each case:
	-Sets the case image up (convert them to gipl.gz, convert them to integer images) [022PrepareCases.bms]
	-If the image was rescaled, rescaled the atlas images [022PrepareCases.bms]
	-histogram match case image and template [023CaseAlign.bms]
	-registers rigidly case image to template [023CaseAlign.bms]
	-affine registration of the template to the rigidly transformed case [023CaseAlign.bms]
	-transformation of all the atlas files with both rigid (invert) and affine transform [023CaseAlign.bms]
	-Creation of an ABC xml file [024genABC]
	-Runs ABC [000SkullStrip.bms]
	-Creates mask from tissue segmentation [000SkullStrip.bms]
	-erodes and dilates mask to smooth it [000SkullStrip.bms]
	-Copy final results in case directory


