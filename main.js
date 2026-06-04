const input = document.getElementById("urlInput");
const button = document.getElementById("goButton");

function normalizeInput(value){
    value = value.trim();

    if(!value){
        return "";
    }

    const youtubeIdRegex = /^[a-zA-Z0-9_-]{11}$/;

    if(youtubeIdRegex.test(value)){
        return `https://www.youtube.com/watch?v=${value}`;
    }

    if(!/^https?:\/\//i.test(value)){
        return "https://" + value;
    }

    return value;
}

button.addEventListener("click", () => {
    const normalizedUrl = normalizeInput(input.value);

    console.log(normalizedUrl);

    /*
    fetch("/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: normalizedUrl
        })
    });
    */
});

input.addEventListener("keydown", e => {
    if(e.key === "Enter"){
        button.click();
    }
});
