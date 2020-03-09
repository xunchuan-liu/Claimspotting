// Perform changes after page has loaded
function init() {
	getDate()
	readJSON()
	setTimeout(savePage, 1000)	
}

// Read JSON data from server
// Fills in the data to the HTML	
function readJSON() {	
	$.getJSON("http://127.0.0.1:5000/claimspotting", function(data) {
		var claims = []
		var excerpts = []
		var links = []
		for (x of data) {
			claims.push(x[2])
			excerpts.push(x[5])
			links.push(x[6])			
		}
		fillData(claims, excerpts, links)
	})	
}

// Saves the completed newsletter after writing dynamic content
function savePage() {
	var blob = new Blob([$("html").html()], {type: "text/html;charset=utf-8"})
	saveAs(blob, "newsletter.html")
}


// Sets the date for the newsletter
// Modifies margin for styling
function getDate() {
	var today = new Date()
	var year = today.getFullYear().toString()
	var month = (today.getMonth() + 1).toString()
	var day = today.getDate().toString()

	var date = month+"/"+day+"/"+year
	document.getElementById("date").innerHTML = date

	document.getElementById("date").style.margin = "0px"
}

// Write claims, excerpts, and links to the newsletter
function fillData(c, e, l) {
	var claims = document.getElementsByClassName("claim")
	var excerpts = document.getElementsByClassName("context")
	var links = document.getElementsByClassName("link")	
	
	for (i = 0; i < claims.length; i++) {
		claims[i].innerHTML = c[i]
		excerpts[i].innerHTML = e[i]
		links[i].href = l[i]
	}
}

//$(document).ready(init)



