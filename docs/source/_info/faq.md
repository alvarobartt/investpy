# Frequent Asked Questions - FAQs

In this section the Frequent Asked Questions are answered, so please read this section before posting a question or openning an issue since duplicates will not be solved or will be referenced to this section. Also, if you think that there are more possible FAQs, consider openning an issue in GitHub so to notify it, since if we all contribute this section can be clear enough so to ease question answering.

## Where can I find the reference of a function and its usage?

Currently the `docs/` are still missing a lot of information, but they can be clear enough so that users can get to know which functions can be used and how. If you feel that any functionallity or feature is not clear enough, please let me know in the issues tab, so that I can explain it properly for newcomers, so that answers are more general and help more users than just the one asking it. Docs can be found at: [Documentation](https://investpy.readthedocs.io/)

## What do I do if the financial product I am looking for is not indexed in investpy?

As it is known, investpy gathers and retrieves data from Investing.com which is a website that contains a lot of financial information. Since investpy relies on Investing.com data, some of it may not be available in Investing, which will mean that it will not be available in investpy either. Anyways, it can be an investpy problem while retrieving data, so on, there is a search function (`investpy.search_quotes(text, products, countries, n_results)`) that can be used for searching financial products that are available in Investing.com but they can not be retrieved using investpy main functions.

## I am having problems while installing the package.

If you followed the [Installation Guide](https://github.com/alvarobartt/investpy/blob/master/README.md#Installation), you should be able to use investpy without having any problem, anyways, if you are stuck on it, open an issue at investpy issues tab so to let the developers know which is your problem in order to solve it as soon as possible. If you were not able to complete the installation, please check that you are running Python 3.5 at least and that you are installing the latest version available, if you are still having problems, open an issue.

## How do I contribute to investpy?

Currently I am not admitting any Pull Request since investpy is under development, and so to keep a clean structure, I will be developing new functionalities until code is clean enough to let newcome contributors help. Anyways, the most effective tool you have in order to contribute to investpy are **issues** where you can give me new ideas or some functionallity you would like to see implemented in investpy. You can also use issues in order to report bugs or problems so to help investpy's development and consistency.

## How do I reference investpy?

Since investpy is an open source Python package, whenever you use it, would be nice from you to mention or comment where does the data comes from. This way, investpy can be spread among more users which will consequently improve package usage since more users can contribute to it due to the increasing reach to newcome developers. A sample reference is presented below:

`investpy - a Python package for Financial Data Extraction from Investing.com developed by Álvaro Bartolomé del Canto, alvarobartt @ GitHub`
