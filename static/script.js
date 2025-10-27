document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const response = await fetch("/upload", { method: "POST", body: formData });

    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "compressed.png";
        link.click();
    } else {
        alert("Error compressing image!");
    }
});
