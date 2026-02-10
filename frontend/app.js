const backendURL = location.hostname === "localhost" ? "http://localhost:8000" : "";

// --------- Tabs ----------
document.querySelectorAll(".tab").forEach(tab => {
  tab.onclick = () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("tab-active"));
    tab.classList.add("tab-active");
    document.querySelectorAll(".tool").forEach(c => c.classList.add("hidden"));
    document.getElementById(tab.dataset.tab).classList.remove("hidden");
  };
});

// --------- Drag & Drop Helper ----------
function drag(drop, input, btn) {
  let file = null;
  drop.onclick = () => input.click();
  drop.ondragover = e => { e.preventDefault(); drop.classList.add("drag-over"); };
  drop.ondragleave = () => drop.classList.remove("drag-over");
  drop.ondrop = e => { e.preventDefault(); drop.classList.remove("drag-over"); handle(e.dataTransfer.files[0]); };
  input.onchange = e => handle(e.target.files[0]);

  function handle(f) {
    file = null;
    btn.classList.add("button-disabled");
    if(!f) return;
    file = f;
    btn.classList.remove("button-disabled");
  }
  return () => file;
}

// PDF → Word
const getPdf = drag(pdfDrop, pdfFile, pdfBtn);
pdfBtn.onclick = async () => {
  const fd = new FormData(); fd.append("file", getPdf());
  const r = await fetch(`${backendURL}/api/pdf/pdf_to_word`, { method: "POST", body: fd });
  const b = await r.blob();
  const a = document.createElement("a");
  a.href = URL.createObjectURL(b); a.download = "converted.docx"; a.textContent = "Download PDF→Word";
  pdfResult.innerHTML = ""; pdfResult.appendChild(a);
};

// Word → PDF
const getWord = drag(wordDrop, wordFile, wordBtn);
wordBtn.onclick = async () => {
  const fd = new FormData(); fd.append("file", getWord());
  const r = await fetch(`${backendURL}/api/word/word-to-pdf`, { method: "POST", body: fd });
  const b = await r.blob();
  const a = document.createElement("a");
  a.href = URL.createObjectURL(b); a.download = "converted.pdf"; a.textContent = "Download Word→PDF";
  wordResult.innerHTML = ""; wordResult.appendChild(a);
};

// Resume / HR Analysis
const getResume = drag(resumeDrop, resumeFile, resumeAnalyzeBtn);
resumeAnalyzeBtn.onclick = async () => {
  const fd = new FormData(); fd.append("file", getResume());
  const r = await fetch(`${backendURL}/api/resume/analyze_resume`, { method: "POST", body: fd });
  const data = await r.json();

  document.getElementById("scoreContainer").classList.remove("hidden");
  document.getElementById("skillsContainer").classList.remove("hidden");

  const scoreBar = document.getElementById("scoreBar");
  scoreBar.style.width = data.score + "%";
  scoreBar.className = "h-4 rounded-full " + (data.score<40?"bg-red-500":data.score<70?"bg-yellow-400":"bg-green-500");
  document.getElementById("scoreText").textContent = data.score + " / 100";

  const skillHeatmap = document.getElementById("skillHeatmap");
  skillHeatmap.innerHTML = "";
  Object.entries(data.skills).forEach(([s,v])=>{
    const div = document.createElement("div");
    div.className = "p-2 rounded text-white";
    div.style.background = `rgb(${255-v*2},${v*2},100)`;
    div.innerHTML = `<b>${s}</b>: ${v}%`;
    skillHeatmap.appendChild(div);
  });

  resumeResult.textContent = data.summary;
};

// Download CSV
resumeCsvBtn.onclick = async () => {
  resumeCsvBtn.onclick = async () => {
 const file = getResume()
  if (!file) return

  const fd = new FormData()
  fd.append("file", file)

  const r = await fetch(
    backendURL + "/api/resume/analyze_resume_csv",
    { method: "POST", body: fd }
  )

  if (!r.ok) {
    alert("CSV generation failed")
    return
  }

  const blob = await r.blob()
  download(blob, "resume_analysis.csv", resumeResult)
}
  const fd = new FormData(); fd.append("file", getResume());
  const r = await fetch(`${backendURL}/api/resume/analyze_resume_csv`, { method: "POST", body: fd });
  const b = await r.blob();
  const a = document.createElement("a");
  a.href = URL.createObjectURL(b); a.download = "resume_analysis.csv"; a.textContent = "Download CSV";
  resumeResult.innerHTML = ""; resumeResult.appendChild(a);
};

// TTS
ttsBtn.onclick = async () => {
  const fd = new FormData(); fd.append("text", ttsText.value);
  const r = await fetch(`${backendURL}/api/tts/text_to_speech`, { method: "POST", body: fd });
  const b = await r.blob();
  const a = document.createElement("a");
  a.href = URL.createObjectURL(b); a.download = "tts.mp3"; a.textContent = "Download Audio";
  ttsResult.innerHTML = ""; ttsResult.appendChild(a);
};
async function loadAnalytics(candidates) {
  const r = await fetch(
    backendURL + "/api/analytics/analyze",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ candidates })
    }
  )

  const data = await r.json()

  totalCandidates.textContent = data.total_candidates
  avgScore.textContent = data.average_match_score

  skillChart.innerHTML = ""
  Object.entries(data.skill_distribution).forEach(([k,v])=>{
    skillChart.innerHTML += `
      <div>${k}: ${v}</div>
    `
  })

  verdictChart.innerHTML = ""
  Object.entries(data.verdict_distribution).forEach(([k,v])=>{
    verdictChart.innerHTML += `
      <div>${k}: ${v}</div>
    `
  })
}
localStorage.setItem("candidates", JSON.stringify(results))
async function loadAnalyticsFromHistory() {
  const candidates = JSON.parse(
    localStorage.getItem("analytics_candidates") || "[]"
  )

  if (!candidates.length) {
    document.getElementById("analytics").innerHTML =
      "<p class='text-gray-500'>No analytics data yet.</p>"
    return
  }

  const r = await fetch(
    backendURL + "/api/analytics/analyze",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ candidates })
    }
  )

  const data = await r.json()

  document.getElementById("totalCandidates").textContent =
    data.total_candidates
  document.getElementById("avgScore").textContent =
    data.average_match_score

  const skillChart = document.getElementById("skillChart")
  skillChart.innerHTML = ""
  Object.entries(data.skill_distribution).forEach(([k, v]) => {
    skillChart.innerHTML += `<div>${k}: ${v}</div>`
  })

  const verdictChart = document.getElementById("verdictChart")
  verdictChart.innerHTML = ""
  Object.entries(data.verdict_distribution).forEach(([k, v]) => {
    verdictChart.innerHTML += `<div>${k}: ${v}</div>`
  })
}
