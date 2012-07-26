cmake_minimum_required(VERSION 2.8)
CMAKE_POLICY(VERSION 2.8)

project(MakeAtlasScripts NONE)

if( DEFINED TemplateDirectory )
  set( templatePathDefinedInline TRUE )
else()
  set( templatePathDefinedInline FALSE )
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
set(InputFile *.nhdr CACHE STRING "input image in 1-Converted, ie: *_T1.nrrd; *
will be replaced by the case name. It is not compulsary" )
get_filename_component( InputTag ${InputFile} NAME_WE )
if( ${InputTag} MATCHES "\\*" )
  set( rootName ${InputTag} )
else()
  set( rootName "*_${InputTag}" )
endif()
###########################Version of the pipeline############################################
set( ConfigVersion 3.00 )
###########################set variables values depending on project type######################
if( ${InputType} STREQUAL scalar )
  set(RigidRegistrationImageFile ${rootName}_reg.nrrd )
  set(IsScalar TRUE )
  set(PopulationAverageInputFiles ${rootName}_reg.nrrd )
  set(Original_Image ${InputFile} )
  set(TransformFile ${rootName}_reg.mat )
  set(StatFile ${rootName}_reg.nrrd )
  set(WarpInputFile ${rootName}_reg.nrrd )
  set(PopulationAverage AverageImage_SS.nrrd )
  set(AverageInputFile @ProcessingDirectory@/*/2-Registration/${rootName}_reg.nrrd )
  set(HISTOGRAM_MATCH_VAL TRUE )
endif()

if( ${InputType} STREQUAL DWI )
  set(PopulationAverage AverageTensor_SS_MD.nrrd )
  set(RigidRegistrationImageFile ${rootName}_idwi_biasCorrected_reg.nrrd )
  set(IsScalar FALSE )
  set(PopulationAverageInputFiles ${rootName}_dti_f_reg_MD.nrrd )
  set(Original_Image ${rootName}_dti_f_reg.nrrd )
  set(TransformFile ${rootName}_reg.mat )
  set(StatFile "${rootName}_reg_AD.nrrd ${rootName}_dti_f_reg_FA.nrrd ${rootName}_dti_f_reg_MD.nrrd ${rootName}_dti_f_reg_RD.nrrd ${rootName}_b0_biasCorrected_reg.nrrd ${rootName}_idwi_biasCorrected_reg.nrrd" )
  set(WarpInputFile ${rootName}_dti_f_reg_MD.nrrd )
  set(TemplateImage AverageTensor_SS_MD.nrrd )
  set(AverageInputFile "@ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_AD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_FA.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_MD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_dti_f_reg_RD.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_b0_biasCorrected_reg.nrrd @ProcessingDirectory@/*/2-Registration/${rootName}_idwi_biasCorrected_reg.nrrd" )
  set(HISTOGRAM_MATCH_VAL "FALSE FALSE FALSE FALSE FALSE FALSE" )
endif()

if( ${InputType} STREQUAL DTI )
  set(PopulationAverage AverageTensor_SS_MD.nrrd )
  set(RigidRegistrationImageFile ${rootName}_reg_MD.nrrd )
  set(IsScalar FALSE )
  set(PopulationAverageInputFiles ${rootName}_reg_MD.nrrd )
  set(Original_Image ${InputFile} )
  set(TransformFile ${rootName}_reg.mat )
  set(StatFile "${rootName}_reg_AD.nrrd ${rootName}_reg_FA.nrrd ${rootName}_reg_MD.nrrd ${rootName}_reg_RD.nrrd" )
  set(WarpInputFile ${rootName}_reg_MD.nrrd )
  set(TemplateImage AverageTensor_SS_MD.nrrd )
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
  set( ExternalSegmentation "${TemplateDirectory}/segmentation.nrrd" CACHE FILEPATH "External segmentation file" FORCE )
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

