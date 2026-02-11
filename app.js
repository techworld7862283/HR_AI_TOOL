const backendURL =
  location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://hr-ai-tool.onrender.com";

/* ---------------- TABS ---------------- */
document.querySelectorAll(".tab").forEach(tab => {
  tab.onclick = () => {
    document.querySelectorAll(".tab").forEach(t =>
      t.classList.remove("tab-active")
    );
    tab.classList.add("tab-active");

    document.querySelectorAll(".tool").forEach(c =>
      c.classList.add("hidden")
    );

    document.getElementById(tab.dataset.tab)
      .classList.remove("hidden");

    if (tab.dataset.tab === "analytics") {
      loadAnalyticsFromHistory();
    }
  };
});

/* ---------------- DRAG FUNCTION ---------------- */
function drag(drop, input, btn) {
  let file = null;

  drop.onclick = () => input.click();

  input.onchange = e => {
    file = e.target.files[0];
    btn.classList.toggle("button-disabled", !file);
  };

  return () => file;
}

/* ---------------- RESUME ANALYSIS ---------------- */
const getResume = drag(
  document.getElementById("resumeDrop"),
  document.getElementById("resumeFile"),
  document.getElementById("resumeAnalyzeBtn")
);

resumeAnalyzeBtn.onclick = async () => {
  const file = getResume();
  if (!file) return;

  const fd = new FormData();
  fd.append("file", file);

  try {
    const r = await fetch(`${backendURL}/api/resume/analyze_resume`, {
      method: "POST",
      body: fd
    });

    if (!r.ok) throw new Error("Server error");

    const data = await r.json();

    if (typeof data.score !== "number") {
      alert("Analysis failed.");
      return;
    }

    /* ---- Show Score ---- */
    document.getElementById("scoreContainer").classList.remove("hidden");
    document.getElementById("skillsContainer").classList.remove("hidden");

    const scoreBar = document.getElementById("scoreBar");
    const scoreText = document.getElementById("scoreText");

    scoreBar.style.width = data.score + "%";

    if (data.score < 40)
      scoreBar.className = "h-4 rounded-full bg-red-500";
    else if (data.score < 70)
      scoreBar.className = "h-4 rounded-full bg-yellow-400";
    else
      scoreBar.className = "h-4 rounded-full bg-green-500";

    scoreText.textContent = data.score + " / 100";

    /* ---- Skills Heatmap ---- */
    const skillHeatmap = document.getElementById("skillHeatmap");
    skillHeatmap.innerHTML = "";

    Object.entries(data.skills || {}).forEach(([skill, value]) => {
      const div = document.createElement("div");
      div.className =
        "p-2 rounded text-white text-sm font-medium";
      div.style.background =
        `rgb(${255 - value * 2}, ${value * 2}, 120)`;
      div.textContent = `${skill}: ${value}%`;
      skillHeatmap.appendChild(div);
    });

    document.getElementById("resumeResult").textContent =
      data.summary || "";

  } catch (err) {
    alert("Resume analysis failed.");
  }
};

/* ---------------- CSV DOWNLOAD ---------------- */
resumeCsvBtn.onclick = async () => {
  const file = getResume();
  if (!file) return;

  const fd = new FormData();
  fd.append("file", file);

  try {
    const r = await fetch(`${backendURL}/api/resume/analyze_resume_csv`, {
      method: "POST",
      body: fd
    });

    if (!r.ok) {
      alert("CSV generation failed.");
      return;
    }

    const blob = await r.blob();
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "resume_analysis.csv";
    a.click();

  } catch {
    alert("CSV download error.");
  }
};

/* ---------------- TTS WITH VOICE + AUDIO PREVIEW ---------------- */
ttsBtn.onclick = async () => {
  if (!ttsText.value.trim()) {
    alert("Enter text first.");
    return;
  }

  const fd = new FormData();
  fd.append("text", ttsText.value);
  fd.append("voice", document.getElementById("voiceSelect").value);

  try {
    const r = await fetch(`${backendURL}/api/tts/text_to_speech`, {
      method: "POST",
      body: fd
    });

    if (!r.ok) throw new Error();

    const blob = await r.blob();
    const url = URL.createObjectURL(blob);

    document.getElementById("ttsResult").innerHTML = `
      <audio controls class="w-full">
        <source src="${url}" type="audio/mpeg">
      </audio>
      <a href="${url}" download="tts.mp3"
         class="inline-block mt-3 bg-green-600 text-white px-4 py-2 rounded">
         Download Audio
      </a>
    `;

  } catch {
    alert("TTS failed.");
  }
};

/* ---------------- ANALYTICS ---------------- */
async function loadAnalyticsFromHistory() {

  const candidates =
    JSON.parse(localStorage.getItem("analytics_candidates") || "[]");

  if (!candidates.length) {
    document.getElementById("skillChart").innerHTML =
      "<p class='text-gray-500'>No analytics data yet.</p>";
    return;
  }

  try {
    const r = await fetch(`${backendURL}/api/analytics/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ candidates })
    });

    if (!r.ok) throw new Error();

    const data = await r.json();

    document.getElementById("totalCandidates").textContent =
      data.total_candidates || 0;

    document.getElementById("avgScore").textContent =
      data.average_match_score || 0;

    const skillChart = document.getElementById("skillChart");
    skillChart.innerHTML = "";

    Object.entries(data.skill_distribution || {}).forEach(([k, v]) => {
      skillChart.innerHTML +=
        `<div class="bg-blue-100 p-2 rounded">${k}: ${v}</div>`;
    });

    const verdictChart =
      document.getElementById("verdictChart");

    verdictChart.innerHTML = "";

    Object.entries(data.verdict_distribution || {}).forEach(([k, v]) => {
      verdictChart.innerHTML +=
        `<div class="bg-green-100 p-2 rounded">${k}: ${v}</div>`;
    });

  } catch {
    document.getElementById("skillChart").innerHTML =
      "<p class='text-red-500'>Analytics load failed.</p>";
  }
}
