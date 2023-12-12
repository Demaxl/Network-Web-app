const posts = {};

function showMessage(text, type) {
    const html =  `

        <div class="alert alert-${type} alert-dismissible fade show m-3" role="alert">
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            ${text}
        </div>
    `
    // Create a temporary container element
    const tempContainer = document.createElement('div');

    // Set the innerHTML of the container to your HTML string
    tempContainer.innerHTML = html;

    // Get the first child of the container (the created div element)
    const alertElement = tempContainer.firstElementChild;

    // Get the target element where you want to append the new element
    const targetElement = document.querySelector('.body'); // Adjust the selector as needed

    // Insert the new element before the content
    targetElement.insertAdjacentElement('beforebegin', alertElement);
}

async function toggleFollow(btn) {
    const response = await fetch(apiURLS['FOLLOW_URL'], {
        method: "POST",
        headers: {
            "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        mode: "same-origin",

        body: JSON.stringify({
            "username": btn.dataset.username,
            "action": btn.dataset.action
        })
    });

    const followerCount = document.getElementById("follower-count");

    if (btn.dataset.action == "FOLLOW") {
        btn.innerHTML = "Unfollow"
        btn.dataset.action = "UNFOLLOW"
        followerCount.innerHTML = parseInt(followerCount.innerHTML) + 1
    } else {
        btn.innerHTML = "Follow"
        btn.dataset.action = "FOLLOW"
        followerCount.innerHTML = parseInt(followerCount.innerHTML) - 1

    }
}


function editPost(btn) {
    const div = btn.parentNode;
    // const div = document.querySelector(".post-container");
    const poster = div.querySelector(".post-poster");
    const body = div.querySelector(".post-body");
    const id = div.dataset.postId;

    posts[id] = div.outerHTML;

    div.outerHTML = `
        <div class="border my-3 p-3 post-container" data-post-id="${id}">
            <h4>${poster.innerHTML}</h4>
            <textarea class="form-control" rows="5">${body.innerHTML}</textarea>
            <button type="button" class="btn btn-primary mt-3" onclick="editPostRequest(this.parentNode)">Edit Post</button>
            <button type="button" class="btn btn-outline-primary mt-3" onclick="this.parentNode.outerHTML = posts['${id}']">Cancel</button>

        </div>
    `    
}

async function editPostRequest(div) {
    // const div = document.querySelector(".post-container");
    const post = div.querySelector("textarea").value

    const response = await fetch(apiURLS['EDIT_URL'], {
        method: "PUT",
        headers: {
            "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        mode: "same-origin",

        body: JSON.stringify({
            postId: div.dataset.postId,
            postBody: post
        })
    })

    const json = await response.json();
    
    if (json.hasOwnProperty("success")) {
        div.outerHTML = json['post']

    }

}


async function likePost(btn, postId) {
    const response = await fetch(apiURLS['LIKE_URL'], {
        method: "POST",
        headers: {
            "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
        },
        mode: "same-origin",
        body: JSON.stringify({
            "postId": postId
        })
    });

    const json = await response.json();

    if (json.hasOwnProperty("success")) {
        const status = json['status']
        const div = document.querySelector(`#post-${postId}`)

        div.outerHTML = json['post']
    
    } else {
        showMessage(json['error'], "danger")
    }
}