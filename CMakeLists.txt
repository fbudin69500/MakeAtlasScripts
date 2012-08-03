cmake_minimum_required(VERSION 2.8)
CMAKE_POLICY(VERSION 2.8)

project(MakeAtlasScripts NONE)

if( DEFINED TemplateDirectory )
  set( templatePathDefinedInline TRUE )
else()
  set( templatePathDefinedInline FALSE )
endif()

if( DEFINED ExternalSegmentation )
  set( segPathDefinedInline TRUE )
else()
  set( segPathDefinedInline FALSE )
endif()


#######################################Tools used######################################
set( listTools
ABC
SegPostProcessCLP
ImageMath
ResampleVolume2
rreg
transformation
areg
RegisterImages
Double2FloatTransform
AtlasWerks
ResampleDTIlogEuclidean
BRAINSDemonWarp
dtiaverage
unu
dtiprocess
ITKTransformTools
MedianImageFilter
ImageStat
ANTS
WarpImageMultiTransform
#buildtemplateparallel.sh
dtiestim
ManualImageOrient
DiffusionTensorEstimation
HistogramMatching
#CreateMRML
N4ITKBiasFieldCorrection
MaskComputationWithThresholding
)

set( ToolsDirectory "/rodent/bin_linux64/toolsJuly2012" CACHE PATH "Tools
directory")

##########################Find tools##############################################
foreach( var ${listTools} )
  find_program(${var}TOOL ${ToolsDirectory}/${var} )
  if(NOT ${var}TOOL )
    find_program(${var}TOOL ${var})
    if(${var}TOOL)
    message( WARNING "${var} was not in ${ToolsDirectory}.  The path was set
 to the dynamic executable path set as default on your machine:
 ${${var}TOOL} ")
    else(${var}TOOL )
        message( WARNING "${var} not found. Path not set")
    endif(${var}TOOL)
  endif(NOT ${var}TOOL )
  mark_as_advanced( ${var}TOOL )
endforeach( var )

mark_as_advanced( CMAKE_BUILD_TYPE CMAKE_INSTALL_PREFIX )
set( ConfigDirectory "${CMAKE_CURRENT_BINARY_DIR}" CACHE PATH "Config directory" )

get_filename_component(initProcessingDirectory ${CMAKE_CURRENT_SOURCE_DIR}/.. REALPATH )
set( ProcessingDirectory "${initProcessingDirectory}" CACHE PATH "Processing directory" )



set( InputType "scalar" CACHE STRING "scalar/DWI/DTI" )
if( NOT( ${InputType} STREQUAL scalar )
    AND NOT( ${InputType} STREQUAL DWI )
    AND NOT( ${InputType} STREQUAL DTI )
  )
  message( FATAL_ERROR "InputType must be either scalar or DWI or DTI" )
endif()
set(InputFile "" CACHE PATH "input image in 1-Converted, ie: /Project/*/1-Converted/*_T1.nrrd; *
will be replaced by the case name. It is not compulsary" )
get_filename_component( InputTag ${InputFile} NAME_WE )
get_filename_component( segmentationTag ${segmentationFile} NAME_WE )
if( ${InputTag} MATCHES "\\*" )
  set( rootName ${InputTag} )
else()
  set( rootName "*_${InputTag}" )
endif()
###########################Version of the pipeline############################################
set( ConfigVersion 3.00 )
set( LabelMapsToWarpFile @ProcessingDirectory@/5-AverageSegmentation/${segmentationTag}.nrrd )
set( LabelMapsTag @ProcessingDirectory@/*/6-Warping/*_${segmentationTag}.nrrd )
set(TransformFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg.mat )
###########################set variables values depending on project type######################
if( ${InputType} STREQUAL scalar )
  set(RigidRegistrationImageFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg.nrrd )
  set(IsScalar TRUE )
  set(PopulationAverageInputFiles @ProcessingDirectory@/*/2-Registration/${rootName}_reg.nrrd )
  set(Original_Image ${InputFile} )
  set(StatFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg.nrrd )
  set(WarpInputFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg.nrrd )
  set(PopulationAverage @ProcessingDirectory@/4-AverageCreation/AverageImage_SS.nrrd )
  set(AverageInputFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg.nrrd )
  set(HISTOGRAM_MATCH_VAL TRUE )
endif()

if( ${InputType} STREQUAL DWI )
  set(PopulationAverage @ProcessingDirectory@/4-AverageCreation/AverageTensor_SS_MD.nrrd )
  set(RigidRegistrationImageFile @ProcessingDirectory@/*/2-Registration/${rootName}_idwi_biasCorrected_reg.nrrd )
  set(IsScalar FALSE )
  set(PopulationAverageInputFiles @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_MD.nrrd )
  set(Original_Image @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f.nrrd )
  set(StatFile "@ProcessingDirectory@/*/2-Registration/${rootName}_reg_AD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_FA.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_MD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_RD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_b0_biasCorrected_reg.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_idwi_biasCorrected_reg.nrrd" )
  set(WarpInputFile @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_MD.nrrd )
  set(TemplateImage @ProcessingDirectory@/4-AverageCreation/AverageTensor_SS_MD.nrrd )
  set(AverageInputFile "@ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_AD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_FA.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_MD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_RD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_b0_biasCorrected_reg.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_idwi_biasCorrected_reg.nrrd" )
  set(HISTOGRAM_MATCH_VAL "FALSE FALSE FALSE FALSE FALSE FALSE" )
endif()

if( ${InputType} STREQUAL DTI )
  set(PopulationAverage @ProcessingDirectory@/4-AverageCreation/AverageTensor_SS_MD.nrrd )
  set(RigidRegistrationImageFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg_MD.nrrd )
  set(IsScalar FALSE )
  set(PopulationAverageInputFiles @ProcessingDirectory@/*/2-Registration/${rootName}_reg_MD.nrrd )
  set(Original_Image ${InputFile} )
  set(StatFile "@ProcessingDirectory@/*/2-Registration/${rootName}_reg_AD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_reg_FA.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_reg_MD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_reg_RD.nrrd" )
  set(WarpInputFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg_MD.nrrd )
  set(TemplateImage @ProcessingDirectory@/4-AverageCreation/AverageTensor_SS_MD.nrrd )
  set(AverageInputFile "@ProcessingDirectory@/*/2-Registration/${rootName}_reg_AD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_reg_FA.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_reg_MD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_reg_RD.nrrd" )
  set(HISTOGRAM_MATCH_VAL "FALSE FALSE FALSE FALSE" )
endif()
#####################################################################################################
FILE(GLOB config_files "${CMAKE_CURRENT_SOURCE_DIR}/Config/*.bms.in")

set( Scale "OFF" CACHE BOOL "Images are scaled to 1,1,1 for registration purposes" )
set( ManualTransform "" CACHE FILEPATH "Manual Transform file To rigidly register the images. No additional registration will be performed" )
set( InitialTransform "" CACHE FILEPATH "Initial Transform file To rigidly register the images. And additional registration will be performed" )
mark_as_advanced( Scale InitialTransform ManualTransform)

if( NOT ManualTransform )
  set( ManualTransformSTRING '' CACHE INTERNAL "" FORCE )
else()
  set( ManualTransformSTRING ${ManualTransform} CACHE INTERNAL "" FORCE )
endif()

if( NOT InitialTransform )
  set( InitialTransformSTRING '' CACHE INTERNAL "" FORCE )
else()
  set( InitialTransformSTRING ${InitialTransform} CACHE INTERNAL "" FORCE )
endif()

if( DEFINED oldProcessingDir )
else( DEFINED oldProcessingDir )
  set( oldProcessingDir "notdefined" CACHE INTERNAL "oldProcessDir" FORCE )
endif()


###########Find the cases in the processing folder########################
###########and configures the path properly########################
if( NOT( ${ProcessingDirectory} STREQUAL ${oldProcessingDir} ) )
  FILE(GLOB casesGlob "${ProcessingDirectory}/*")
  set( casesValues "" )
  foreach( var ${casesGlob} )
    string(REGEX REPLACE ".*/" "" var ${var} )
    if( NOT(
         ( ${var} MATCHES ".*\\..*" )
      OR ( ${var} MATCHES "[cC]onfig.*" )
      OR ( ${var} MATCHES "[tT]emp.*" )
      OR ( ${var} MATCHES ".*[tT][oO][oO][lL][sS].*" )
      OR ( ${var} MATCHES ".*[aA][tT][Ll][aA][sS].*" )
      OR ( ${var} MATCHES ".*[sS][tT][aA][tT][sS].*" )
      OR ( ${var} MATCHES ".*[aA][vV][eE][rR][aA][gG][eE].*" )
         )
      )
      set( casesValues "${var} ${casesValues}" )
    endif()
  endforeach( var )
  set( oldProcessingDir ${ProcessingDirectory} CACHE INTERNAL "oldProcessDir" FORCE)
  Set( cases ${casesValues} CACHE STRING "cases to process" FORCE)
  if( NOT ${templatePathDefinedInline} )
    set(TemplateDirectory "${ProcessingDirectory}/template/a-original" CACHE PATH "Template directory" FORCE )
  endif()
  if( NOT ${segPathDefinedInline} )
    set( ExternalSegmentation "${TemplateDirectory}/segmentation.nrrd" CACHE FILEPATH "External segmentation file" FORCE )
  endif()
endif()

unset( TemplateFile CACHE)
find_file( TemplateFile NAMES template.mha PATHS ${TemplateDirectory} NO_DEFAULT_PATH)
mark_as_advanced( TemplateFile )

if( NOT TemplateFile )
  message( FATAL_ERROR "template.mha not found in specified template directory. Please select another template directory" )
endif()

unset( PRIORS CACHE)
unset( ProbaListFiles CACHE)
unset( last_var )
unset( TemplateDirFile CACHE )
file( GLOB TemplateDirFile ${TemplateDirectory}/*.mha)
list( LENGTH TemplateDirFile size )
if( ${size} GREATER 0 )
  foreach( loop_var RANGE 1 ${size} 1 )
    list( FIND TemplateDirFile "${TemplateDirectory}/${loop_var}.mha" found_var)
    if( ${found_var} LESS 0 )
      math( EXPR last_var ${loop_var}-1 )
      break()
    endif()
  endforeach()
  if( ${last_var} LESS 1 )
    message( FATAL_ERROR "No probability map found" )
  else()
    #we do a second loop that stops at the first file missing. There could be 1.mha, 2.mha and 4.mha. We would only take into account 1.mha and 2.mha
    foreach( loop_var RANGE 1 ${last_var} 1 )
      set( ProbaListFiles "${ProbaListFiles} ${loop_var}.mha" CACHE  STRING "list of probability map files" FORCE)
      set( PRIORS "${PRIORS} 1" CACHE  STRING "list of probability map files" FORCE )
    endforeach()
  endif()
else()
  message( FATAL_ERROR "No file found in specified template directory. Please select another template directory" )
endif()
mark_as_advanced( PRIORS ProbaListFiles TemplateDirFile )


get_filename_component( segmentationFileName ${ExternalSegmentation} NAME )
get_filename_component( segmentationPath ${ExternalSegmentation} PATH )
unset( segmentationFile CACHE)
find_file( segmentationFile NAMES ${segmentationFileName} PATHS ${segmentationPath} NO_DEFAULT_PATH)
mark_as_advanced( segmentationFile )
if( NOT segmentationFile )
  message( WARNING "${ExternalSegmentation} does not exist. Please select another file" )
endif()

##############Writes configured files##############################################
foreach( var ${config_files} )
  string(REPLACE ".bms.in" ".bms" var2 ${var} )
  string(REGEX REPLACE ".*/" "" var2 ${var2} )
  configure_file( "${var}" "${ConfigDirectory}/${var2}" @ONLY )
  get_filename_component(ConfigDirectoryRealPath ${ConfigDirectory} REALPATH )
  get_filename_component(CMAKE_CURRENT_BINARY_DIRRealPath ${CMAKE_CURRENT_BINARY_DIR} REALPATH )
  if( NOT ( ${ConfigDirectoryRealPath} STREQUAL ${CMAKE_CURRENT_BINARY_DIRRealPath} ) )
    file( REMOVE ${CMAKE_CURRENT_BINARY_DIR}/${var2} )
  endif()
endforeach( var )

