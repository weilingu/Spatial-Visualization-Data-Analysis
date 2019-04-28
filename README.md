# Spatial Visualization for Data Analysis

The first step to tackle any project that involves dataset is to understand the data. A common and easy approach is to plot a few distribution graphs, such as histograms, boxplots, pie charts, and etc. To uncover relationships between variables, we can  use scatter plots, line plots, or even 3D contour plots. These techniques are easy to implement and the graphs easy to interpret. However, they usually fail to uncover other important characteristics of a dataset, such as geographical variations.
 
This project aims to demonstrate the power of spatial visualization in preliminary data analysis. Using powerful graphic packages such as `Matplotlib`, `Seaborn`, and `Basemap` available in Python, we can create informative spatial visualization of a dataset that could help us gain a deeper understanding of the data and uncover interesting variable characteristics.
 
This post shows how you could quickly create a spatial visualization graph. I use the `IRS 2017 U.S. Tax Return` dataset as an example. After reading the notebook, you will see how we could change the visualization of the dataset from this messy and relatively uninformative graph:   

<img src="https://user-images.githubusercontent.com/48388315/56777145-da35dc00-679d-11e9-9aa1-320a72903717.jpg" align="center">

to this clean and informative graph: 

![Income by Zip Code](https://user-images.githubusercontent.com/48388315/56778693-9b0b8900-67a5-11e9-85da-d36430a3a8c3.png)


