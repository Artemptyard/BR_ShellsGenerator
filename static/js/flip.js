// JavaScript to rotate the card after 3 seconds
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        rotateCard();
    }, 1500); // 3000 milliseconds (3 seconds)

    function rotateCard() {
        var card = document.getElementById("myCard1");
        card.style.transform = "rotateX(180deg)";
        card = document.getElementById("myCard2");
        card.style.transform = "rotateX(180deg)";
    }
});