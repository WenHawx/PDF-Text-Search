# PDF-Text-Search
Searches a PDF for terms

This web application parses pdf files so they can be searched for a user provided term. 

When the user searches a term, the application returns a list of books that it has in its database, within each book entry, it provides a list of page numbers
that the term appears on. The user can then click on a page number which in turn will open to that page number of the pdf.

NOTE** Books only appear if they are first uploaded to the application.

Code uses python module pdfminer from https://github.com/euske/pdfminer

This web application is coded in HTML and python using flask framework.
