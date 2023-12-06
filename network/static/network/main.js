

async function toggleFollow(btn) {
    const response = await fetch(btn.dataset.apiUrl, {
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