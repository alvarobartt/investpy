## ❓ Discussions (Q&A, AMA)

GitHub recently released a new feature named __GitHub Discussions__ (still in beta). GitHub Discussions is a 
collaborative communication forum for the community around an open source project.

Check the investpy GitHub Discussions page at [Discussions](https://github.com/alvarobartt/investpy/discussions), 
and feel free to ask me (ar any developer) anything, share updates, have open-ended conversations, and follow along 
on decisions affecting the community's way of working.

📌 __Note__. Usually I don't answer emails asking me questions about investpy, as we currently have the
GitHub Discussions tab, and I encourage you to use it. GitHub Discussions is the easiest way to contact me about 
investpy, so that I don't answer the same stuff more than once via email, as anyone can see the opened/answered
discussions.

Also, in this section some Frequent Asked Questions are answered, so please read this section before posting a 
question or openning an issue since duplicates will not be solved or will be referenced to this section. Also, 
if you think that there are more possible FAQs, consider openning an issue in GitHub so to notify it, since if we 
all contribute this section can be clear enough so to ease question answering.

__Where can I find the reference of a function and its usage?__

Currently the `docs/` are still missing a lot of information, but they can be clear enough so that users can get to know which functions can be used and how. If you feel that any functionallity or feature is not clear enough, please let me know in the issues tab, so that I can explain it properly for newcomers, so that answers are more general and help more users than just the one asking it. Docs can be found at: [Documentation](https://investpy.readthedocs.io/)

__What do I do if the financial product I am looking for is not indexed in investpy?__

As it is known, investpy gathers and retrieves data from Investing.com which is a website that contains a lot of financial information. Since investpy relies on Investing.com data, some of it may not be available in Investing, which will mean that it will not be available in investpy either. Anyways, it can be an investpy problem while retrieving data, so on, there is a search function (`investpy.search_quotes(text, products, countries, n_results)`) that can be used for searching financial products that are available in Investing.com but they can not be retrieved using investpy main functions.

__I am having problems while installing the package.__

If you followed the [Installation Guide](https://github.com/alvarobartt/investpy/blob/master/README.md#Installation), you should be able to use investpy without having any problem, anyways, if you are stuck on it, open an issue at investpy issues tab so to let the developers know which is your problem in order to solve it as soon as possible. If you were not able to complete the installation, please check that you are running at least Python 3.6 and that you are installing the latest version available, if you are still having problems, open an issue.

__How do I contribute to investpy?__

As this is an open-source project it is **open to contributions, bug reports, bug fixes, documentation improvements, 
enhancements, and ideas**. There is an open tab of [issues](https://github.com/alvarobartt/investpy/issues) where 
anyone can open new issues if needed or navigate through them to solve them or contribute to its solving. 
Remember that issues are not threads to describe multiple problems, this does not mean that issues can not 
be discussed, but so to keep structured project management, the same issue should not describe different 
problems, just the main one and some nested/related errors that may be found.
