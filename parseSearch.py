import os, re, sys, subprocess, webbrowser
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed



def pdfParser(fileName):
	tempFileName = "./pdf_files/" + fileName
	fp = open(tempFileName, 'rb')
	parser = PDFParser(fp)  
	document= PDFDocument(parser)

	#take of .pdf extension
	tempName = fileName[:-3]
	#save as new textFile of same name
	newFileName ='./textFiles/' + tempName + 'txt'

	if not document.is_extractable:
		raise PDFTextExtractionNotAllowed
	else:
		rsrcmgr=PDFResourceManager()
		laparams=LAParams()
		device=PDFPageAggregator(rsrcmgr,laparams=laparams)
		interpreter=PDFPageInterpreter(rsrcmgr,device)
		#parses each page of pdf
		for page in PDFPage.create_pages(document):
			interpreter.process_page(page)
			layout=device.get_result()
			output=str(layout)
			for x in layout:
				if (isinstance(x,LTTextBoxHorizontal)):
					text=x.get_text()
					output+=text
					output=re.sub('\s','',output)
			with open(newFileName,'a',encoding='utf-8') as f:
				#writes out to a text file with same name as pdf file
				f.write(output)
		fp.close()
	
	
def wordSearch(word):
	wordToSearch = word
	file_list = []
	list_of_page_dict = []
	word = "Search: " + word

	#This url is where pdf_files are stoed after uploading them to be parsed for the word search
	url_link = ""

	#Take out whitespace characters
	wordToSearch = wordToSearch.replace(" ","")

	if(wordToSearch.isalnum()):
		for root, directory, files in os.walk('./textFiles/'):
			#walks through each file in textFiles/
			for name in files:
				with open(os.path.join(root,name),encoding='utf-8') as opened_file:
					text_list= opened_file.read().split('<LTPage')
					opened_file.close()
					n=len(text_list)
					page_dict = {}
					for itr in range(1,n):
						#if term is found within text file and page
							#page number is appended to page_list
						if wordToSearch in text_list[itr]:
							# key value pair is appended to dictionary, key = page number, value = hyperlink

							page_dict[itr] = "https://www." + url_link + name[:-4] + ".pdf#page=" + str(itr)
					if page_dict:
						file_list.append(name[:-4])
						list_of_page_dict.append(page_dict)
					length_of_list = len(file_list)
				
		return word, file_list, list_of_page_dict, length_of_list
	else:
		return "You've entered an invalid search term"


def pdfOpen(pdf_to_open):
	path_to_pdf = 'pdf_files/' + os.sep + pdf_to_open + '.pdf'
	#opens pdf in clients default browser
	webbrowser.open_new(path_to_pdf)

