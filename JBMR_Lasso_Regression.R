# JBMR Lasso Regression
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
# Objective: Identify the microstructural traits (cortical and trabecular) in the 
#      femoral neck that best predict bone strength in males and females.
#      Potential Problems with dataset:
#           - small sample size
#           - collinear variables

# Lasso Regression Model will be used for a number of reasons
#       1) high prediction accuracy
#       2) shrink and remove coefficients without a substantial increase of the bias
#       3) perform well on datasets with few observations and many features
#       4) can increase the model interpretability by eliminating irrelevant variables 
#       (Tibshirani, 2011; Fonti, 2017)
##########################################################################################################################
# Functions that will be used to identify the optimal lambda value
# Lasso Function: 
# LASSO regression is similar to a regression value which minimizes the sum of squared errors. 
# - takes into account a tuning parameter, ??. The tuning parameter, is determined based off test data (a hold-out set)
# - and is selected to minimize the sum of square errors in the linear regression model applied to the test data.
# - ?? =  0-???. When ??=0 multiple linear regression, If ?? equals ??? all coefficients are eliminated. 
# -   Increased ?? = Increased Bias, Decreased ?? = Increased Variance 
# - ?? varies by model and requires systematic testing, such as cross-validation

# lassofunction:
# Description: 
# Uses a five-fold cross validation to determine the best model
# Tests 200 ?? values ranging from: 0.001 - 100000
# Two Test Outplut Plots to viualize: (1) ??min and ??1se selection: LogLamba_MSE
#                                     (2) variable importance
# Repeated this analysis 1000 to make sure the ??min and ??1se value is reproduicble 
# Output plots: Histogram of ??min and ??1se
# Final model:based off of median from ??min and ??1se
# Output Excel files: ??min: output beta valus and results 
#                     ??1se: output beta valus and results 
# Output variables: number of varibles, lambda, % Dev of the model explained
#                   sum of squared residuals (SSR), R^2
lambdas_to_try <- 10^seq(-3, 5, length.out = 200)
lambdas_to_try
min(lambdas_to_try)
max(lambdas_to_try)
lassofunction <- function(Test1){
  # Split into training and testing data
  smp_siz = floor(0.75*nrow(Test1)) # creates a value for dividing the data into training and tresting data
  set.seed(123)
  train_ind = sample(seq_len(nrow(Test1)), size = smp_siz)
  train = Test1[train_ind,] # Creates the training data
  test = Test1[-train_ind,] # Creates the training data
  
  # Setting alpha = 0 implements ridge regression
  lambdas_to_try <- 10^seq(-3, 5, length.out = 200)
  lasso_cv <- cv.glmnet(as.matrix(train[-1]), train[,1], alpha = 1, lambda = lambdas_to_try,
                        nfolds = 3, type.measure = "mse")
  # Plot cross-validation results
  jpeg("LogLamba_MSE.jpg")
  plot(lasso_cv)
  dev.off()
  plot.new()
  # Plot Summary of Parameter Importance
  jpeg("Lasso_norm_lambda.jpg", units = "in", width = 12, height = 12, res = 600)
  par(mfrow=c(1, 2))
  plot(lasso_cv$glmnet.fit, "norm", label=TRUE)
  plot(lasso_cv$glmnet.fit, "lambda", label=TRUE)
  dev.off()
  
  # Lamda min model and 1se
  i = 200
  testm <- matrix(nrow = i, ncol = 2)
  for (k in 1:i){
    lasso_cv <- cv.glmnet(as.matrix(train[-1]), train[,1], alpha = 1, lambda = lambdas_to_try,
                          nfolds = 3, type.measure = "mse")
    testm[k,1] <- lasso_cv$lambda.min
    testm[k,2] <- lasso_cv$lambda.1se
  }
  
  colnames(testm) <- c("lambda.min", "lambda.1se")
  lambdamin <- median(testm[,1])
  lambda1se <- median(testm[,2])
  
  jpeg("Lambdamin_Histogram.jpg", units = "in", width = 8, height = 6, res = 600)
  hist(testm[,1])
  dev.off()
  
  jpeg("Lambda1se_Histogram.jpg", units = "in", width = 8, height = 6, res = 600)
  hist(testm[,2])
  dev.off()
  
  # Lambda min
  lambdamin_cv <- glmnet(as.matrix(train[-1]), train[,1], alpha = 1, lambda = lambdamin)
  lambdamin <- coef(lambdamin_cv)
  lamdamindf <- data.frame(Type = rownames(lambdamin),
                           Beta = lambdamin[,1])
  write.csv(lamdamindf, "Lambamin_Beta_values.csv")
  #Training Data
  y_hat_cv <- predict(lambdamin_cv, as.matrix(train[,-1]))
  ssr_cv <- t(train[,1] - y_hat_cv) %*% (train[,1] - y_hat_cv)
  rsq_ridge_cv <- cor(train[,1], y_hat_cv)^2
  paramsum <- c(lambdamin_cv$df,lambdamin_cv$lambda,lambdamin_cv$dev.ratio,ssr_cv, rsq_ridge_cv)
  names <- c("DF", "Lambda", "%Dev", "SSR","RSQ")
  ResultsSum2 <- data.frame(names, paramsum)
  write.csv(ResultsSum2, "Lambamin_Results_train.csv")
  # Testing Data
  y_hat_cv <- predict(lambdamin_cv, as.matrix(test[,-1]))
  ssr_cv <- t(test[,1] - y_hat_cv) %*% (test[,1] - y_hat_cv)
  rsq_ridge_cv <- cor(test[,1], y_hat_cv)^2
  paramsum <- c(lambdamin_cv$df,lambdamin_cv$lambda,lambdamin_cv$dev.ratio,ssr_cv, rsq_ridge_cv)
  names <- c("DF", "Lambda", "%Dev", "SSR","RSQ")
  ResultsSum2 <- data.frame(names, paramsum)
  write.csv(ResultsSum2, "Lambamin_Results_test.csv")
  
  
  
  # Lambda 1se
  lambda1se_cv <- glmnet(as.matrix(train[-1]), train[,1], alpha = 1, lambda = lambda1se)
  lambda1se <- coef(lambda1se_cv)
  lambda1sedf <- data.frame(Type = rownames(lambda1se),
                            Beta = lambda1se[,1])
  write.csv(lambda1sedf, "Lamba1se_Beta_values.csv")
  # Train
  y_hat_cv <- predict(lambda1se_cv, as.matrix(train[,-1]))
  ssr_cv <- t(train[,1] - y_hat_cv) %*% (train[,1] - y_hat_cv)
  rsq_ridge_cv <- cor(train[,1], y_hat_cv)^2
  paramsum <- c(lambda1se_cv$df,lambda1se_cv$lambda,lambda1se_cv$dev.ratio,ssr_cv, rsq_ridge_cv)
  names <- c("DF", "Lambda", "%Dev", "SSR","RSQ")
  ResultsSum2 <- data.frame(names, paramsum)
  write.csv(ResultsSum2, "Lamba1se_Results_train.csv")
  
  # Test
  y_hat_cv <- predict(lambda1se_cv, as.matrix(test[,-1]))
  ssr_cv <- t(test[,1] - y_hat_cv) %*% (test[,1] - y_hat_cv)
  rsq_ridge_cv <- cor(test[,1], y_hat_cv)^2
  paramsum <- c(lambda1se_cv$df,lambda1se_cv$lambda,lambda1se_cv$dev.ratio,ssr_cv, rsq_ridge_cv)
  names <- c("DF", "Lambda", "%Dev", "SSR","RSQ")
  ResultsSum2 <- data.frame(names, paramsum)
  write.csv(ResultsSum2, "Lamba1se_Results_test.csv")
}
# Observed value - redicted val


