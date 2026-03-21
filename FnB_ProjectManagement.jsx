import { useState } from "react";

const COLORS = {
  bg: "#0D1117",
  surface: "#161B22",
  surfaceHover: "#1C2333",
  border: "#30363D",
  accent: "#00C9A7",
  accentDim: "#00c9a720",
  accentHover: "#00b896",
  text: "#E6EDF3",
  textMuted: "#8B949E",
  student: "#4FC3F7",
  teacher: "#CE93D8",
  admin: "#FFCC80",
  danger: "#F85149",
  success: "#3FB950",
  warn: "#D29922",
};

const styles = {
  app: {
    fontFamily: "'DM Sans', 'Segoe UI', sans-serif",
    background: COLORS.bg,
    minHeight: "100vh",
    color: COLORS.text,
  },
  // AUTH
  authWrap: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    background: `radial-gradient(ellipse at 60% 0%, #00c9a710 0%, transparent 60%), ${COLORS.bg}`,
  },
  authCard: {
    background: COLORS.surface,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 16,
    padding: "40px 44px",
    width: 400,
    boxShadow: "0 24px 48px #00000080",
  },
  authLogo: {
    fontSize: 28,
    fontWeight: 800,
    letterSpacing: -1,
    color: COLORS.accent,
    marginBottom: 4,
  },
  authSub: { fontSize: 13, color: COLORS.textMuted, marginBottom: 32 },
  label: { fontSize: 12, color: COLORS.textMuted, marginBottom: 6, display: "block", letterSpacing: 0.5, textTransform: "uppercase" },
  input: {
    width: "100%",
    background: COLORS.bg,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 8,
    padding: "10px 14px",
    color: COLORS.text,
    fontSize: 14,
    outline: "none",
    boxSizing: "border-box",
    marginBottom: 16,
    transition: "border-color 0.2s",
  },
  roleGrid: { display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 10, marginBottom: 20 },
  roleBtn: (active, color) => ({
    padding: "10px 8px",
    borderRadius: 8,
    border: `1.5px solid ${active ? color : COLORS.border}`,
    background: active ? color + "18" : COLORS.bg,
    color: active ? color : COLORS.textMuted,
    fontWeight: 600,
    fontSize: 13,
    cursor: "pointer",
    textAlign: "center",
    transition: "all 0.2s",
  }),
  btn: (variant = "primary") => ({
    width: "100%",
    padding: "11px 0",
    borderRadius: 8,
    border: "none",
    background: variant === "primary" ? COLORS.accent : COLORS.surface,
    color: variant === "primary" ? "#0D1117" : COLORS.text,
    fontWeight: 700,
    fontSize: 14,
    cursor: "pointer",
    letterSpacing: 0.3,
    transition: "background 0.2s",
  }),
  // LAYOUT
  layout: { display: "flex", minHeight: "100vh" },
  sidebar: {
    width: 220,
    background: COLORS.surface,
    borderRight: `1px solid ${COLORS.border}`,
    display: "flex",
    flexDirection: "column",
    padding: "24px 0",
    position: "fixed",
    top: 0,
    bottom: 0,
    left: 0,
  },
  sidebarLogo: { padding: "0 20px 24px", fontSize: 20, fontWeight: 800, color: COLORS.accent, letterSpacing: -0.5 },
  sidebarSection: { fontSize: 10, color: COLORS.textMuted, padding: "12px 20px 6px", letterSpacing: 1, textTransform: "uppercase" },
  navItem: (active) => ({
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "9px 20px",
    cursor: "pointer",
    borderRadius: 0,
    background: active ? COLORS.accentDim : "transparent",
    borderLeft: active ? `2px solid ${COLORS.accent}` : "2px solid transparent",
    color: active ? COLORS.accent : COLORS.textMuted,
    fontSize: 14,
    fontWeight: active ? 600 : 400,
    transition: "all 0.15s",
  }),
  userBadge: (role) => {
    const colors = { student: COLORS.student, teacher: COLORS.teacher, admin: COLORS.admin };
    return {
      margin: "auto 16px 0",
      padding: "10px 14px",
      borderRadius: 10,
      background: colors[role] + "18",
      border: `1px solid ${colors[role]}30`,
      fontSize: 13,
    };
  },
  main: { marginLeft: 220, flex: 1, padding: "32px 36px", maxWidth: 1100 },
  pageTitle: { fontSize: 22, fontWeight: 700, marginBottom: 4, letterSpacing: -0.5 },
  pageSub: { fontSize: 13, color: COLORS.textMuted, marginBottom: 28 },
  // CARDS
  statsRow: { display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 16, marginBottom: 28 },
  statCard: (accent) => ({
    background: COLORS.surface,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 12,
    padding: "20px 22px",
    borderTop: `3px solid ${accent}`,
  }),
  statVal: { fontSize: 28, fontWeight: 800, marginBottom: 2 },
  statLabel: { fontSize: 12, color: COLORS.textMuted },
  card: {
    background: COLORS.surface,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 12,
    padding: 24,
    marginBottom: 20,
  },
  cardTitle: { fontSize: 15, fontWeight: 700, marginBottom: 16 },
  // TABLE
  table: { width: "100%", borderCollapse: "collapse", fontSize: 13 },
  th: { textAlign: "left", padding: "10px 14px", color: COLORS.textMuted, borderBottom: `1px solid ${COLORS.border}`, fontSize: 11, textTransform: "uppercase", letterSpacing: 0.5 },
  td: { padding: "12px 14px", borderBottom: `1px solid ${COLORS.border}20`, verticalAlign: "middle" },
  badge: (color) => ({
    display: "inline-block",
    padding: "3px 10px",
    borderRadius: 20,
    fontSize: 11,
    fontWeight: 600,
    background: color + "20",
    color: color,
  }),
  // FORM
  formGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 },
  formGroup: { marginBottom: 16 },
  textarea: {
    width: "100%",
    background: COLORS.bg,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 8,
    padding: "10px 14px",
    color: COLORS.text,
    fontSize: 14,
    minHeight: 90,
    resize: "vertical",
    outline: "none",
    boxSizing: "border-box",
    fontFamily: "inherit",
  },
  select: {
    width: "100%",
    background: COLORS.bg,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 8,
    padding: "10px 14px",
    color: COLORS.text,
    fontSize: 14,
    outline: "none",
    boxSizing: "border-box",
    marginBottom: 0,
  },
  smallBtn: (variant = "primary") => ({
    padding: "7px 16px",
    borderRadius: 7,
    border: "none",
    background: variant === "primary" ? COLORS.accent : variant === "danger" ? COLORS.danger + "22" : COLORS.surface,
    color: variant === "primary" ? "#0D1117" : variant === "danger" ? COLORS.danger : COLORS.text,
    fontWeight: 600,
    fontSize: 12,
    cursor: "pointer",
    transition: "background 0.2s",
  }),
  filterRow: { display: "flex", gap: 10, marginBottom: 20, flexWrap: "wrap", alignItems: "center" },
  filterChip: (active) => ({
    padding: "6px 14px",
    borderRadius: 20,
    border: `1px solid ${active ? COLORS.accent : COLORS.border}`,
    background: active ? COLORS.accentDim : "transparent",
    color: active ? COLORS.accent : COLORS.textMuted,
    fontSize: 12,
    cursor: "pointer",
    fontWeight: active ? 600 : 400,
  }),
};

