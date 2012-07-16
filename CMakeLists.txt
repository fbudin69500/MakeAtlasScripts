cmake_minimum_required(VERSION 2.8)
CMAKE_POLICY(VERSION 2.8)

project(MakeAtlasScripts NONE)


set( listTools
DWIProcessPipeline
ABC
SegPostProcessCLP
ImageMath
ResampleVolume2
#rreg
#transformation
#areg
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
buildtemplateparallel.sh
dtiestim
ManualImageOrient
DiffusionTensorEstimation
HistogramMatching
CreateMRML
N4ITKBiasFieldCorrection
MaskComputationWithThresholding
)

set( ToolsDirectory "/rodent/bin_linux64/toolsApril2012" CACHE PATH "Tools
directory")

#Find tools
foreach( var ${listTools} )
  find_program(${var}TOOL ${ToolsDirectory}/${var} )
  if(NOT ${var}TOOL )
    find_program(${var}TOOL ${var})
    if(${var}TOOL)
    message( WARNING "${var} was not in ${ToolsDirectory}.  The path was set
to the dynamic executable path set as default on your machine")
#    endif(${var}TOOL)
    else(${var}TOOL )
        message( WARNING "${var} not found. Path not set")
    endif(${var}TOOL)
  endif(NOT ${var}TOOL )
  mark_as_advanced( ${var}TOOL )
endforeach( var )

mark_as_advanced( CMAKE_BUILD_TYPE CMAKE_INSTALL_PREFIX )
set( ConfigDirectory "${CMAKE_CURRENT_BINARY_DIR}" CACHE PATH "Config directory" )

get_filename_component(initProcessingDirectory ${CMAKE_CURRENT_SOURCE_DIR}/.. REALPATH )
Set( ProcessingDirectory "${initProcessingDirectory}" CACHE PATH "Processing directory" )


set( ResultsSubDirectory Results CACHE STRING "Results subdirectory" )
mark_as_advanced( ResultsSubDirectory )
set( InputPostSubDirectory . CACHE STRING "Input Post subdirectory" )
mark_as_advanced( InputPostSubDirectory )




set( InputType "scalar" CACHE STRING "scalar/DWI/DTI" )
if( NOT( ${InputType} STREQUAL scalar )
    AND NOT( ${InputType} STREQUAL DWI )
    AND NOT( ${InputType} STREQUAL DTI )
  )
  message( FATAL_ERROR "InputType must be either scalar or DWI or DTI" )
endif()

set( ConfigVersion 2.2 )

if( ${InputType} STREQUAL scalar )
  set(InputSuffix .nhdr )
  set(RigidRegistrationImageSuffix .nhdr )
  set(IsScalar TRUE )
  set(PopulationAverageInputSuffix .nhdr )
  set(DTISuffix '' )
  set(TransformSuffix '' )
  set(TransformSuffixAverage '' )
  set(StatFileSuffix _reg.nrrd )
  set(WarpInputSuffix _reg.nrrd )
  set(PopulationAverage AverageImage_SS.nrrd )
  set(AverageInputSuffix .nhdr )
  set(HISTOGRAM_MATCH_VAL TRUE )
endif()

if( ${InputType} STREQUAL DWI )
  set(PopulationAverage AverageTensor_SS.nrrd )
  set(InputSuffix _dwi.nhdr )
  set(RigidRegistrationImageSuffix _idwi_biasCorrected.nrrd )
  set(IsScalar FALSE )
  set(PopulationAverageInputSuffix _dti_f_reg_MD.nhdr )
  set(DTISuffix _dti_f.nhdr )
  set(TransformSuffix _toTemplateCombined.txt )
  set(StatFileSuffix "_dti_f_reg_AD.nrrd _dti_f_reg_FA.nrrd _dti_f_reg_MD.nrrd _dti_f_reg_RD.nrrd _b0_biasCorrected_reg.nrrd _idwi_biasCorrected_reg.nrrd" )
  set(WarpInputSuffix _dti_f_toTemplate_MD.nhdr )
  set(TemplateImage AverageTensor_SS_MD.nrrd )
  set(AverageInputSuffix "_dti_f_reg_AD.nrrd _dti_f_reg_FA.nrrd _dti_f_reg_MD.nrrd _dti_f_reg_RD.nrrd _b0_biasCorrected_reg.nrrd _idwi_biasCorrected_reg.nrrd" )
  set(HISTOGRAM_MATCH_VAL FALSE FALSE FALSE FALSE FALSE FALSE )
endif()

if( ${InputType} STREQUAL DTI )
  set(PopulationAverage AverageTensor_SS.nrrd )
  set(InputSuffix _dti_f.nhdr )
  set(RigidRegistrationImageSuffix _dti_f_reg_MD.nrrd )
  set(IsScalar FALSE )
  set(PopulationAverageInputSuffix _dti_f_reg_MD.nrrd )
  set(DTISuffix _dti_f.nhdr )
  set(TransformSuffix _toTemplateCombined.txt )
  set(StatFileSuffix "_dti_f_reg_AD.nrrd _dti_f_reg_FA.nrrd _dti_f_reg_MD.nrrd _dti_f_reg_RD.nrrd" )
  set(WarpInputSuffix _dti_f_toTemplate_MD.nhdr )
  set(TemplateImage AverageTensor_SS_MD.nrrd )
  set(AverageInputSuffix "_dti_f_reg_AD.nrrd _dti_f_reg_FA.nrrd _dti_f_reg_MD.nrrd _dti_f_reg_RD.nrrd" )
  set(HISTOGRAM_MATCH_VAL "FALSE FALSE FALSE FALSE" )
endif()

FILE(GLOB config_files "${CMAKE_CURRENT_SOURCE_DIR}/Config/*.bms.in")

if( DEFINED oldProcessingDir )
else( DEFINED oldProcessingDir )
  set( oldProcessingDir "notdefined" CACHE INTERNAL "oldProcessDir" FORCE )
endif()

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
  set(TemplateDirectory "${ProcessingDirectory}/template/a-original" CACHE PATH "Template directory" FORCE )
  get_filename_component(changeProjectDirectory ${ProcessingDirectory}/.. REALPATH )
  set( ProjectDirectory "${changeProjectDirectory}" CACHE PATH "Project directory" FORCE )
endif()

get_filename_component(ProcessingDirRealPath ${ProcessingDirectory} REALPATH )
get_filename_component(ProjectDirectoryRealPath ${ProjectDirectory} REALPATH )

file(RELATIVE_PATH ProcessingRelativePath ${ProjectDirectoryRealPath} ${ProcessingDirRealPath} )

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

