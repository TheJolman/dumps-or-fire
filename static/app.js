
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
  const pop = result[0].popularity;
  scoreContainer.textContent = `Popularity: ${pop} / 100`
})
