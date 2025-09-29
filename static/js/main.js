function captureFace(face) {
    const formData = new FormData();
    formData.append("face", face);

    fetch("/capture_face", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "ok") {
            document.getElementById(face + "-preview").src = data.url;
        } else {
            alert("Capture failed: " + data.error);
        }
    })
    .catch(err => console.error("Error capturing:", err));
}

function solveCube() {
    fetch("/solve", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.status === "done") {
                document.getElementById("solution").innerText = "Solution: " + data.solution;
            } else {
                document.getElementById("solution").innerText = "Error: " + data.message;
            }
        })
        .catch(err => console.error("Error solving:", err));
}