#######################################################################################
# Level of Refinement 1
#################################################################################

# Lasso Regression
# Data Preparation
names(FNOrgResults)
myvars <- c("Max.Load.LTF..N.", "Total_BVF_mean", "TtAr_mean", "Sex",
            "maxTtAr", "minTtAr")
# We have 94 observations but only 83 with max load values
Test1 <- FNOrgResults[myvars]
Test1 <-  Test1[!(is.na(Test1$Max.Load.LTF..N.) | Test1$Max.Load.LTF..N.==""), ]

#quick look at vairables
pairs(Test1[,-4])

# Combined for Sex: Running the glmnet
setwd('C:/Users/pattondm/Desktop/JBMR_manuscript_data/Level1')
Test1$Sex <- as.numeric(as.factor(Test1$Sex))
# Add in interaction effect
Test1Sex <- model.matrix(Max.Load.LTF..N.~.*Sex, data = Test1)
Test1Sexdf <- as.data.frame(Test1Sex)
# Normalize variable so that min/max values are the same
Test1Sexdf_scaled <- as.data.frame(scale(Test1Sexdf))
# Drop Intercept 
drops <- c("(Intercept)")
Test1Sexdf_scaled = Test1Sexdf_scaled[ , !(names(Test1Sexdf_scaled) %in% drops)]
Test1Sexdf_scaled
# Adding Max Load Back to the data
Test1Sexdf2 <- cbind(MaxLoad = Test1$Max.Load.LTF..N., Test1Sexdf_scaled)
names(Test1Sexdf2)
lassofunction(Test1Sexdf2)
remove(Test1,Test1Sex,Test1Sexdf, Test1Sexdf_scaled,Test1Sexdf2)

