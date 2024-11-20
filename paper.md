---
title: 'DISCOV: A Neural Network Classifier for Intertidal Vegetation Drone Mapping'
tags:
- Python
- R
- Marine Ecology
- Drone
- Seagrass
date: "13 August 2017"
affiliations:
- name: "Institut des Substances et Organismes de la Mer, ISOMer, Nantes Université,
    UR 2160, F-44000 Nantes, France"
  index: 1
authors:
- name: Simon Oiry
  orcid: "0000-0001-7161-5246"
  equal-contrib: true
  affiliation: 1
- name: Bede Ffinian Rowe Davies
  orcid: "0000-0001-6462-4347"
  equal-contrib: true
  affiliation: 1
- name: Pierre Gernez
  orcid: "0000-0003-2055-410X"
  equal-contrib: true
  affiliation: 1
- name: Laurent Barillé
  orcid: "0000-0001-5138-2684"
  equal-contrib: true
  affiliation: 1
bibliography: paper.bib
---

# Summary

Coastal intertidal seagrass meadows are critical ecosystems providing essential services such as carbon sequestration, erosion control, and habitats for diverse marine species [@sousa2019blue; @unsworth2022]. Despite their importance, these ecosystems face increasing threats from human activities, eutrophication, and habitat fragmentation, which diminish their ecological functions [@chefaoui2018dramatic; @nguyen2021; @wang2022]. Monitoring these habitats has been challenging due to their dynamic nature and the complexity of distinguishing vegetation types with similar pigment compositions [@Douay2022; @ralph2002]. This study addresses these challenges by developing a deep learning model capable of accurately classifying macrophytes, including seagrasses (Magnoliopsida) and green algae (Chlorophyceae), which share close pigment compositions [@Davies2023]. The model was trained on high-resolution drone-based reflectance data collected across diverse intertidal habitats in France and Portugal, encompassing monospecific and mixed vegetation meadows. It successfully discriminates between macrophyte types, leveraging subtle spectral differences, even in challenging cases where pigment similarity could hinder classification. This approach highlights the potential for advanced modeling techniques to improve vegetation mapping accuracy, offering insights into intertidal ecosystem dynamics and supporting more effective conservation strategies.

## Statement of needs

Accurately mapping and classifying intertidal vegetation, such as seagrasses and green macroalgae, is vital for the sustainable management of coastal ecosystems. These habitats provide critical services, including carbon sequestration, erosion control, and biodiversity support, but face escalating threats from anthropogenic pressures, climate change, and eutrophication. Monitoring these ecosystems requires precise, reliable, and scalable tools to assess habitat distribution, health, and changes over time.

Traditional monitoring methods, such as field surveys and satellite remote sensing, face significant limitations. Field surveys are labor-intensive, restricted by tidal accessibility, and often lack spatial coverage. Satellite data, while providing broader coverage, typically struggles with inadequate spatial and spectral resolution, making it difficult to differentiate between vegetation types like seagrasses and green macroalgae, which share similar pigment compositions and spectral characteristics. This gap necessitates innovative solutions to deliver high-resolution and accurate classification.

![](Website/Imgs/DISCOV_logo.png){width="20%"}

The **DISCOV (Drone Intertidal Substrate Classification Of Vegetation)** model offers a groundbreaking solution to these challenges. By leveraging drone-based high-resolution multispectral imagery and a neural network classifier, DISCOV enables the precise discrimination of vegetation types, even in mixed and heterogeneous habitats. This model delivers several capabilities:

-   **High Classification Accuracy**: DISCOV achieves a classification accuracy of 94%, with 97% accuracy in distinguishing seagrasses from green macroalgae, addressing a key challenge in remote sensing applications.
-   **Disctinction of 5 vegetation classes**: DISCOV is not only able to distinguish green algae from seagrasses, but can also recognize the most common vegetation classes found in intertidal areas along the European Atlantic coastline: Phaeophyceae (Brown macroalgae), Rhodophyceae (Red macroalgae) and Bacillariophyceae (diatoms).

