function toggleDropdown() {
    var regionSelection = document.getElementById("regionSelection");
    var shelterButton = document.getElementById("shelterButton");

    if (regionSelection.style.display === "none" || regionSelection.style.display === "") {
        var rect = shelterButton.getBoundingClientRect();
        regionSelection.style.left = rect.right + "px";
        regionSelection.style.top = rect.top + "px";
        regionSelection.style.display = "block";
    } else {
        regionSelection.style.display = "none";
    }
}

document.addEventListener("click", function(event) {
    var isClickInsideButton = document.getElementById("shelterButton").contains(event.target);
    var isClickInsideDropdown = document.getElementById("regionSelection").contains(event.target);

    if (!isClickInsideButton && !isClickInsideDropdown) {
        document.getElementById("regionSelection").style.display = "none";
    }
});