// MOCK DATA
const mockProjects = [
  { id: 1, title: "AI Study Planner", student: "Aryan Mehta", tech: "React, Flask, MongoDB", innovation: "High", quality: "Excellent", status: "reviewed", usp: "Personalized AI scheduling", feedback: "Great innovation! Consider adding export features and better onboarding UX.", submittedAt: "2026-03-10" },
  { id: 2, title: "Campus Food Tracker", student: "Priya Sharma", tech: "Next.js, Node, PostgreSQL", innovation: "Medium", quality: "Good", status: "pending", usp: "Real-time canteen menu", feedback: "", submittedAt: "2026-03-14" },
  { id: 3, title: "Attendance QR System", student: "Rohit Kumar", tech: "Flutter, Firebase", innovation: "High", quality: "Excellent", status: "reviewed", usp: "QR-based auto attendance", feedback: "Excellent implementation! Document the security model more clearly.", submittedAt: "2026-03-08" },
  { id: 4, title: "Budget Manager App", student: "Sneha Patel", tech: "Vue.js, Express, MySQL", innovation: "Low", quality: "Average", status: "pending", usp: "Student expense tracking", feedback: "", submittedAt: "2026-03-16" },
  { id: 5, title: "Peer Code Reviewer", student: "Karan Singh", tech: "React, Django, MongoDB", innovation: "High", quality: "Good", status: "reviewed", usp: "AI-powered code feedback", feedback: "Strong concept. Needs more test coverage and a demo video.", submittedAt: "2026-03-12" },
];

