var filterPanel;
var recipePanel;
var ingredPanel;
var recipeDialog;
var tagArea;
var activeTagArea;
var searchField;
var resultArea;
var appliedTags = [];

(function init() {
    filterPanel = document.getElementById("filter");
    recipePanel = document.getElementById("recipe");
    ingredPanel = document.getElementById("ingredients");
    recipeDialog = document.getElementById("newRecipeWindow");
    tagArea = document.getElementById("tagArea");
    activeTagArea = document.getElementById("activeTagArea");
    resultArea = document.getElementById('resultArea');

    var saveDishButton = document.getElementById('newRecipeButton');
    saveDishButton.addEventListener('click', saveRecipe, true);

    var openButton = document.getElementById("openRecipeDialog");
    openButton.addEventListener('click', toggleRecipeDialog, true);

    var closeButton = document.getElementById("closeRecipeButton");
    closeButton.addEventListener('click', toggleRecipeDialog, true);

    var clearButton = document.getElementById("clearRecipeButton");
    clearButton.addEventListener('click', handleClearRecipe, true);
    filterPanel.addEventListener('click', toggleFilterPanel, false);

    var searchButton = document.getElementById("searchButton");
    searchButton.addEventListener('click', handleSearchEvent, true);

    var importButton = document.getElementById("recipeFromFile");
    importButton.addEventListener('click', handleImportEvent, true);

    searchField = document.getElementById("searchText");
    searchField.addEventListener('click', handleSearchInput, true);
    searchField.addEventListener('keypress',
				 function(evt) {
				     if (evt.keyCode == 13) {
					 handleSearchEvent(evt);
					 return false;
				     }
				 },
				 true
				);
    resetInput();
})();


function handleSearchEvent(evt) {
    var searchTerm = searchField.value;
    evt = evt || event;
    evt.stopPropagation();
    python.searchDB(searchTerm);
}


function handleImportEvent(evt) {
    evt = evt || event;
    evt.stopPropagation();
    python.importFromFile();
}


function handleSearchInput(evt) {
    evt = evt || event;
    evt.stopPropagation();
}


var filterPanelOpen = true;
function toggleFilterPanel(evt) {
    if (filterPanelOpen) {
	filterPanel.setAttribute("style", "left: -30%;");
	ingredPanel.setAttribute("style", "left: 3%;");
	recipePanel.setAttribute("style", "left: 36%;");
    }
    else {
	filterPanel.setAttribute("style", "left: 0;");
	ingredPanel.setAttribute("style", "left: 33%;");
	recipePanel.setAttribute("style", "left: 66%;");
    }
    evt = evt || event;
    evt.stopPropagation();
    filterPanelOpen = !filterPanelOpen;
}


var recipeDialogOpen = false;
function toggleRecipeDialog(evt) {
    if (recipeDialogOpen) {
	recipeDialog.setAttribute("style", "visibility:hidden;");
    }
    else {
	recipeDialog.setAttribute("style", "visibility:visible;");
    }
    evt = evt || event;
    evt.stopPropagation();
    recipeDialogOpen = !recipeDialogOpen;
}


function saveRecipe(evt) {
    var rcpName = document.getElementById("name").value;
    var fldIngr = document.getElementById("ingr");
    var rcpIngr = fldIngr.value;
    var rcpRcpe = document.getElementById("rcpe").value;
    var rcpTags = document.getElementById("tagInput").value;
    resetInput();
    evt = evt || event;
    evt.stopPropagation();
    python.newRecipe(rcpName, rcpIngr, rcpRcpe, rcpTags);
    alert("Rezept hinzugefügt: " + name);
}


function resetInput() {
    document.getElementById("name").value = "Name des Gerichts";
    document.getElementById("ingr").value = "Zutaten";
    document.getElementById("rcpe").value = "Zubereitung";
    document.getElementById("tagInput").vale = "tag,tag,...";
}


function handleAddTagEvent(evt) {
    python.applyTag(text);
    evt = evt || event;
    evt.stopPropagation();
}


function handleClearRecipe(evt) {
    evt = evt || event;
    evt.stopPropagation();
    resetInput();
}


var addTag = function(text) {
    var ttag = document.createElement("a");
    ttag.setAttribute("class", "tagBox");
    ttag.setAttribute("id", text);
    ttag.innerHTML = text + " ";
    ttag.addEventListener(
	'click',
	function(evt) {
	    evt.stopPropagation();
	    addAppliedTag(text);
	},
	true
    );
    tagArea.appendChild(ttag);
}


function addAppliedTag(text) {
    if (appliedTags.indexOf(text) >= 0) {
	return;
    }
    activeTagArea.setAttribute("style", "visibility:visible;");
    var ttag = document.createElement("a");
    ttag.setAttribute("class", "tagBox");
    ttag.setAttribute("name", text);
    ttag.innerHTML = text + " ";
    ttag.addEventListener(
	'click',
	function(evt) {
	    evt.stopPropagation();
	    removeTag(text);
	},
	true
    );
    appliedTags.push(text);
    activeTagArea.appendChild(ttag);
    python.applyTag(text);
}


function removeTag(text) {
    var ttags =  document.getElementsByName(text);
    var ttag = ttags[0];
    activeTagArea.removeChild(ttag);
    appliedTags.splice( appliedTags.indexOf(text), 1 ); // remove element from array
    if (appliedTags.length == 0) {
	activeTagArea.setAttribute("style", "visibility: hidden");
    }
    python.removeTag(text);
}

function clearResults() {
    while (resultArea.lastChild) {
	resultArea.removeChild( resultArea.lastChild );
    }
}

function clearAppliedTags() {
    while (activeTagArea.lastChild) {
	activeTagArea.removeChild( activeTagArea.lastChild );
    }
}

function clearAvailableTags() {
    while (tagArea.lastChild) {
	tagArea.removeChild( tagArea.lastChild );
    }
}

function addResult(id, title) {
    var dish = document.createElement('a')
    dish.setAttribute("class", "rlink");
    dish.innerHTML = title + " ";
    dish.addEventListener(
	'click',
	function(evt) {
	    python.openRecipe(id);
	    evt = evt || event;
	    evt.stopPropagation();
	},
	true);
    resultArea.appendChild(dish);
    resultArea.appendChild( document.createElement('br') );
}


function displayDish(title, ingreds, recipe) {
    var ingrField = ingredPanel.getElementsByTagName("div")
    ingrField[0].innerHTML = "<h3>Zutaten:</h3>" + ingreds;
    var rcpeField = recipePanel.getElementsByTagName("div")
    rcpeField[0].innerHTML = "<h2>" + title + "</h2>" + recipe;
}
