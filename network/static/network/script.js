document.addEventListener('DOMContentLoaded', function () {

    let newPost = document.querySelector('#post_content');
    if (newPost) {
        this.addEventListener('keyup', counter);
    }

    document.querySelectorAll('.like_btn').forEach(btn => {
        btn.addEventListener('click', like_post);
    });

    document.querySelectorAll('.edit_btn').forEach(btn => {
        btn.addEventListener('click', edit_post);
    });
});


// Like/unlike post
function like_post() {

    fetch(`posts/${this.id}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
    
    let counter = parseInt(this.nextElementSibling.textContent);

    if (this.className === "like_btn bi-suit-heart-fill") {
        this.className = "like_btn bi-suit-heart";
        this.style.color = "gray";
        this.nextElementSibling.innerHTML = counter - 1;
    } else {
        this.className = "like_btn bi-suit-heart-fill";
        this.style.color = "red";
        this.nextElementSibling.innerHTML = counter + 1;
    }
}



// Edit Post
function edit_post() {
    let edit_btn = this;
    edit_btn.style.display = "none";

    let paragraph = this.nextElementSibling;
    let oldContent = paragraph.textContent;

    // Replace the paragraph with a form with textarea
    let form = document.createElement("form");

    let text_area = document.createElement("textarea");
    text_area.className = "form-control my-2";
    text_area.textContent = oldContent;
    text_area.setAttribute("maxlength", 250);
    text_area.setAttribute("rows", 4);
    let update_btn = document.createElement("button");
    update_btn.innerHTML = "Update"
    update_btn.className = "btn btn-sm btn-primary mr-2";
    let cancel_btn = document.createElement("button");
    cancel_btn.className = "btn btn-sm btn-secondary";
    cancel_btn.innerHTML = "Cancel"

    form.appendChild(text_area);
    form.appendChild(update_btn);
    form.appendChild(cancel_btn);

    paragraph.replaceWith(form);

    // Cancel Edit Post
    cancel_btn.addEventListener("click", function(event) {
        event.preventDefault();
        edit_btn.style.display = "inline";
        form.replaceWith(paragraph);
        paragraph.textContent = oldContent;
    })

    // Update Post and save it to Database
    update_btn.addEventListener("click", function(event) {
        event.preventDefault()
        let newContent = text_area.value;
        fetch(`posts/${edit_btn.dataset.post}`, {
            method: 'POST',
            body: JSON.stringify({
                content: newContent
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            edit_btn.style.display = "inline";
            form.replaceWith(paragraph);
            paragraph.textContent = newContent;
        });
    })

}


// Remaining characters counter + enable/disable submit button
function counter() {

    let text_area = document.querySelector('#post_content');
    let submit_btn = document.querySelector('.submit-btn');
    let counter = document.querySelector('#counter');

    if (text_area.value != "") {
        submit_btn.disabled = false,
            submit_btn.style.cursor = "poniter",
            counter.innerHTML = text_area.value.length - 250;
    } else {
        submit_btn.disabled = true,
            counter.innerHTML = '';
    }
}
