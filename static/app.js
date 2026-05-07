function getOrCreate(id, tag = 'div', parent = document.body) {
  let el = document.getElementById(id);
  if (el === null) {
    el = document.createElement(tag);
    el.id = id;
    parent.appendChild(el);
  }
  return el;
}

document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  // const data = new FormData(e.target);
  const response = await fetch("/api/popularity", {
    method: "GET",
    // body: JSON.stringify(Object.fromEntries(data)),
    headers: { "Content-Type": "application/json" },
  });

  const result = await response.json();

  let resultDiv = document.getElementById("result");
  if (resultDiv === null) {
    console.error("could not find score container")
    return;
  }

  getOrCreate('result-artist', 'p', resultDiv).textContent = `Artist: ${result.artist}`
  getOrCreate('result-track', 'p', resultDiv).textContent = `Track: ${result.track}`
  getOrCreate('result-pop', 'p', resultDiv).textContent = `Popularity: ${result.popularity} / 100`
})
