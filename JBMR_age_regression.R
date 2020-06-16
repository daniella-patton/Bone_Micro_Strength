# JBMR Age Regression
# Daniella Patton
# Last Edit: 6/15/2020

# Summary:
#    - Objective 1: The objective of this study is to identify the microstructural traits (cortical and trabecular) in the 
#      femoral neck that best predict bone strength in males and females. 
#    - Objective 2: In addition, we will determine if adding more 
#      cortical and trabecular architectural details improves strength predictions. In order address this objective, 
#      analyses will be completed in three levels of refinement from least to most detail.

# Proximal femur femoral neck data was extracted using a custom code written in Python in Dragonfly ORS
# Levels of Refinement
# Level of Refinemnt One:  Total_BVF_mean, TtAr_mean, Sex, maxTtAr, minTtAr

# Level of Refinement Two: Cortical_Total_BVTV, Cortical_Total_mean_thick, CtAr_mean, 
#                          Trabecular_Total_BVTV,Trabecular_Total_mean_thick, MaAr_mean, 
#                          ixx_mean, ixy_mean, iyy_mean,imin_mean,imax_mean,polari_mean,
#                          minTtAr,Sex

# Level of refinmnt Three: Cortical_Sup1_BVTV,Cortical_Sup1_mean_thick,Trabecular_Sup1_BVTV,
#                          Trabecular_Sup1_mean_thick, Cortical_Sup2_BVTV,Cortical_Sup2_mean_thick,    
#                          Trabecular_Sup2_BVTV,Trabecular_Sup2_mean_thick,Cortical_Inf1_BVTV,
#                          Cortical_Inf1_mean_thick, Trabecular_Inf1_BVTV, Trabecular_Inf1_mean_thick,
#                          Cortical_Inf2_BVTV, Cortical_Inf2_mean_thick, Trabecular_Inf2_BVTV,
#                          Trabecular_Inf2_mean_thick, Sex, minTtAr
##########################################################################################################################
# Packages
rm(list = ls())
library('caret')
library('ellipse')
library('dplyr')
library('tidyverse')
library('MASS')
library('faraway')
library('olsrr')
library('ggplot2')
library(glmnet)  # for ridge regression
library(dplyr)   # for data cleaning
library(psych)   # for function tr() to compute trace of a matrix
set.seed(123)    # seed for reproducibility
###########################################################################################################################
###########################################################################################################################
# Read in the Data
getwd()
setwd('C:/Users/pattondm/Desktop/Dissertation/Dissertation/Dissertation_Chapters/Chapter 5/Chapter V Data')
FNOrgResults <- read.csv('FN_Org_Results.csv')
names(FNOrgResults)
FNOrgResults[1:4,]


# Checking the Output Vairable of Interest: Max.Load.LTF..N.
# Boxplot
boxplot(FNOrgResults$Max.Load.LTF..N.)
ggplot(FNOrgResults, aes(x = Sex, y = Max.Load.LTF..N., fill = Sex)) + geom_boxplot()
dev.off()

# Histogram
hist(FNOrgResults$Max.Load.LTF..N.)
ggplot(FNOrgResults, aes(x = Max.Load.LTF..N., color = Sex)) + geom_histogram(fill="white", alpha=0.5, position="identity")
dev.off()

# qqnorm
qqnorm(FNOrgResults$Max.Load.LTF..N.) 
qqline(FNOrgResults$Max.Load.LTF..N.)
ggplot(FNOrgResults, aes(sample = Max.Load.LTF..N., color = Sex)) + geom_qq_line() + stat_qq()
dev.off()
##########################################################################################################################
# Objective: Identify sex specific differences in age-bone microstructural loss (cortical and trabecular) in the 
#      femoral neck that best predict bone strength in males and females.
###########################################################################################################################
# Loop to run an ANCOVA on all vairables that in a table that are not sex and age
ancovatests <- function(data_tbl, level){
  # Run ancova for all variables, excluding age and sex
  i = dim(data_tbl)[2] - 2
  for (k in 1:i){
    y = names(data_tbl)[k]
    print(y)
    mod1 = aov(data_tbl[,k] ~ data_tbl$Sex*data_tbl$Age)
    csv_export = paste(level, y, "_ancova.csv")
    print(csv_export)
    mod_df = data.frame(unclass(summary(mod1)), check.names = FALSE, stringsAsFactors = FALSE)
    write.csv(mod_df, csv_export)
    LM <- lm(data_tbl[,k] ~ data_tbl$Sex*data_tbl$Age)
    print(summary(LM))
  }
}
###########################################################################################################################
# Read in the Data
getwd()
setwd('C:/Users/pattondm/Desktop/Dissertation/Dissertation/Dissertation_Chapters/Chapter 5/Chapter V Data')
FNOrgResults <- read.csv('FN_Org_Results.csv')
names(FNOrgResults)
FNOrgResults[1:4,]
#######################################################################################
# Level of Refinement 1
#################################################################################
# ANCOVA
# Data Preparation
names(FNOrgResults)
myvars <- c("Max.Load.LTF..N.", "Total_BVF_mean", "TtAr_mean","maxTtAr", "minTtAr",
            "Sex","Age")