const mockUsers = [
  { id: 1, name: "Aryan Mehta", email: "aryan@college.edu", role: "student", status: "active" },
  { id: 2, name: "Priya Sharma", email: "priya@college.edu", role: "student", status: "active" },
  { id: 3, name: "Dr. Nisha Roy", email: "nisha@college.edu", role: "teacher", status: "active" },
  { id: 4, name: "Prof. Anand Kumar", email: "anand@college.edu", role: "teacher", status: "active" },
  { id: 5, name: "Rohit Kumar", email: "rohit@college.edu", role: "student", status: "inactive" },
];

// AUTH SCREEN
function AuthScreen({ onLogin }) {
  const [role, setRole] = useState("student");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const roleColors = { student: COLORS.student, teacher: COLORS.teacher, admin: COLORS.admin };
  const roleLabels = { student: "👤 Student", teacher: "🎓 Teacher", admin: "🛡 Admin" };

  const handleLogin = () => {
    if (username && password) onLogin({ name: username || "Demo User", role });
  };

  return (
    <div style={styles.authWrap}>
      <div style={styles.authCard}>
        <div style={styles.authLogo}>FnB</div>
        <div style={styles.authSub}>Fetch and Build · Student Project Review Platform</div>

        <label style={styles.label}>Select Role</label>
        <div style={styles.roleGrid}>
          {Object.entries(roleLabels).map(([r, label]) => (
            <button key={r} style={styles.roleBtn(role === r, roleColors[r])} onClick={() => setRole(r)}>{label}</button>
          ))}
        </div>

        <label style={styles.label}>Username</label>
        <input
          style={styles.input}
          placeholder={`Enter ${role} username`}
          value={username}
          onChange={e => setUsername(e.target.value)}
          onFocus={e => (e.target.style.borderColor = COLORS.accent)}
          onBlur={e => (e.target.style.borderColor = COLORS.border)}
        />

        <label style={styles.label}>Password</label>
        <input
          style={styles.input}
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={e => setPassword(e.target.value)}
          onFocus={e => (e.target.style.borderColor = COLORS.accent)}
          onBlur={e => (e.target.style.borderColor = COLORS.border)}
        />

        <button style={styles.btn("primary")} onClick={handleLogin}>Sign In</button>
        <p style={{ textAlign: "center", marginTop: 14, fontSize: 12, color: COLORS.textMuted }}>
          No account? Contact your administrator.
        </p>
      </div>
    </div>
  );
}

