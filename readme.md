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
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
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


<!-- GETTING STARTED -->
## Overview of the Methods

Cadaveric proximal femurs were scanned at 27 um resolution. Proximal femur strength data (i.e., maximum load) were reported previously to compare whole bone strength across skeletal sites (Patton et al, J Biomech 2019) and are used here to test for structure-function relationships.

### Volume Extraction

All image processing and quantification of bone microstructure were completed using Dragonfly software (Dragonfly 4.0, Object Research Systems; Montreal, QC, Canada). A process was developed to extract a consistent volume of interest (VOI) for the femoral neck, which included the location of most fracture paths following mechanical testing. Briefly, two anatomical landmarks, the inferior aspect of the lesser trochanter and the base of the greater trochanter, were used as anatomical landmarks to generate the distal plane of the femoral neck.

### Image Processing and Volume Extraction

Bone Segmentation and Cortical-Trabecular Separation
Segmentation of bone from background and cortical from trabecular area were conducted by developing and validating two separate two-dimensional (i.e., slice-by-slice segmentation) fully convolutional neural networks (FCNNs) with U-net architecture. The networks were trained and tested on the dataset within the framework of Dragonfly software 4.0 (ORS, Montreal, Computer: HP Z820 Workstation). The details will not be described here, but the networks has a dice coefficient of 0.961 and 0.956 for the bone from background and cortical from trabecular, respectively. Both networks are publicly available on the [infinite toolbox (Dragonfly, ORS)](https://infinitetoolbox.theobjects.com).

### Quantification of Cortical and Trabecular Microstructure 

Measures of cortical and trabecular architecture were quantified using a custom written plug-in that is publicly available through the Infinite Toolbox in Dragonfly software 4.0 (ORS, Montreal, Canada, https://infinitetoolbox.theobjects.com/category/Plugins). Bone volume fraction was determined as the number of bone voxels normalized by the total number of voxels. Average thickness measures were determined by averaging a 3-D volume thickness map, which labeled each voxel of the VOI as the diameter of the largest sphere that can fit in the VOI at that location. Moments of inertia (rectangular, polar), cortical area (Ct.Ar) and total area (Tt.Ar) were quantified for the cortical shell. Each femoral neck volume was padded by 200 slices on the proximal and distal boundary before analysis to remove the possibility of boundary condition errors for cortical bone (i.e., underestimation of bone thickness). 

Statistical Analysis
The statistical analysis was completed in three parts with increasing levels of refinement from least (Level 1) to most (Level 3) (Fig. 3). The structural details included in each refinement level and used to predict whole bone strength are listed below:
-	Level 1: In the lowest refinement level, femoral neck total bone volume fraction and basic measures of external morphology (i.e., total area) were included. Although BMD was not assessed for these samples, the detail for Level 1 was expected to capture a relatively similar type of information to what is obtained from BMD. This analysis included basic information on the femoral neck size and mass, including measures of external size (mean TtAr, minimum TtAr, maximum TtAr) and the total bone volume fraction (total BVF), which includes both cortical and trabecular tissues.
-	Level 2: The next (intermediate) level of refinement included information on cortical and trabecular architecture separately. The second analysis added details about cortical shell structure and trabecular architecture averaged over the entire femoral neck VOI, including trabecular thickness (Tb.Th), trabecular bone volume fraction (Tb.BVF), cortical thickness (Ct.Th), cortical bone volume fraction (Ct.BVF), cortical area (Ct.Ar), subendosteal area (Ma.Ar + trabecular area), and principal moments of inertia (Imin, Imax). Minimum Tt.Ar was included so that a measure of external size was considered in the analysis.
-	Level 3: The third, most detailed, analysis added regional information on cortical shell structure and trabecular architecture. Cortical and marrow regions were segmented into superior-proximal [SP], superior-distal [SD], inferior-proximal [IP], inferior-distal [ID]) regions for a total of 8 sub-regions (4 cortical and 4 trabecular VOIs). The traits quantified for the cortical regions included Ct.Th and Ct.BVF. The traits quantified for the trabecular regions included Tb.Th and Tb.BVF. Like Level 2, minimum Tt.Ar was included so that a measure of external size was considered in the analysis. 

Analyses were completed in RStudio [23] and all subsequent code used for analysis is publicly available (https://github.com/daniella-patton/Bone_Micro_Strength). The least absolute shrinkage and operator (LASSO) method from the glmnet package was used for the analysis of refinement level to identify the variables that were collectively the best predictors of bone strength [23]. LASSO regression is a machine learning model that performs well on datasets with few observations and many features and that increases model interpretability by eliminating irrelevant variables [24], [25]. The LASSO method objectively identifies variables of greatest importance in predicting strength for each refinement level. Sex was included as a covariate for all models. Plots were created using the sklearn package in Python 3.0 [26].

Outliers were removed, variables were normalized so coefficients could be compared directly, and data were split into training (75%) and test (25%) sets for each refinement level. The tuning parameter, λ, was determined using a three-fold cross validation on the training data. Briefly, two hundred λ values were tested (Range: 0.001- 100000, Sequence: 10ji, j_i=∑_(-3)^5▒〖j_(i-1)+0.04〗) for each model and the λ value that resulted in the most regularized model (i.e., λ1se) was determined. λ1se is the λ value that lies within one standard error of the optimal value that minimizes the mean squared-error (i.e., λmin) [27]. This was repeated 200 times and the median λ1se was used as the final value for the analysis to ensure convergence on consistent λ values. 

The R2 values were reported for each model on the training and test set along with beta (β) values for variables that were significant predictors of strength. Further, the percent (null) deviance explained (i.e., a measure 1 – deviance ratio of the model divided by the null deviance) was included, which is a measure of how well the response variable is predicted by the final model compared to a saturated model and a model which includes only the intercept. Next, the variables selected with the lasso regression were included in a final multiple linear regression model. Beta values, p-values, and adjusted R-squared values were reported for each of the final models.

Finally, to identify the variables in each level of refinement that change with age and differ by sex, least squares multiple linear regression including age, sex, and sex*age interaction was reported. The analysis of covariance (ANCOVA) was used to test whether the structural details of bone are equal across sex when controlling for age. 


This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
```sh
npm install npm@latest -g
```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
```sh
git clone https://github.com/your_username_/Project-Name.git
```
3. Install NPM packages
```sh
npm install
```
4. Enter your API in `config.js`
```JS
const API_KEY = 'ENTER YOUR API';
```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [GitHub Pages for othneildrew](https://github.com/othneildrew/Best-README-Template)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





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






