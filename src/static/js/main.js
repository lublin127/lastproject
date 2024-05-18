function confirmDelete() {
    const ok = confirm("Are you sure you want to delete vacation permanently?")
    if(!ok) event.preventDefault();
}

const errorSpan= document.querySelector(".error");
if(errorSpan) {
    setTimeout(() => {
        errorSpan.parentNode.removeChild(errorSpan);
    }, 4000);
}


// Function to color liked buttons on page load
window.addEventListener('load', function() {
    document.querySelectorAll('.likeButton').forEach(button => {
        var vacationId = button.getAttribute('data-id');
        var isLiked = sessionStorage.getItem('liked_' + vacationId);
        if (isLiked === 'true') {
            button.style.backgroundColor = "#df437b"; // Color liked buttons to #df437b
        }
    });
});

// Function to color liked buttons on page load
window.addEventListener('load', function() {
    document.querySelectorAll('.likeButton').forEach(button => {
        var vacationId = button.getAttribute('data-id');
        var isLiked = sessionStorage.getItem('liked_' + vacationId);
        if (isLiked === 'true') {
            button.style.backgroundColor = "#df437b"; // Color liked buttons to #df437b
        }
    });
});

// Function to handle like button clicks
document.querySelectorAll('.likeButton').forEach(button => {
    button.addEventListener('click', function() {
        var vacationId = this.getAttribute('data-id');
        var url = "/vacations/like/" + vacationId;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    let response = JSON.parse(xhr.responseText);
                    let newLikesCount = response.new_likes_count;
                    let isLiked = response.is_liked;

                    // Update button color if liked
                    if (isLiked) {
                        button.style.backgroundColor = "#df437b"; // Color liked button to #df437b
                    } else {
                        button.style.backgroundColor = ""; // Remove inline style for background color
                    }

                    // Save liked status to session storage
                    sessionStorage.setItem('liked_' + vacationId, isLiked);

                    // Create a new SVG element for the heart icon
                    let heartIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                    heartIcon.setAttribute("xmlns", "http://www.w3.org/2000/svg");
                    heartIcon.setAttribute("width", "16");
                    heartIcon.setAttribute("height", "16");
                    heartIcon.setAttribute("fill", "white");
                    heartIcon.setAttribute("class", "bi bi-heart-fill heart-icon");
                    heartIcon.setAttribute("viewBox", "0 0 16 16");

                    // Create the path element for the heart shape
                    let path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    path.setAttribute("fill-rule", "evenodd");
                    path.setAttribute("d", "M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314");

                    // Append the path element to the SVG
                    heartIcon.appendChild(path);

                    // Update the like button content with the heart icon and new likes count
                    button.innerHTML = '';
                    button.appendChild(heartIcon);
                    button.insertAdjacentHTML('beforeend', ' ' + newLikesCount + ' Likes');
                }
            }
        };
        xhr.send();
    });
});

window.onload = function() {
    // Get the element containing the date strings
    var dateElement = document.querySelector('.card-date');
    
    // Extract the date strings from the element's text content
    var dateStrings = dateElement.textContent.split('<br>');

    // Extract the start and end date strings
    var fromDateStr = dateStrings[0].split(': ')[1];
    var toDateStr = dateStrings[1].split(': ')[1];

    // Convert date strings to Date objects
    var fromDate = new Date(fromDateStr);
    var toDate = new Date(toDateStr);

    // Format the dates
    var options = { month: 'long', day: 'numeric' };
    var fromFormatted = fromDate.toLocaleDateString('en-US', options);
    var toFormatted = toDate.toLocaleDateString('en-US', options);

    // Update the text content of the element with formatted dates
    dateElement.innerHTML = "From: " + fromFormatted + "<br> To: " + toFormatted;
};