Applications of DISCOV span a range of critical environmental management and research areas: - **Early Detection of Green Tides**: Monitoring and identifying the initial stages of algal blooms to mitigate their ecological and economic impacts. - **Seagrass Health Assessment**: Evaluating resilience to eutrophication, climate stressors, and other anthropogenic pressures. - **Policy Support**: Providing actionable data to meet conservation goals outlined in international frameworks like the EU Water Framework Directive. - **Biodiversity Conservation**: Mapping habitats to inform restoration and protection efforts.

DISCOV is addressing the need for advanced tools to combat biodiversity loss and environmental degradation. By integrating drone-based insights with larger-scale remote sensing efforts, DISCOV offers a scalable, efficient, and accurate framework for understanding and managing intertidal vegetation dynamics in the face of accelerating global change.

# Material & Methods 

This study employed drone-based high-resolution multispectral imagery to classify intertidal vegetation across nine sites in France and Portugal. Two flight altitudes (12 m and 120 m) were used, providing spatial resolutions of 8 mm and 80 mm, respectively. A DJI Matrice 200 drone equipped with a Micasense RedEdge Dual MX sensor (10 spectral bands: 444–840 nm) was used for image acquisition. Ground control points were established with differential GPS for georeferencing, and reflectance was calibrated using a standard panel.

Low-altitude flights were utilized to train the DISCOV model, a neural network classifier developed using the fastai workflow with two hidden layers and 26,054 trainable parameters. The model was trained on more than 418,000 pixels from the 8 mm resolution imagery, categorized into seven classes: seagrasses, green macroalgae, red macroalgae, brown macroalgae, benthic diatoms, sediment, and water. Training incorporated spectral bands, their standardized values, and the NDVI index.

![Schematic representation of the workflow. Parallelograms represent input or output data, and rectangles represent Python processing algorithms. The overall workflow of this study is divided into two distinct parts based on the spatial resolution of the drone flights: high-resolution flights (pixel size: 8 mm) were used for training and prediction of the Neural Network model, whereas lower-resolution flights (pixel size: 80 mm) were solely employed for prediction purposes. Validation has been performed on both high and low-resolution flights.](Website/Imgs/Figure3.png){width="95%"}

Validation was performed using both low- and high-altitude flights, with 536,000 pixels collected from *in situ* field measurements and photo-interpretations. Metrics such as global accuracy, sensitivity, specificity, F1 score, and Kappa coefficient were calculated to evaluate model performance. 

![A global confusion matrix on the left is derived from validation data across each flight, while a mosaic of confusion matrices from individual flights is presented on the right. The labels inside the matrices indicate the balanced accuracy for each class. The labels at the bottom of the global matrix indicate the User’s accuracy for each class, and those on the right indicate the Producer’s Accuracy. The values adjacent to the names of each site represent the proportion of total pixels from that site contributing to the overall matrix. Grey lines within the mosaic indicate the absence of validation data for the class at that site. The table at the bottom summarizes the Sensitivity, Specificity, and Accuracy for each class and for the overall model.](Website/Imgs/ConfusionMatrixGlobal.png){width="95%"}

# Acknowledgments

This work was supported through the BiCOME (Biodiversity of the Coastal Ocean: Monitoring with Earth Observation) project funded by the European Space Agency under the ‘Earth Observation Science for Society’ element of FutureEO-1 BIODIVERSITY+PRECURSORS call, contract No. 4000135756/21/I-EF. This work was also supported by French Ministry of Research & Higher Education for funding first authors PhD. This study was partially funded by FCT/MCTES (Fundação para a Ciência e a Tecnologia) under the project UIDB/50017/2020 + UIDP/50017/2020 + LA/P/0094/2020 granted to CESAM and through research contract CEECIND/00962/2017 (DOI: 10.54499/CEECIND/00962/2017/CP1459/CT0008) granted to AI Sousa. The work was also partially funded by the project BIOPRADARIA (MAR-01.04.02-FEAMP-0020), funded by the Operational Program MAR2020, EMFF-European Maritime and Fisheries Fund, European Union, Portugal2020.

# References
