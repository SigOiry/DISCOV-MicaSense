

# What is DISCOV ?

This repository complements a scientific paper published by Oiry et
al. in Remote Sensing of Environment (Under review).

This paper has produced during Simon Oiry’s PhD and the [BiCOME
project](https://bicome.info). The project is one of three studies that
form part of the European Space Agency’s ‘Biodiversity+ Precursors’
on [Terrestrial
(EO4DIVERSITY)](https://www.eo4diversity.info/), [Freshwater
(BIOMONDO)](https://www.biomondo.info/) and Coastal ecosystems (BiCOME).

<img src="Data/figs/Micasense_Dual_MX.png" align="left" width="20%" title="Micasense RedEdge-MX Dual">

This work demonstrates the development and application of a Neural
Network classification model trained on a Micasense RedEdge-MX Dual
multispectral drone camera. This model is called **DISCOV**, which
stands for **D**rone **I**ntertidal **S**ubstrats **C**lassification
**O**f **V**egetation.

<img src="Data/figs/Figure2.jpg" width="40%" align="right"
title="Classes of the model">

DISCOV is designed to classify soft bottom sediments, such as mudflats
and sandflats, as well as the vegetation typically found in these
habitats. The primary objective of this model is to accurately
distinguish between seagrasses and green macroalgae. This distinction
presents a significant challenge in remote sensing for accurately
classifying coastal habitats, owing to the similar pigment compositions
of these two types of vegetation. In the image on the right, you can see
the spectral signature for each vegetation class identified by the
model.

## Input and Output of the model

DISCOV processes input from a multilayer TIFF file containing 10
spectral bands. Band 1 corresponds to the 444 nm band of the Micasense
RedEdge-MX Dual, and Band 10 corresponds to the one at 840 nm. The model
has been trained using pixels processed into reflectance by [Agisoft
Metashape V2.1.1](https://www.agisoft.com). The training pixels were
encoded in 16-bit integers, with values ranging from 0 to 10,000. The
version 1.0 of DISCOV gives has output a TIFF file with values ranging
between 1 and 10:

- **1 - Microphytobenthos**: Unicellular microalgae and/or Cyanobacteria
  that can colonize superficial sediments at low tide. They can form a
  biofilm covering several square kilometers. The primary class of
  microalgae forming these biofilms is Bacillariophyceae, commonly known
  as diatoms.

- **2 - Chlorophyceae**: Green algae from the genus *Ulva sp* stranded
  on the sediment. The model has primarily been trained on *Ulva
  lactuca*, *Ulva armoricana*, and *Ulva intestinalis* . Therefore, I am
  uncertain how the model will behave when encountering other types of
  Chlorophyceae outside of the Ulvophyceae class, such as *Caulerpa
  sp.*).

- **3 - Magnoliopsida**: Marine angiosperm of the genus *Nanozostera
  sp.* (syn. *Zostera sp.*). The model has been trained exclusively on
  pixels from *Nanozostera noltei* (syn. *Zostera noltei*).

- **4 - Phaeophyceae**: Brown macrolalgae, stranded on the sediment or
  oftenly attached to rocks. Mainly trained from pixels of the genus
  *Fusus sp.*

- **5 - Rhodophyceae**: Red Algae. This class was trained with the
  fewest pixels in DISCOV V1.0, using only pixels from *Gracilaria sp.*
  (likely *Gracilaria vermiculophylla*) observed in the Ria de Aveiro
  coastal lagoon, Portugal.

- **6 - Bare Sediment**: The class is primarily trained on bare mud but
  also performs well on sand. It can be mistaken for Microphytobenthos
  because sometimes the bare mud contains a small amount of
  chlorophyll-a, which absorbs light around 668 nm.
