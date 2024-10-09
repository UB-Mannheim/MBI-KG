# Models

The two fine-tuned models are specialized for processing the historical document "Die Maschinen-Industrie im Deutschen Reich" using the Kraken OCR engine through the eScriptorium platform.

## mbi-1937_layout
### Purpose
This model focuses on layout segmentation, which is crucial for accurately capturing the complex page structure of the source material. The biggest challenge addressed by this model is the two-column layout, where each column contains individual company entries, separated into distinct layout regions.
### Fine-tuning
To ensure the segmentation aligns with the document's unique layout, the layout model was trained on 47 pages specifically created for layout segmentation. The separators between company entries further complicated the task, making it essential to define precise regions for each entry. The base model used for the fine-tuning is called "cbad_1800_compensated_50".

## mbi-1937_print
### Purpose
This model is dedicated to text recognition, specifically the fonts and printing styles used in historical documents.
### Fine-tuning
The transcription model was fine-tuned using a data set of 26 pages, specifically selected to capture the unique characteristics of the fonts used in the document. This was necessary to achieve a high level of text recognition accuracy, especially given the historical and potentially challenging fonts used. The base model used for fine-tuning is called "digitue_best".
### Guidelines
The model was developed in accordance with the OCR-D Ground Truth Guidelines (Level 2) to ensure compatibility and quality when combined with other datasets. These guidelines focus on correctly segmenting the visual structure of the page, which in this case includes recognizing columns, separators and other layout features.
### Performance
After fine-tuning the model, the model achieved a transcription accuracy of 99.3%, suitable for high quality research data.

Together, the two models work in tandem to accurately segment and transcribe the historical document, overcoming the challenges posed by its complex layout and distinctive fonts.