# We have 94 observations but only 83 with max load values
Test1 <- FNOrgResults[myvars]
Test1 <-  Test1[!(is.na(Test1$Max.Load.LTF..N.) | Test1$Max.Load.LTF..N.==""), ]

#quick look at vairables
pairs(Test1[,-4])

# Combined for Sex: Running the glmnet
setwd('C:/Users/pattondm/Desktop/JBMR_manuscript_data/Level1')
Test1$Sex <- as.numeric(as.factor(Test1$Sex)) # Female = 1, Male = 2
ancovatests(Test1, level = "Level1")

remove(Test1)
###############################################################################
# Level of Refinement 2
################################################################################
# Data Preparation
# Ct.BVF, Ct.Th, Ct.Ar, Tb.BVF, Tb.Th, Ma.Ar, imin, imax, polar
names(FNOrgResults)
FNOrgResults[1:4,]
myvars <- c("Max.Load.LTF..N.", "Cortical_Total_BVTV", "Cortical_Total_mean_thick", "CtAr_mean",
            "Trabecular_Total_BVTV","Trabecular_Total_mean_thick", "MaAr_mean",
            "imin_mean","imax_mean", "minTtAr", "Age", "Sex")
# We have 94 observations but only 83 with max load values
Test2 <- FNOrgResults[myvars]
Test2 <-  Test2[!(is.na(Test2$Max.Load.LTF..N.) | Test2$Max.Load.LTF..N.==""), ]
# Need to remove the trabecular thickness outlier for females. 
tbthout <- filter(Test2, Sex == "F")
names(Test2)
boxplot(tbthout$Trabecular_Total_mean_thick)
Out <- boxplot(tbthout$Trabecular_Total_mean_thick, plot = FALSE)$out
Test2 <- Test2[!(Test2$Trabecular_Total_mean_thick== Out),]
boxplot(Test2$Trabecular_Total_mean_thick)
remove(tbthout, Out)

# Combined for Sex: Running the glmnet
setwd('C:/Users/pattondm/Desktop/JBMR_manuscript_data/Level2')
Test2$Sex <- as.numeric(as.factor(Test2$Sex)) # Female = 1, Male = 2
ancovatests(Test2, level = "Level2")
remove(Test2)

###############################################################################
# Level of Refinement 3
################################################################################
# Data Preparation
# Level 3 Data Preparation
# variables of Interest 
#head(FNOrgResults)
#names(FNOrgResults)
# Maybe add ct.Ar nd Ma.Ar
myvars <- c("Max.Load.LTF..N.",
            "Cortical_Sup1_BVTV","Cortical_Sup1_mean_thick",     
            "Trabecular_Sup1_BVTV","Trabecular_Sup1_mean_thick",
            "Cortical_Sup2_BVTV","Cortical_Sup2_mean_thick",    
            "Trabecular_Sup2_BVTV","Trabecular_Sup2_mean_thick",  
            "Cortical_Inf1_BVTV","Cortical_Inf1_mean_thick",
            "Trabecular_Inf1_BVTV", "Trabecular_Inf1_mean_thick",
            "Cortical_Inf2_BVTV", "Cortical_Inf2_mean_thick",
            "Trabecular_Inf2_BVTV","Trabecular_Inf2_mean_thick",
             "minTtAr", "Age", "Sex")
Test3 <- FNOrgResults[myvars]
#head(Test3)
Test3 <-  Test3[!(is.na(Test3$Max.Load.LTF..N.) | Test3$Max.Load.LTF..N.==""), ]
tbthout <- filter(Test3, Sex == "F")
boxplot(tbthout$Trabecular_Sup1_mean_thick, main="Female Sup. 1 Tb.Th")
boxplot(tbthout$Trabecular_Sup2_mean_thick, main="Female Sup. 2 Tb.Th")
boxplot(tbthout$Trabecular_Inf1_mean_thick, main="Female Inf. 1 Tb.Th") # Inf1 is where the extreme outlier is located 
boxplot(tbthout$Trabecular_Inf2_mean_thick, main="female Inf. 2 Tb.Th")
Out <- boxplot(tbthout$Trabecular_Inf1_mean_thick, plot = FALSE)$out
Test3 <- Test3[!(Test3$Trabecular_Inf1_mean_thick== Out),]
boxplot(Test3$Trabecular_Inf1_mean_thick)
remove(Out, tbthout)

# Combined for Sex: Running the glmnet
setwd('C:/Users/pattondm/Desktop/JBMR_manuscript_data/Level3')
Test3$Sex <- as.numeric(as.factor(Test3$Sex)) # Female = 1, Male = 2
ancovatests(Test3, level = "Level3")


















