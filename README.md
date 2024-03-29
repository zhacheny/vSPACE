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
- In this mode, you can select multiple genes for analysis. After Z-ZPlot is generated, hit the "Run" button to perform statistical tests. This feature identifies candidate cells based on the selected genes and displays highly correlated genes in order.
- Adjust the area of the plot using the "High", "Low", and "Absent" options to refine your analysis.
- Users can add more genes to analyze on the list. 
![UseCellSelection](https://github.com/zhacheny/vSPACE/assets/163660925/f9b38143-ba25-4bd7-86d5-cb9e8cffc8f9)


## Acknowledgements
Research reported in this work was supported in part by NIH Grant No. U54AR078664 and its NOSI supplement. Its contents are solely the responsibil-ity of the authors and do not necessarily represent the official views of the NIH.
