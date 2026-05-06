function createAddChildText(parent) {
  return (text) => {
    let p = document.createElement("p");
    p.textContent = text
    parent.appendChild(p);
  }
}

document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  // const data = new FormData(e.target);
  const res = await fetch("/api/popularity", {
    method: "GET",
    // body: JSON.stringify(Object.fromEntries(data)),
    headers: { "Content-Type": "application/json" },
  });

  const result = await res.json();

  let resultDiv = document.getElementById("result");
  if (resultDiv === null) {
    console.error("could not find score container")
    return;
  }
  const addResults = createAddChildText(resultDiv)

  addResults(`Artist: ${result.artist}`);
  addResults(`Track: ${result.track}`);
  addResults(`Popularity: ${result.popularity} / 100`);
})