// SIDEBAR
function Sidebar({ user, activeTab, setActiveTab, onLogout }) {
  const roleColor = { student: COLORS.student, teacher: COLORS.teacher, admin: COLORS.admin }[user.role];

  const navItems = {
    student: [
      { id: "dashboard", icon: "⬛", label: "Dashboard" },
      { id: "submit", icon: "📤", label: "Submit Project" },
      { id: "myprojects", icon: "📁", label: "My Projects" },
      { id: "feedback", icon: "💬", label: "My Feedback" },
    ],
    teacher: [
      { id: "dashboard", icon: "⬛", label: "Dashboard" },
      { id: "projects", icon: "📋", label: "All Projects" },
      { id: "review", icon: "🔍", label: "Pending Review" },
      { id: "givefeedback", icon: "✍️", label: "Give Feedback" },
    ],
    admin: [
      { id: "dashboard", icon: "⬛", label: "Dashboard" },
      { id: "users", icon: "👥", label: "User Management" },
      { id: "allprojects", icon: "📁", label: "All Projects" },
      { id: "reports", icon: "📊", label: "Reports" },
    ],
  };

  return (
    <div style={styles.sidebar}>
      <div style={styles.sidebarLogo}>⚡ FnB</div>
      <div style={styles.sidebarSection}>Navigation</div>
      {navItems[user.role].map(item => (
        <div key={item.id} style={styles.navItem(activeTab === item.id)} onClick={() => setActiveTab(item.id)}>
          <span>{item.icon}</span>
          <span>{item.label}</span>
        </div>
      ))}

      <div style={styles.userBadge(user.role)}>
        <div style={{ fontSize: 11, color: COLORS.textMuted, marginBottom: 2 }}>{user.role.toUpperCase()}</div>
        <div style={{ fontWeight: 600, fontSize: 13 }}>{user.name}</div>
        <div
          style={{ fontSize: 11, color: COLORS.danger, cursor: "pointer", marginTop: 8 }}
          onClick={onLogout}
        >Sign out →</div>
      </div>
    </div>
  );
}

