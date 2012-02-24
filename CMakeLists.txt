cmake_minimum_required(VERSION 2.8)
CMAKE_POLICY(VERSION 2.8)

project(MakeAtlasScripts)


set( listTools
DWIProcessPipeline
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
buildtemplateparallel.sh
)

#Find tools
foreach( var ${listTools} )
  find_program(${var}TOOL ${var} )
  if(NOT ${var}TOOL )
    message( WARNING "${var} not found. Its path is not set" )
  endif(NOT ${var}TOOL )
  mark_as_advanced( ${var}TOOL )
endforeach( var )

mark_as_advanced( CMAKE_BUILD_TYPE CMAKE_INSTALL_PREFIX )
set( ConfigDirectory "${CMAKE_CURRENT_BINARY_DIR}" CACHE PATH "Config directory" )

Set( ProcessingDir "${CMAKE_CURRENT_SOURCE_DIR}/.." CACHE PATH "Processing directory" )
set( ProjectDirectory "${CMAKE_CURRENT_SOURCE_DIR}/../../" CACHE PATH "Project directory" )
set( InputType "scalar" CACHE STRING "scalar/DWI/DTI" )
if( NOT( ${InputType} STREQUAL scalar )
    AND NOT( ${InputType} STREQUAL DWI )
    AND NOT( ${InputType} STREQUAL DTI )
  )
  message( FATAL_ERROR "InputType must be either scalar or DWI or DTI" )
endif()

set( ConfigVersion 2.04 )

if( ${InputType} STREQUAL scalar )
  set(InputSuffix .nhdr )
  set(RigidRegistrationImageSuffix .nhdr )
  set(IsScalar TRUE )
  set(AtlasInputSuffix .nhdr )
  set(DTISuffix '' )
  set(TransformSuffix '' )
  set(TransformSuffixAverage '' )
  set(StatFileSuffix _reg.nrrd )
  set(WarpInputSuffix _reg.nrrd )
  set(TemplateImage AverageImage_SS.nrrd )
endif()

if( ${InputType} STREQUAL DWI )
  set(InputSuffix _dwi.nhdr )
  set(RigidRegistrationImageSuffix _idwi_toTemplate.nhdr )
  set(IsScalar FALSE )
  set(AtlasInputSuffix _dti_f_toTemplate_MD.nhdr )
  set(DTISuffix _dti_f.nhdr )
  set(TransformSuffix _toTemplateCombined.txt )
  set(TransformSuffixAverage _toTemplate.txt )
  set(StatFileSuffix _dti_f_reg_AD.nrrd _dti_f_reg_FA.nrrd _dti_f_reg_MD.nrrd _dti_f_reg_RD.nrrd _b0_biasCorrected_reg.nrrd _idwi_biasCorrected_reg.nrrd )
  set(WarpInputSuffix _dti_f_toTemplate_MD.nhdr )
  set(TemplateImage AverageTensor_SS_MD.nrrd )
endif()

if( ${InputType} STREQUAL DTI )
  set(InputSuffix _dti_f.nhdr )
  set(RigidRegistrationImageSuffix _MD_toTemplate.nhdr )
  set(IsScalar FALSE )
  set(AtlasInputSuffix _dti_f_toTemplate_MD.nhdr )
  set(DTISuffix _dti_f.nhdr )
  set(TransformSuffix _toTemplateCombined.txt )
  set(StatFileSuffix _dti_f_reg_AD.nrrd _dti_f_reg_FA.nrrd _dti_f_reg_MD.nrrd _dti_f_reg_RD.nrrd )
  set(WarpInputSuffix _dti_f_toTemplate_MD.nhdr )
  set(TemplateImage AverageTensor_SS_MD.nrrd )
endif()

FILE(GLOB config_files "${CMAKE_CURRENT_SOURCE_DIR}/Config/*.bms.in")

if( DEFINED oldProcessingDir )
else( DEFINED oldProcessingDir )
  set( oldProcessingDir "notdefined" CACHE INTERNAL "oldProcessDir" FORCE )
endif()

if( NOT( ${ProcessingDir} STREQUAL ${oldProcessingDir} ) )
  FILE(GLOB casesGlob "${ProcessingDir}/*")
  set( casesValues "" )
  foreach( var ${casesGlob} )
    string(REGEX REPLACE ".*/" "" var ${var} )
    if( NOT(
         ( ${var} MATCHES ".*\\..*" )
      OR ( ${var} MATCHES "[cC]onfig.*" )
      OR ( ${var} MATCHES "[tT]emp.*" )
      OR ( ${var} MATCHES ".*[tT][oO][oO][lL][sS].*" )
      OR ( ${var} MATCHES ".*[aA][tT][Ll][aA][sS].*" )
         )
      )
      set( casesValues "${var} ${casesValues}" )
    endif()
  endforeach( var )
  Set( cases ${casesValues} )
  set( oldProcessingDir ${ProcessingDir} CACHE INTERNAL "oldProcessDir" FORCE)
  Set( cases ${casesValues} CACHE STRING "cases to process" FORCE)
endif()

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
