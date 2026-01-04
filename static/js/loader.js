function showLoader(text = "Carregando...") {
    const loader = document.getElementById("global-loader");
    loader.querySelector("span").textContent = text;
    loader.classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("global-loader").classList.add("hidden");
}