// STUDENT DASHBOARD
function StudentDashboard({ user }) {
  const myProjects = mockProjects.filter(p => p.student === user.name || true).slice(0, 3);
  const reviewed = myProjects.filter(p => p.status === "reviewed").length;

  return (
    <>
      <div style={styles.pageTitle}>Welcome back, {user.name.split(" ")[0]} 👋</div>
      <div style={styles.pageSub}>Track your submissions and teacher feedback below.</div>
      <div style={styles.statsRow}>
        {[
          { label: "Projects Submitted", val: 3, accent: COLORS.student },
          { label: "Reviewed", val: reviewed, accent: COLORS.success },
          { label: "Pending Review", val: 3 - reviewed, accent: COLORS.warn },
          { label: "Avg Rating", val: "B+", accent: COLORS.accent },
        ].map(s => (
          <div key={s.label} style={styles.statCard(s.accent)}>
            <div style={{ ...styles.statVal, color: s.accent }}>{s.val}</div>
            <div style={styles.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>
      <div style={styles.card}>
        <div style={styles.cardTitle}>My Submissions</div>
        <table style={styles.table}>
          <thead>
            <tr>
              {["Project", "Technology", "Submitted", "Status", ""].map(h => <th key={h} style={styles.th}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {myProjects.map(p => (
              <tr key={p.id}>
                <td style={styles.td}><strong>{p.title}</strong><br /><span style={{ fontSize: 11, color: COLORS.textMuted }}>{p.usp}</span></td>
                <td style={styles.td}><span style={{ ...styles.badge(COLORS.accent), fontSize: 11 }}>{p.tech.split(",")[0]}</span></td>
                <td style={styles.td}><span style={{ color: COLORS.textMuted, fontSize: 12 }}>{p.submittedAt}</span></td>
                <td style={styles.td}>
                  <span style={styles.badge(p.status === "reviewed" ? COLORS.success : COLORS.warn)}>
                    {p.status === "reviewed" ? "✓ Reviewed" : "⏳ Pending"}
                  </span>
                </td>
                <td style={styles.td}><button style={styles.smallBtn("secondary")}>View</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

// SUBMIT PROJECT
function SubmitProject() {
  const [form, setForm] = useState({ title: "", tech: "", usp: "", desc: "", innovation: "Medium", quality: "Good", file: "" });
  const [submitted, setSubmitted] = useState(false);

  if (submitted) return (
    <div style={{ ...styles.card, textAlign: "center", padding: 48 }}>
      <div style={{ fontSize: 40, marginBottom: 12 }}>✅</div>
      <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>Project Submitted!</div>
      <div style={{ color: COLORS.textMuted, marginBottom: 20 }}>Your project is now under review. You'll be notified once feedback is available.</div>
      <button style={{ ...styles.smallBtn("secondary"), padding: "9px 24px" }} onClick={() => setSubmitted(false)}>Submit Another</button>
    </div>
  );

  return (
    <>
      <div style={styles.pageTitle}>Submit Project</div>
      <div style={styles.pageSub}>Fill in all required fields and upload your project files.</div>
      <div style={styles.card}>
        <div style={styles.cardTitle}>Project Details</div>
        <div style={styles.formGrid}>
          <div>
            <label style={styles.label}>Project Title *</label>
            <input style={styles.input} placeholder="e.g. AI Study Planner" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} />
          </div>
          <div>
            <label style={styles.label}>Technology Stack *</label>
            <input style={styles.input} placeholder="e.g. React, Flask, MongoDB" value={form.tech} onChange={e => setForm({ ...form, tech: e.target.value })} />
          </div>
          <div>
            <label style={styles.label}>Unique Selling Point (USP)</label>
            <input style={styles.input} placeholder="What makes your project stand out?" value={form.usp} onChange={e => setForm({ ...form, usp: e.target.value })} />
          </div>
          <div>
            <label style={styles.label}>Innovation Level</label>
            <select style={styles.select} value={form.innovation} onChange={e => setForm({ ...form, innovation: e.target.value })}>
              <option>Low</option><option>Medium</option><option>High</option>
            </select>
          </div>
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Project Description *</label>
          <textarea style={styles.textarea} placeholder="Describe your project, its purpose, features, and implementation..." value={form.desc} onChange={e => setForm({ ...form, desc: e.target.value })} />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Upload Project Files</label>
          <div style={{ border: `2px dashed ${COLORS.border}`, borderRadius: 8, padding: "20px", textAlign: "center", color: COLORS.textMuted, fontSize: 13, cursor: "pointer" }}>
            📎 Click to upload or drag & drop<br />
            <span style={{ fontSize: 11 }}>Supported: .zip, .pdf, .docx (max 50MB)</span>
          </div>
        </div>
        <button style={{ ...styles.smallBtn("primary"), padding: "10px 28px", fontSize: 14 }} onClick={() => setSubmitted(true)}>
          Submit Project →
        </button>
      </div>
    </>
  );
}

// TEACHER PROJECT LIST
function TeacherProjects() {
  const [filter, setFilter] = useState("all");
  const [techFilter, setTechFilter] = useState("all");

  const statusFilters = ["all", "pending", "reviewed"];
  const filtered = mockProjects.filter(p => {
    const statusMatch = filter === "all" || p.status === filter;
    const techMatch = techFilter === "all" || p.tech.toLowerCase().includes(techFilter.toLowerCase());
    return statusMatch && techMatch;
  });

  return (
    <>
      <div style={styles.pageTitle}>Project Submissions</div>
      <div style={styles.pageSub}>Review and evaluate student projects. Use filters to narrow down.</div>

      <div style={styles.filterRow}>
        <span style={{ fontSize: 12, color: COLORS.textMuted }}>Status:</span>
        {statusFilters.map(f => (
          <button key={f} style={styles.filterChip(filter === f)} onClick={() => setFilter(f)}>{f.charAt(0).toUpperCase() + f.slice(1)}</button>
        ))}
        <span style={{ fontSize: 12, color: COLORS.textMuted, marginLeft: 12 }}>Tech:</span>
        {["all", "React", "Flutter", "Vue.js"].map(t => (
          <button key={t} style={styles.filterChip(techFilter === t)} onClick={() => setTechFilter(t)}>{t}</button>
        ))}
      </div>

      <div style={styles.card}>
        <table style={styles.table}>
          <thead>
            <tr>
              {["Project", "Student", "Tech Stack", "Innovation", "Quality", "Status", "Action"].map(h => <th key={h} style={styles.th}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {filtered.map(p => (
              <tr key={p.id}>
                <td style={styles.td}><strong style={{ fontSize: 13 }}>{p.title}</strong><br /><span style={{ fontSize: 11, color: COLORS.textMuted }}>{p.usp}</span></td>
                <td style={styles.td}><span style={{ fontSize: 13 }}>{p.student}</span></td>
                <td style={styles.td}><span style={styles.badge(COLORS.accent)}>{p.tech.split(",")[0]}</span></td>
                <td style={styles.td}><span style={styles.badge(p.innovation === "High" ? COLORS.success : p.innovation === "Medium" ? COLORS.warn : COLORS.textMuted)}>{p.innovation}</span></td>
                <td style={styles.td}><span style={{ fontSize: 12, color: COLORS.textMuted }}>{p.quality}</span></td>
                <td style={styles.td}><span style={styles.badge(p.status === "reviewed" ? COLORS.success : COLORS.warn)}>{p.status === "reviewed" ? "✓ Done" : "⏳ Pending"}</span></td>
                <td style={styles.td}>
                  <button style={styles.smallBtn(p.status === "pending" ? "primary" : "secondary")}>
                    {p.status === "pending" ? "Review" : "Edit"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div style={{ textAlign: "center", padding: 32, color: COLORS.textMuted }}>No projects match the selected filters.</div>}
      </div>
    </>
  );
}

// GIVE FEEDBACK
function GiveFeedback() {
  const [selected, setSelected] = useState(mockProjects[1]);
  const [feedback, setFeedback] = useState(selected.feedback);
  const [saved, setSaved] = useState(false);

  const pending = mockProjects.filter(p => p.status === "pending");

  const handleSave = () => { setSaved(true); setTimeout(() => setSaved(false), 2000); };

  return (
    <>
      <div style={styles.pageTitle}>Give Feedback</div>
      <div style={styles.pageSub}>Select a pending project and submit structured feedback.</div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1.6fr", gap: 20 }}>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Pending Projects ({pending.length})</div>
          {pending.map(p => (
            <div key={p.id}
              onClick={() => { setSelected(p); setFeedback(p.feedback); }}
              style={{ padding: "12px 14px", borderRadius: 8, cursor: "pointer", background: selected?.id === p.id ? COLORS.accentDim : "transparent", border: `1px solid ${selected?.id === p.id ? COLORS.accent : "transparent"}`, marginBottom: 8, transition: "all 0.15s" }}
            >
              <div style={{ fontWeight: 600, fontSize: 13 }}>{p.title}</div>
              <div style={{ fontSize: 11, color: COLORS.textMuted, marginTop: 2 }}>{p.student} · {p.submittedAt}</div>
            </div>
          ))}
        </div>
        {selected && (
          <div style={styles.card}>
            <div style={styles.cardTitle}>{selected.title}</div>
            <div style={{ fontSize: 12, color: COLORS.textMuted, marginBottom: 12 }}>
              Student: <strong style={{ color: COLORS.text }}>{selected.student}</strong> &nbsp;|&nbsp;
              Tech: <strong style={{ color: COLORS.text }}>{selected.tech}</strong>
            </div>
            <div style={{ marginBottom: 12 }}>
              {[["Innovation", selected.innovation], ["Quality", selected.quality], ["USP", selected.usp]].map(([k, v]) => (
                <span key={k} style={{ ...styles.badge(COLORS.accent), marginRight: 8 }}>{k}: {v}</span>
              ))}
            </div>
            <label style={styles.label}>Feedback & Suggestions</label>
            <textarea style={{ ...styles.textarea, minHeight: 120 }} placeholder="Write detailed feedback, suggestions, and improvement remarks..." value={feedback} onChange={e => setFeedback(e.target.value)} />
            <div style={{ display: "flex", gap: 10, marginTop: 16, alignItems: "center" }}>
              <button style={{ ...styles.smallBtn("primary"), padding: "9px 24px", fontSize: 13 }} onClick={handleSave}>
                {saved ? "✓ Saved!" : "Submit Feedback"}
              </button>
              <button style={{ ...styles.smallBtn("secondary"), padding: "9px 16px", fontSize: 13 }}>Clear</button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

// STUDENT FEEDBACK VIEW
function FeedbackView() {
  const reviewed = mockProjects.filter(p => p.status === "reviewed");
  return (
    <>
      <div style={styles.pageTitle}>My Feedback</div>
      <div style={styles.pageSub}>Teacher feedback and suggestions for your submitted projects.</div>
      {reviewed.map(p => (
        <div key={p.id} style={styles.card}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: 15 }}>{p.title}</div>
              <div style={{ fontSize: 12, color: COLORS.textMuted, marginTop: 2 }}>Submitted: {p.submittedAt}</div>
            </div>
            <span style={styles.badge(COLORS.success)}>✓ Reviewed</span>
          </div>
          <div style={{ background: COLORS.bg, borderRadius: 8, padding: "14px 16px", borderLeft: `3px solid ${COLORS.accent}`, fontSize: 13, lineHeight: 1.7, color: COLORS.text }}>
            "{p.feedback}"
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
            {[["Innovation", p.innovation], ["Quality", p.quality]].map(([k, v]) => (
              <span key={k} style={styles.badge(COLORS.teacher)}>{k}: {v}</span>
            ))}
          </div>
        </div>
      ))}
    </>
  );
}

// ADMIN USER MANAGEMENT
function UserManagement() {
  const [users, setUsers] = useState(mockUsers);
  const roleColor = { student: COLORS.student, teacher: COLORS.teacher, admin: COLORS.admin };

  const toggleStatus = (id) => {
    setUsers(users.map(u => u.id === id ? { ...u, status: u.status === "active" ? "inactive" : "active" } : u));
  };

  return (
    <>
      <div style={styles.pageTitle}>User Management</div>
      <div style={styles.pageSub}>Create, manage, and control access for all platform users.</div>
      <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 16 }}>
        <button style={{ ...styles.smallBtn("primary"), padding: "9px 20px", fontSize: 13 }}>+ Add User</button>
      </div>
      <div style={styles.card}>
        <table style={styles.table}>
          <thead>
            <tr>{["Name", "Email", "Role", "Status", "Actions"].map(h => <th key={h} style={styles.th}>{h}</th>)}</tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id}>
                <td style={styles.td}><strong>{u.name}</strong></td>
                <td style={styles.td}><span style={{ color: COLORS.textMuted, fontSize: 12 }}>{u.email}</span></td>
                <td style={styles.td}><span style={styles.badge(roleColor[u.role])}>{u.role}</span></td>
                <td style={styles.td}><span style={styles.badge(u.status === "active" ? COLORS.success : COLORS.danger)}>{u.status}</span></td>
                <td style={styles.td}>
                  <div style={{ display: "flex", gap: 8 }}>
                    <button style={styles.smallBtn("secondary")} onClick={() => toggleStatus(u.id)}>
                      {u.status === "active" ? "Disable" : "Enable"}
                    </button>
                    <button style={styles.smallBtn("danger")}>Remove</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

// GENERIC DASHBOARD
function Dashboard({ user }) {
  const roleColor = { student: COLORS.student, teacher: COLORS.teacher, admin: COLORS.admin }[user.role];
  const stats = {
    student: [
      { label: "Projects Submitted", val: 3, accent: COLORS.student },
      { label: "Feedback Received", val: 2, accent: COLORS.success },
      { label: "Pending Review", val: 1, accent: COLORS.warn },
      { label: "Profile Complete", val: "90%", accent: COLORS.accent },
    ],
    teacher: [
      { label: "Projects to Review", val: 2, accent: COLORS.warn },
      { label: "Reviewed This Month", val: 8, accent: COLORS.success },
      { label: "Students Mentored", val: 12, accent: COLORS.teacher },
      { label: "Avg Rating Given", val: "B+", accent: COLORS.accent },
    ],
    admin: [
      { label: "Total Users", val: 5, accent: COLORS.admin },
      { label: "Active Projects", val: 5, accent: COLORS.accent },
      { label: "Pending Reviews", val: 2, accent: COLORS.warn },
      { label: "System Health", val: "✓ OK", accent: COLORS.success },
    ],
  }[user.role];

  return (
    <>
      <div style={styles.pageTitle}>{user.role.charAt(0).toUpperCase() + user.role.slice(1)} Dashboard</div>
      <div style={styles.pageSub}>Overview of your FnB activity and recent updates.</div>
      <div style={styles.statsRow}>
        {stats.map(s => (
          <div key={s.label} style={styles.statCard(s.accent)}>
            <div style={{ ...styles.statVal, color: s.accent }}>{s.val}</div>
            <div style={styles.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: 20 }}>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Recent Projects</div>
          {mockProjects.slice(0, 4).map(p => (
            <div key={p.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: `1px solid ${COLORS.border}20` }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600 }}>{p.title}</div>
                <div style={{ fontSize: 11, color: COLORS.textMuted }}>{p.student}</div>
              </div>
              <span style={styles.badge(p.status === "reviewed" ? COLORS.success : COLORS.warn)}>
                {p.status}
              </span>
            </div>
          ))}
        </div>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Quick Actions</div>
          {user.role === "student" && [["📤 Submit New Project", "submit"], ["💬 View Feedback", "feedback"]].map(([label]) => (
            <div key={label} style={{ padding: "11px 14px", borderRadius: 8, background: COLORS.bg, marginBottom: 8, cursor: "pointer", fontSize: 13, fontWeight: 500, border: `1px solid ${COLORS.border}` }}>{label}</div>
          ))}
          {user.role === "teacher" && [["🔍 Review Pending", ""], ["✍️ Give Feedback", ""]].map(([label]) => (
            <div key={label} style={{ padding: "11px 14px", borderRadius: 8, background: COLORS.bg, marginBottom: 8, cursor: "pointer", fontSize: 13, fontWeight: 500, border: `1px solid ${COLORS.border}` }}>{label}</div>
          ))}
          {user.role === "admin" && [["👥 Manage Users", ""], ["📁 All Projects", ""], ["📊 View Reports", ""]].map(([label]) => (
            <div key={label} style={{ padding: "11px 14px", borderRadius: 8, background: COLORS.bg, marginBottom: 8, cursor: "pointer", fontSize: 13, fontWeight: 500, border: `1px solid ${COLORS.border}` }}>{label}</div>
          ))}
        </div>
      </div>
    </>
  );
}

// MAIN APP
export default function App() {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState("dashboard");

  const handleLogin = (userData) => { setUser(userData); setActiveTab("dashboard"); };
  const handleLogout = () => { setUser(null); setActiveTab("dashboard"); };

  if (!user) return <AuthScreen onLogin={handleLogin} />;

  const renderContent = () => {
    if (activeTab === "dashboard") return <Dashboard user={user} />;
    if (activeTab === "submit") return <SubmitProject />;
    if (activeTab === "feedback") return <FeedbackView />;
    if (activeTab === "projects" || activeTab === "allprojects" || activeTab === "review") return <TeacherProjects />;
    if (activeTab === "givefeedback") return <GiveFeedback />;
    if (activeTab === "users") return <UserManagement />;
    if (activeTab === "myprojects") return <StudentDashboard user={user} />;
    if (activeTab === "reports") return (
      <div style={styles.card}>
        <div style={styles.cardTitle}>Reports</div>
        <div style={{ color: COLORS.textMuted, textAlign: "center", padding: 40 }}>📊 Analytics and reporting features coming soon.</div>
      </div>
    );
    return <Dashboard user={user} />;
  };

  return (
    <div style={styles.app}>
      <div style={styles.layout}>
        <Sidebar user={user} activeTab={activeTab} setActiveTab={setActiveTab} onLogout={handleLogout} />
        <div style={styles.main}>{renderContent()}</div>
      </div>
    </div>
  );
}
