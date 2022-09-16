function openSelect(file)
{
  (file).trigger('click');
}

function getSearchTerm()
{
	var inputTerm = document.getElementById('query').value;
	console.log(inputTerm)
}

function loadSearch()
{
	var searchButton = document.getElementById('searchButton');
	searchButton.addEventListener('click', getSearchTerm, false);
}