###############################################################################
# Level of Refinement 2
################################################################################
# Data Preparation
# Ct.BVF, Ct.Th, Ct.Ar, Tb.BVF, Tb.Th, Ma.Ar, imin, imax, polar
names(FNOrgResults)
FNOrgResults[1:4,]
myvars <- c("Max.Load.LTF..N.", "Cortical_Total_BVTV", "Cortical_Total_mean_thick", "CtAr_mean",
            "Trabecular_Total_BVTV","Trabecular_Total_mean_thick", "MaAr_mean",
            "imin_mean","imax_mean", "polari_mean", "minTtAr", "Sex")
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
######################################################################################
# Combined for Sex: Running the glmnet
setwd('C:/Users/pattondm/Desktop/JBMR_manuscript_data/Level2')
Test2$Sex <- as.numeric(as.factor(Test2$Sex))
# Add in interaction effect
Test2Sex <- model.matrix(Max.Load.LTF..N.~.*Sex, data = Test2)
Test2Sexdf <- as.data.frame(Test2Sex)
# Normalize variable so that min/max values are the same
Test2Sexdf_scaled <- as.data.frame(scale(Test2Sexdf))
# Drop Intercept 
drops <- c("(Intercept)")
Test2Sexdf_scaled = Test2Sexdf_scaled[ , !(names(Test2Sexdf_scaled) %in% drops)]
# Adding Max Load Back to the data
Test2Sexdf2 <- cbind(MaxLoad = Test2$Max.Load.LTF..N., Test2Sexdf_scaled)
names(Test2Sexdf2)
lassofunction(Test2Sexdf2)
remove(Test2,Test2Sex,Test2Sexdf, Test2Sexdf_scaled,Test2Sexdf2)


#########################################################################################################################
# Level of Refinement 3
#########################################################################################################################
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
            "Sex", "minTtAr")
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
#########################################################################################################################################
#########################################################################################################################################
# Combined for Sex: Running the glmnet
setwd('C:/Users/pattondm/Desktop/JBMR_manuscript_data/Level3')
Test3$Sex <- as.numeric(as.factor(Test3$Sex))
# Add in interaction effect
Test3Sex <- model.matrix(Max.Load.LTF..N.~.*Sex, data = Test3)
Test3Sexdf <- as.data.frame(Test3Sex)
# Normalize variable so that min/max values are the same
Test3Sexdf_scaled <- as.data.frame(scale(Test3Sexdf))
# Drop Intercept 
drops <- c("(Intercept)")
Test3Sexdf_scaled = Test3Sexdf_scaled[ , !(names(Test3Sexdf_scaled) %in% drops)]
# Adding Max Load Back to the data
Test3Sexdf2 <- cbind(MaxLoad = Test3$Max.Load.LTF..N., Test3Sexdf_scaled)
names(Test3Sexdf2)
lassofunction(Test3Sexdf2)
remove(Test3,Test3Sex,Test3Sexdf, Test3Sexdf_scaled,Test3Sexdf2)







# Test 3 
setwd('C:/Users/pattondm/Desktop/Dissertation/Dissertation/Chapter V/Chapter V Data/LassoPlots/Level3/Combined')
# Combined for Sex: Running the glmnet
Test3$Sex <- as.numeric(as.factor(Test3$Sex))
lassofunction(Test3)

names(Test3)
setwd('C:/Users/pattondm/Desktop/Dissertation/Dissertation/Chapter V/Chapter V Data/LassoPlots/Level3/Combined_Interaction_NoCtAr')
Test3Sex <- model.matrix(Max.Load.LTF..N.~.*Sex, data = Test3)
Test3Sexdf <- as.data.frame(Test3Sex)
Test3Sexdf2 <- cbind(MaxLoad = Test3$Max.Load.LTF..N., Test3Sexdf)
names(Test3Sexdf2)
lassofunction(Test3Sexdf2)

# Females Only
setwd('C:/Users/pattondm/Desktop/Dissertation/Dissertation/Chapter V/Chapter V Data/LassoPlots/Level3/Female')
Test3  <- FNOrgResults[myvars]
Test3  <-Test3[!(is.na(Test3$Max.Load.LTF..N.) | Test3$Max.Load.LTF..N.==""), ]
tbthout <- filter(Test3, Sex == "F")
Out <- boxplot(tbthout$Trabecular_Inf1_mean_thick, plot = FALSE)$out
Test3 <- Test3[!(Test3$Trabecular_Inf1_mean_thick== Out),]
boxplot(Test3$Trabecular_Inf1_mean_thick)
remove(Out, tbthout)
Test3f <- filter(Test3, Sex == "F")
Test3f <- subset(Test3f, select = -c(Sex) )
head(Test3f)
lassofunction(Test3f)

# Males Only
setwd('C:/Users/pattondm/Desktop/Dissertation/Dissertation/Chapter V/Chapter V Data/LassoPlots/Level3/Male/Test')
Test3  <- FNOrgResults[myvars]
Test3  <-Test3[!(is.na(Test3$Max.Load.LTF..N.) | Test3$Max.Load.LTF..N.==""), ]
Test3m <- filter(Test3, Sex == "M")
Test3m <- subset(Test3m, select = -c(Sex) )
head(Test3m)
lassofunction(Test3m)


remove(Test3, Test3f, Test3m)
