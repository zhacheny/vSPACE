# Welcome to vSPACE!
vSPACE: Exploring Virtual Spatial Representation of Articular Chondrocytes at the Single-Cell Level\\
This user guideline will walk you through the features and functionalities of the webpage, which could not only empower your research by analyzing and visualizing your data but also assist you in examining your hypothesis.

## Web Link
https://vspace.cse.uconn.edu/

# Sample Data
There are two types of data samples, OA and Cartnorm. 6 OA and 6 normal samples are obtained from NCBI GSE220244(https://ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE220244). One more OA data is added from NCBI GSE104782(https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104782). The GSE104782 data has been merged and processed.

# Z-ZPlot 
**What is Z-ZPlot?**
Z-ZPlot offers a powerful platform for visualizing data using Z scores. Users can Experiment with different datasets and customize options to gain valuable insights from your data.

**Key Terms Explained**
- Y-axis H threshold: estimated zonal score threshold for superficial zone and middle zone (Default set to 0.79, it can be adjusted by dragging the horizontal line);
- Y-axis L threshold: estimated zonal score threshold for middle zone, and deep zone (Default set to -0.99, it can be adjusted by dragging the horizontal line)
![image](https://github.com/zhacheny/vSPACE/assets/17793217/6c621bb5-26b6-4bd0-a5ad-e534ad5487cb)

- DO: Drop-out cells; MWDO: Mean with drop-out cells; MWODO: Mean without Drop out cells;
- %Total, %Sup, %Mid, and %Deep: the percentages of expressing cells concerning the total population, superficial zone, middle zone, and deep zone, respectively

**How to use it**
- Begin by inputting your data for the x and y axes. This would utilize the provided space to generate your Z-ZPlot. You can also customize your plot by adjusting the data points and zones (deep, mid, sup zone) as needed.
- You can explore the capability to visualize multiple genes simultaneously on the Z-ZPlot. Input various genes and observe their distributions and correlations within the plot.
- *Distribution table* : Users can access the Distribution Table feature to view the most correlated genes. Please utilize this information to refine your visualization by selecting correlated genes to add to the plot.
- You can also download cell information by selecting the region of interest on the Z-ZPlot (Simply, just drag the area you want to choose and hit the 'Download Selected Cells' button!). 

# Analysis modes
**Mode 1 : Use Gradient Color**:
- This mode allows the analysis of two selected genes simultaneously. Upon selection, the distribution tables on the right display the analysis results for each gene. You can utilize this mode to gain insights into the relationship between the two selected genes.
- Here is an example of the mode. You can see the analysis on the Distribution table for your selected two genes. You can threshold zones by dragging the horizontal lines. 
![UseGradientColor](https://github.com/zhacheny/vSPACE/assets/163660925/7f64a7ed-04b4-4db2-86d3-a5f79bf9cd7d)

**Mode 2 : Use Cell Selection**:
- In this mode, you can select multiple genes for analysis. After generating Z-ZPlot, hit the "Run" button to perform statistical tests. This feature identifies candidate cells based on the selected genes and displays highly correlated genes in order.
- Adjust the area of the plot using the "High", "Low", and "Absent" options to refine your analysis.
- Users can add more genes to analyze on the list. 
![UseCellSelection](https://github.com/zhacheny/vSPACE/assets/163660925/f9b38143-ba25-4bd7-86d5-cb9e8cffc8f9)

# Citation

```@article{vspace,
  title={vSPACE: Exploring Virtual Spatial Representation of Articular Chondrocytes at the Single-Cell Level},
  author={Zhang, C., Wang, H., Hong, S. H., Olmer, M., Swahn, H., Lotz, M. K., Maye, P., Rowe, D., & Shin, D. G. (2024).},
  journal={bioRxiv},
  doi={10.1101/2024.02.07.577817}
}```



## Acknowledgements
Research reported in this work was supported in part by NIH Grant No. U54AR078664 and its NOSI supplement. Its contents are solely the responsibility of the authors and do not necessarily represent the official views of the NIH.
