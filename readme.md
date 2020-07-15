<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Bone Microstructure vs. Whole Bone Strength Project</h3>

  <p align="center">
   A repository for all of the code for an in process manuscript. 
    <br />
    <a href="https://github.com/daniella-patton/Bone_Micro_Strength/blob/master/readme.md"><strong>Explore the docs »</strong></a>
    <br />
  <a href="https://github.com/daniella-patton/Bone_Micro_Strength">
    <img src="BrokenProxFemur.jpeg" alt="Logo" width="450" height="450">
  </a>
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Overview of the Methods](#Overview-of-the-Methods)
  * [Volume Extraction](#Volume-Extraction)
  * [Installation](#installation)
  * [Image Processing and Volume Extraction](#Image-Processing-and-Volume-Extraction)
  * [Quantification of Cortical and Trabecular Microstructure](#Quantification-of-Cortical-and-Trabecular-Microstructure)
  * [Statistical Analysis](#Statistical-Analysis)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

The work in this project was a product of the work I completed during my PhD thesis. This repository contains all of the code used to run analysis on each proximal femur used in this study. 

The objectives in this study included:
* Identify the cortical and trabecular traits in the femoral neck that best predicts bone strength in males and females
* Determine whether adding progressively more cortical and trabecular structural detail improves strength predictions and whether the additional detail is necessary to explain age and sex-specific differences in bone strength

We hypothesized that both cortical and trabecular parameters contribute to proximal femur strength and that localized regions of the femoral neck would better explain strength compared to measures that are averaged across the femoral neck.  

### Built With
The major framework used for this project include the following: 
* [Dragonfly (ORS)](https://www.theobjects.com/dragonfly/index.html)
* [Rstudio](https://rstudio.com)
* [Anaconda](https://www.anaconda.com/)


<!-- Overview of the Methods -->
## Overview of the Methods

Cadaveric proximal femurs were scanned at 27 um resolution. Proximal femur strength data (i.e., maximum load) were reported previously to compare whole bone strength across skeletal sites (Patton et al, J Biomech 2019) and are used here to test for structure-function relationships.

### Volume Extraction

All image processing and quantification of bone microstructure were completed using Dragonfly software (Dragonfly 4.0, Object Research Systems; Montreal, QC, Canada). A process was developed to extract a consistent volume of interest (VOI) for the femoral neck, which included the location of most fracture paths following mechanical testing. Briefly, two anatomical landmarks, the inferior aspect of the lesser trochanter and the base of the greater trochanter, were used as anatomical landmarks to generate the distal plane of the femoral neck.

### Image Processing and Volume Extraction

Bone Segmentation and Cortical-Trabecular Separation
Segmentation of bone from background and cortical from trabecular area were conducted by developing and validating two separate two-dimensional (i.e., slice-by-slice segmentation) fully convolutional neural networks (FCNNs) with U-net architecture. The networks were trained and tested on the dataset within the framework of Dragonfly software 4.0 (ORS, Montreal, Computer: HP Z820 Workstation). 

Two custom plug-ins were created to run within the framework of Dragonfly:  

* 1. [GT_ROI Plug-in Folder](https://github.com/daniella-patton/Bone_Micro_Strength/tree/master/Ground_Truth_ROI_d7417746294e11e9a4db005056c00008): This plugin is used to 'average' three ROIs to create a Ground Truth ROI. The GT ROI is created by setting a voxel as ON if it is on in 2 or more of the three input ROIs, otherwise it is set to OFF. The plugin will check to make sure all three input ROI's exist and are the same shape. The GT ROI will have the same shape as the input ROIs, and will be associated with the same input image as ROI

* 2. [Compare Segmentations Plug-in Folder](https://github.com/daniella-patton/Bone_Micro_Strength/tree/master/CompareSegmentations_9de7a126150a11e98401005056c00008): his plugin is used to calculate several image comparison statistics to evaluate various segmentation methods. This plugin requires a "Ground Truth" ROI and the segemented comparison ROI. The plugin will make sure both selected ROIs are valid and the same shape; if not the plugin will return with no results calculated. The results calculated are output to a CSV file, if specified in GUI  

Additional details will not be described here, but the networks has a dice coefficient of 0.961 and 0.956 for the bone from background and cortical from trabecular, respectively. Both networks are publicly available on the [infinite toolbox (Dragonfly, ORS)](https://infinitetoolbox.theobjects.com).

### Quantification of Cortical and Trabecular Microstructure 

Measures of cortical and trabecular architecture were quantified using a custom written plug-in to run within the framework of Dragonfly:  

* 1. [Bone Quadrent Analysis](https://github.com/daniella-patton/Bone_Micro_Strength/tree/master/BoneQuadrentAnalysis_6be3f97a40e711e9ae07005056c00008):
Bone volume fraction was determined as the number of bone voxels normalized by the total number of voxels. Average thickness measures were determined by averaging a 3-D volume thickness map, which labeled each voxel of the VOI as the diameter of the largest sphere that can fit in the VOI at that location. Moments of inertia (rectangular, polar), cortical area (Ct.Ar) and total area (Tt.Ar) were quantified for the cortical shell. Each femoral neck volume was padded by 200 slices on the proximal and distal boundary before analysis to remove the possibility of boundary condition errors for cortical bone (i.e., underestimation of bone thickness). 

### Statistical Analysis
The statistical analysis was completed in three parts with increasing levels of refinement from least (Level 1) to most (Level 3). When/if the manuscript is published, I will attach a link directly to the publication for more information. 

* 1. [Lasso Regression](https://github.com/daniella-patton/Bone_Micro_Strength/blob/master/JBMR_Lasso_Regression.R): However, subsequent anlysis of each level of refinement were completed in RStudio and can be found here. The least absolute shrinkage and operator (LASSO) method from the glmnet package was used for the analysis of refinement level to identify the variables that were collectively the best predictors of bone strength. Outliers were removed, variables were normalized so coefficients could be compared directly, and data were split into training (75%) and test (25%) sets for each refinement level. The tuning parameter, λ, was determined using a three-fold cross validation on the training data. Two hundred λ values were tested for each model and the λ value that resulted in the most regularized model (i.e., λ1se) was determined. This was repeated 200 times and the median λ1se was used as the final value for the analysis to ensure convergence on consistent λ values.  Variables selected with the lasso regression were included in a final multiple linear regression model.

* 2. [Python Plots](https://github.com/daniella-patton/Bone_Micro_Strength/tree/master/BoneQuadrentAnalysis_6be3f97a40e711e9ae07005056c00008): Plots were created using the sklearn package in Python 3.0.


* 3. [Age-Regressions](https://github.com/daniella-patton/Bone_Micro_Strength/blob/master/JBMR_age_regression.R): To identify the variables in each level of refinement that change with age and differ by sex, least squares multiple linear regression including age, sex, and sex-age interaction was reported. The analysis of covariance (ANCOVA) was used to test whether the structural details of bone are equal across sex when controlling for age. 


<!-- USAGE EXAMPLES -->
## Usage

This repository is to be used as a reference for our current in-progress mansucript, to ensure that our work is useful, repeatable, and understandable for many. 


<!-- CONTRIBUTING -->
## Contributing

I would like to thank rob Goulet, PhD, who was a co-author on all of the plug-ins I have listed in this repository. 
In addition, I would like to thank my previous PhD advisor, Karl Jepsen, PhD. 

Additional contributors will be added **post manuscript review**.


<!-- LICENSE -->
## License
MIT © Daniella Patton



<!-- CONTACT -->
## Contact

Daniella Patton - pattondm@umich.edu

Project Link: [https://github.com/daniella-patton/Bone_Micro_Strength]("https://github.com/daniella-patton/Bone_Micro_Strength")

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Readme example from othneildrew](https://github.com/othneildrew/Best-README-Template)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png


