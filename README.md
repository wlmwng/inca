*This is a clone of the "INfrastructure for Content Analysis" package [(INCA)](https://github.com/uvacw/inca).* <br>
>INCA aims to provide a bundle of scraping and analysis functionalities for social scientists. The main goals are to facilitate
 >1. Data collection from websites and social media.
 >2. Basic processing, such as tokenizing, lemmatizing, POS-tagging, NER
 >3. Some analyses such as machine learning or time series analysis

This version of INCA is used as part of the [us-right-media](https://github.com/wlmwng/us-right-media) project. The project is organized in a multi-container Docker environment, where INCA is installed inside a JupyterLab container to assist with data collection, text pre-processing, and news event clustering. To setup the project's containers, please see the instructions in [us-right-media-config](https://github.com/wlmwng/us-right-media-config).
