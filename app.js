const backendURL =
  location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://hr-ai-tool.onrender.com";

/* ---------------- TABS ---------------- */
document.querySelectorAll(".tab").forEach(tab => {
  tab.onclick = () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("tab-active"));
    tab.classList.add("tab-active");
    document.querySelectorAll(".tool").forEach(c => c.classList.add("hidden"));
    document.getElementById(tab.dataset.tab).classList.remove("hidden");

    if (tab.dataset.tab === "analytics") {
      loadAnalyticsFromHistory();
    }
  };
});

/* ---------------- DRAG ---------------- */
function drag(drop, input, btn) {
  let file = null;
  drop.onclick = () => input.click();
  input.onchange = e => {
    file = e.target.files[0];
    btn.disabled = !file;
  };
  return () => file;
}

/* ---------------- RESUME ANALYSIS ---------------- */
const getResume = drag(resumeDrop, resumeFile, resumeAnalyzeBtn);

resumeAnalyzeBtn.onclick = async () => {
  const file = getResume();
  if (!file) return;

  const fd = new FormData();
  fd.append("file", file);

  const r = await fetch(`${backendURL}/api/resume/analyze_resume`, {
    method: "POST",
    body: fd
  });

  const data = await r.json();

  if (!data.score && data.score !== 0) {
    alert("Analysis failed.");
    return;
  }

  scoreBar.style.width = data.score + "%";
  scoreText.textContent = data.score + " / 100";

  skillHeatmap.innerHTML = "";
  Object.entries(data.skills).forEach(([s, v]) => {
    skillHeatmap.innerHTML += `<div>${s}: ${v}</div>`;
  });

  resumeResult.textContent = data.summary;
};

/* ---------------- CSV DOWNLOAD ---------------- */
resumeCsvBtn.onclick = async () => {
  const file = getResume();
  if (!file) return;

  const fd = new FormData();
  fd.append("file", file);

  const r = await fetch(`${backendURL}/api/resume/analyze_resume_csv`, {
    method: "POST",
    body: fd
  });

  const blob = await r.blob();
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "resume_analysis.csv";
  a.click();
};

/* ---------------- TTS WITH AUDIO PLAYER ---------------- */
ttsBtn.onclick = async () => {
  const fd = new FormData();
  fd.append("text", ttsText.value);

  const r = await fetch(`${backendURL}/api/tts/text_to_speech`, {
    method: "POST",
    body: fd
  });

  const blob = await r.blob();
  const url = URL.createObjectURL(blob);

  ttsResult.innerHTML = `
    <audio controls src="${url}"></audio>
    <br/>
    <a href="${url}" download="tts.mp3">Download Audio</a>
  `;
};

/* ---------------- ANALYTICS ---------------- */
async function loadAnalyticsFromHistory() {
  const candidates = JSON.parse(localStorage.getItem("analytics_candidates") || "[]");

  if (!candidates.length) {
    analytics.innerHTML = "<p>No analytics data yet.</p>";
    return;
  }

  const r = await fetch(`${backendURL}/api/analytics/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ candidates })
  });

  const data = await r.json();

  totalCandidates.textContent = data.total_candidates;
  avgScore.textContent = data.average_match_score;

  skillChart.innerHTML = "";
  Object.entries(data.skill_distribution).forEach(([k, v]) => {
    skillChart.innerHTML += `<div>${k}: ${v}</div>`;
  });

  verdictChart.innerHTML = "";
  Object.entries(data.verdict_distribution).forEach(([k, v]) => {
    verdictChart.innerHTML += `<div>${k}: ${v}</div>`;
  });
}
