
document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  // const data = new FormData(e.target);
  const res = await fetch("/api/popularity", {
    method: "GET",
    // body: JSON.stringify(Object.fromEntries(data)),
    headers: { "Content-Type": "application/json" },
  });

  const result = await res.json();

  let scoreContainer = document.getElementById("result");
  if (scoreContainer === null) {
    console.error("could not find score container")
    return;
  }
  let artistText = document.createElement("p");
  artistText.textContent = `Artist: ${result.artist}`
  scoreContainer.appendChild(artistText);

  let trackText = document.createElement("p");
  trackText.textContent = `Track: ${result.track}`
  scoreContainer.appendChild(trackText);

  popRatio = document.createElement("p");
  popRatio.textContent = `Popularity: ${result.popularity} / 100`;
  scoreContainer.appendChild(popRatio);
})
