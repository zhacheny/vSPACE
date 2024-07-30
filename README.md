# Welcome to vSPACE!
vSPACE: Exploring Virtual Spatial Representation of Articular Chondrocytes at the Single-Cell Level\\
This user guideline will walk you through the features and functionalities of the webpage, which could not only empower your research by analyzing and visualizing your data but also assist you in examining your hypothesis.

## Web Link
https://vspace.cse.uconn.edu/

# Sample Data
There are two types of data samples, OA and Cartnorm. 6 normal samples (1. CartNorm1_31_F_G1; 2. CartNorm2_24_M_G0; 3. CartNorm3_20_M_G0; 4. CartNorm4_56_M_G1; 5. CartNorm5_49_M_G2; 6. CartNorm6_27_F_G0) and 6 OA samples (7. OA1_67_F; 8. OA2_72_F; 9. OA3_69_F; 10. OA4_61_F; 11. OA5_71_M; 12. OA6_69_M) are obtained from NCBI GSE220244(https://ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE220244). One more OA data (13. OA _10_patients-Pooled) is added from NCBI GSE104782(https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104782). The GSE104782 data has been merged and processed.

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

# Supplementary Information
### Comparison of Spearman Correlation and Pearson Correlation
![image](https://github.com/user-attachments/assets/0d890ff4-f067-42c0-be71-fcc4ef684063)

**Supplementary Table S1**:This table is to contrast <correlation coefficient, p-value> from Pearson and Spearman tests for the X and Y values obtained for selectively chosen 16 genes using the entire population of cells (total number, 7068) from the human knee articular cartilage sample CartNorm4_56_M_G1 (56 years old, Male, Sample Grade 1). The objective of this table is to contrast linear or non-linear nature of “correlation” trends between the z-score for the chosen gene (X value) and the “surrogate” zonal score (Y value) for all cells. One question under consideration is if Equation 1 prescribes the outcome patterns to follow linearity exclusively or not. One way to test the linearity presumption by the equation is to perform two different correlation tests between actual X and Y values that are produced for the population of cells and compare the coefficient values from the two tests, Pearson measuring linear associating and Spearman measuring monotonic relationship. By comparing the coefficients from the two tests, one can gauge the likely linear/or non-linear trend inherently present in the population of the cells. For each row (gene) in the table, the larger (stronger) coefficient cases are denoted by **. Marker column indicates if the selected gene is a zonal marker gene used to calculate the zonal score or not. Absent value here means not a marker gene.  The comparison shows that in 11 out of the total 16, the magnitude of Spearman coefficient values is larger. In contrast, in 5 out of 16 cases Pearson coefficient is larger indicating a higher degree of linearity. Noticeable here are the 3 out 5 these cases are for the marker genes which is expected due to the nature of algebraic formulation of Equation 1. Since these coefficients are only indicative of trend (positive value for positive correlation and negative value for negative trend), the actual Z-Z plots for a subset of these genes are presented in Supplementary Figure S1. 

### Selective Z-Z Plots with Correlation Coefficients
![image](https://github.com/user-attachments/assets/31f1b81b-ea9e-4441-a5c0-31a48ee721ff)

**Supplementary Figure S1**:Selective Z-Z plots from the genes in Supplementary Table S1 are presented to help the readers develop intuition in interpreting the reported correlation coefficients. Each plot is annotated with two numbers in the format, Spearman coefficient vs. Peason coefficient. The boldface blue colored number signifies a larger absolute value between the two. The figure IDs A-L match the IDs given in Fig. S1 column in Table S1 thus following the rank order of the genes listed based on the Spearman coefficients (from the highest to the lowest). Star icons are placed to indicate marker gene status, OGN (A), PRG4 (B) and IGFBP5 (D), for the superficial zone (with red color stars) and COL10A1 (H), IBSP (I) and CLEC3A (K) for the deep zone (with green color stars). The correlation trend is indicated by the plot outline color, Red for positive correlation and Green for negative correlation. Gray suggests little correlation such as for TPT1 (F) and COL2A1 (G). TPT1 is a great example for no correlation and this figure has been instrumental for biologists to decide to use TPT1 as a control in their spatial transcriptomics experiments since this gene should be highly expressing in all zones. A few notable facts in this figure are summarized. (i) The genes with higher Spearman coefficient than Pearson coefficient exhibit non-linearity trend as expected. (ii) There are genes exhibiting a linear trend as in COL10A1 (H) and IBSP (I) and this is not surprising because these two genes are marker genes used to produce Y axis values. (iii) However, being a marker gene does not mean the trend should be linear as evidenced by the patterns and the higher Spearman coefficients for other marker genes OGN (A), PRG4 (B), IGFBP5 (D), and CLEC3A (K). (iv) Lastly, strongly correlated genes are newly discovered such as CRTAC1 (C), ACAN (J) and FGFBP2 (L) which clearly show non-linear trends and strongly suggest spatial locality of gene expression patterns along the zonal axis. Such information has been very useful for bench scientists.
# Citation

```
@article{vspace,
  title={vSPACE: Exploring Virtual Spatial Representation of Articular Chondrocytes at the Single-Cell Level},
  author={Zhang, C., Wang, H., Hong, S. H., Olmer, M., Swahn, H., Lotz, M. K., Maye, P., Rowe, D., & Shin, D. G. (2024).},
  journal={bioRxiv},
  doi={10.1101/2024.02.07.577817}
}
```



## Acknowledgements
Research reported in this work was supported in part by NIH Grant No. U54AR078664 and its NOSI supplement. Its contents are solely the responsibility of the authors and do not necessarily represent the official views of the NIH.
