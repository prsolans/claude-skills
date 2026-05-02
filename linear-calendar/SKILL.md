---
name: linear-calendar
description: Show Linear issues and projects on a visual HTML calendar in the browser. Trigger when the user says "linear calendar", "show my calendar", "timeline view", or "what's due".
user_invocable: true
---

# Linear Calendar

Generate a week-view calendar showing active Linear issues (by due date) and project target dates, with a footer showing rest-of-month items and milestones with progress bars. Week navigation (Prev/Next/Today) works client-side.

## Steps

1. **Fetch issues** using the `list_issues` MCP tool:
   - Set `assignee` to `"me"`
   - Set `limit` to `250`
   - Collect: id (used as identifier, e.g. "PRS-123"), title, dueDate, status (state name), priority, url, project (project name)

2. **Filter issues:**
   - **Only include issues that have a dueDate** (skip null dueDate)
   - **Only include active issues** — exclude issues with status "Done", "Canceled", "Cancelled", "Duplicate"

3. **Fetch projects** using the `list_projects` MCP tool:
   - Set `member` to `"me"`
   - Set `limit` to `50`
   - Collect: id, name, targetDate, state, url
   - **Only include projects that have a targetDate** (we only show target dates, not start dates)
   - Set `startDate` to `null` for all projects (we don't use start dates)

4. **Fetch milestones** for each active (non-completed, non-backlog) project using `list_milestones`:
   - Call once per project
   - Collect: name, project (project name), targetDate, progress
   - **Only include milestones where progress < 100 and targetDate is not null**
   - Sort by targetDate ascending

5. **Build 4 JSON arrays** and embed them into the HTML template:
   - `issues` — filtered active issues with dueDate, including `project` field (project name string)
   - `projects` — projects with targetDate only
   - `projectDates` — derived from projects: `{date, label: "<name> target", url, type: "project"}`
   - `milestones` — incomplete milestones with target dates, sorted by date

6. **Generate the HTML file** at `/tmp/linear-calendar.html` using the template below, with the 4 JSON arrays embedded as JavaScript constants.

7. **Open in browser:**
```bash
open /tmp/linear-calendar.html
```

8. Tell the user the calendar is open. Mention how many active issues and projects are shown.

## HTML Template

The output is a single self-contained HTML file. All data is embedded as JS constants. The calendar renders client-side with week navigation.

**Layout:**
- Header: Prev / Today / Next buttons + "Week of Mon DD – Mon DD, YYYY" title
- Subtitle: "N issues · N project targets"
- Legend: Issue due (blue card) + Project target (purple card)
- Week grid: 7 columns (Mon–Sun), each with day header and cards
- Footer: two-column grid
  - Left: **"[Month] [Year]"** — all issues, project targets, and milestones due this month, **excluding items already visible in the current week view**. Updates when navigating weeks.
  - Right: **"Milestones"** — all upcoming incomplete milestones with progress bars, sorted by target date

**Issue cards show:** priority dot (color-coded), identifier, title, project name (green), state
**Project target cards show:** "Target" label + project name (purple)
**Footer items show:** date (color-coded: red=overdue, orange=soon, blue=today), name, project tag
**Milestone items show:** date, name, project tag, progress bar with percentage

Write the HTML file directly using the Write tool — do NOT use the render_calendar.py script.

```html
<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Linear – Week View</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#0d1117; color:#c9d1d9; padding:24px; }
.container { max-width:1200px; margin:0 auto; }
.header { display:flex; align-items:center; gap:16px; margin-bottom:4px; }
h1 { font-size:20px; font-weight:600; color:#e6edf3; }
.nav-btn { background:#21262d; border:1px solid #30363d; color:#c9d1d9; padding:5px 12px; border-radius:6px; cursor:pointer; font-size:13px; }
.nav-btn:hover { background:#30363d; }
.today-btn { background:#1f3a5f; color:#58a6ff; border:1px solid #264773; }
.today-btn:hover { background:#264773; }
.subtitle { font-size:13px; color:#8b949e; margin-bottom:16px; }
.legend { display:flex; gap:16px; margin-bottom:16px; font-size:12px; color:#8b949e; }
.legend span { display:inline-flex; align-items:center; gap:6px; }
.swatch { display:inline-block; width:12px; height:12px; border-radius:3px; }
.week-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:8px; }
.day-col { background:#161b22; border:1px solid #21262d; border-radius:8px; min-height:400px; }
.day-col.today { border-color:#58a6ff; background:#111827; }
.day-header { padding:10px 10px 8px; border-bottom:1px solid #21262d; font-size:13px; font-weight:600; color:#8b949e; }
.day-col.today .day-header { color:#58a6ff; }
.date-num { font-size:15px; color:#e6edf3; }
.today-badge { font-size:10px; background:#1f3a5f; color:#58a6ff; padding:1px 6px; border-radius:8px; margin-left:4px; }
.day-body { padding:8px; display:flex; flex-direction:column; gap:6px; }
.issue-card { display:block; background:#1c2333; border:1px solid #30363d; border-radius:6px; padding:8px; text-decoration:none; color:#c9d1d9; transition:border-color .15s; }
.issue-card:hover { border-color:#58a6ff; }
.prio-dot { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:4px; vertical-align:middle; }
.ident { font-size:11px; font-weight:600; color:#79c0ff; }
.title { display:block; font-size:12px; margin-top:3px; line-height:1.35; }
.project-tag { display:block; font-size:10px; color:#7ee787; margin-top:3px; opacity:.8; }
.state { display:block; font-size:10px; color:#8b949e; margin-top:2px; }
.proj-card { display:block; background:#2d1f4e; border:1px solid #3b2466; border-radius:6px; padding:8px; text-decoration:none; color:#d2a8ff; transition:border-color .15s; }
.proj-card:hover { border-color:#a371f7; }
.proj-label { font-size:9px; text-transform:uppercase; letter-spacing:.5px; opacity:.7; }
.proj-name { display:block; font-size:12px; margin-top:2px; font-weight:600; }
.footer { margin-top:24px; display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.footer-section { background:#161b22; border:1px solid #21262d; border-radius:8px; padding:16px; }
.footer-section h3 { font-size:13px; font-weight:600; color:#e6edf3; margin-bottom:10px; text-transform:uppercase; letter-spacing:.5px; }
.footer-item { display:flex; align-items:baseline; gap:10px; padding:6px 0; border-bottom:1px solid #21262d; font-size:12px; }
.footer-item:last-child { border-bottom:none; }
.footer-date { font-weight:600; color:#8b949e; min-width:70px; white-space:nowrap; }
.footer-date.overdue { color:#f85149; }
.footer-date.soon { color:#f0883e; }
.footer-date.today { color:#58a6ff; }
.footer-name { color:#c9d1d9; }
.footer-project { color:#7ee787; font-size:11px; opacity:.8; margin-left:4px; }
.footer-progress { margin-left:auto; font-size:11px; color:#8b949e; white-space:nowrap; }
.progress-bar { display:inline-block; width:40px; height:6px; background:#21262d; border-radius:3px; vertical-align:middle; margin-right:4px; overflow:hidden; }
.progress-fill { height:100%; border-radius:3px; background:#3fb950; }
.empty-msg { font-size:12px; color:#484f58; font-style:italic; }
</style></head><body>
<div class="container">
<div class="header">
  <button class="nav-btn" onclick="nav(-1)">&larr; Prev</button>
  <button class="nav-btn today-btn" onclick="goToday()">Today</button>
  <button class="nav-btn" onclick="nav(1)">Next &rarr;</button>
  <h1 id="week-title"></h1>
</div>
<p class="subtitle" id="subtitle"></p>
<div class="legend">
  <span><span class="swatch" style="background:#1c2333;border:1px solid #30363d"></span> Issue due</span>
  <span><span class="swatch" style="background:#2d1f4e;border:1px solid #3b2466"></span> Project target</span>
</div>
<div class="week-grid" id="grid"></div>
<div class="footer">
  <div class="footer-section">
    <h3 id="this-month-title">This Month</h3>
    <div id="this-month"></div>
  </div>
  <div class="footer-section">
    <h3>Milestones</h3>
    <div id="milestones"></div>
  </div>
</div>
</div>
<script>
const issues = __ISSUES_JSON__;
const projects = __PROJECTS_JSON__;
const projectDates = __PROJECT_DATES_JSON__;
const milestones = __MILESTONES_JSON__;
const prioColors = {1:'#f85149',2:'#f0883e',3:'#58a6ff',4:'#8b949e'};
const dayNames = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
const monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

function toDateStr(d) {
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
}
function addDays(d, n) { const r=new Date(d); r.setDate(r.getDate()+n); return r; }
function getMonday(d) { const r=new Date(d); const day=r.getDay(); const diff=r.getDate()-day+(day===0?-6:1); r.setDate(diff); return r; }
function esc(s) { const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }
function fmtDate(s) {
  const d = new Date(s+'T00:00:00');
  return monthNames[d.getMonth()] + ' ' + d.getDate();
}
function dateCls(s, todayStr) {
  if (s < todayStr) return 'overdue';
  if (s === todayStr) return 'today';
  const t = new Date(todayStr+'T00:00:00');
  const d = new Date(s+'T00:00:00');
  const diff = (d - t) / 86400000;
  if (diff <= 3) return 'soon';
  return '';
}

const today = new Date();
today.setHours(0,0,0,0);
const todayStr = toDateStr(today);
let weekStart = getMonday(today);

const issuesByDate = {};
issues.forEach(i => {
  if (i.dueDate) {
    const k = i.dueDate.slice(0,10);
    (issuesByDate[k] = issuesByDate[k]||[]).push(i);
  }
});
const projByDate = {};
projects.forEach(p => {
  if (p.targetDate) {
    const k = p.targetDate.slice(0,10);
    (projByDate[k] = projByDate[k]||[]).push(p);
  }
});

function render() {
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  const end = addDays(weekStart, 6);
  document.getElementById('week-title').textContent =
    'Week of ' + monthNames[weekStart.getMonth()] + ' ' + weekStart.getDate() +
    ' \u2013 ' + monthNames[end.getMonth()] + ' ' + end.getDate() + ', ' + end.getFullYear();

  let issueCount = 0, projCount = 0;
  for (let i = 0; i < 7; i++) {
    const d = addDays(weekStart, i);
    const ds = toDateStr(d);
    const isToday = ds === todayStr;
    const col = document.createElement('div');
    col.className = 'day-col' + (isToday ? ' today' : '');
    let hdr = dayNames[i] + ' <span class="date-num">' + d.getDate() + '</span>';
    if (isToday) hdr += ' <span class="today-badge">Today</span>';
    col.innerHTML = '<div class="day-header">' + hdr + '</div>';
    const body = document.createElement('div');
    body.className = 'day-body';

    (issuesByDate[ds]||[]).forEach(iss => {
      issueCount++;
      const prio = iss.priority || 0;
      const dot = prio ? '<span class="prio-dot" style="background:'+prioColors[prio]+'"></span>' : '';
      const projTag = iss.project ? '<span class="project-tag">' + esc(iss.project) + '</span>' : '';
      const a = document.createElement('a');
      a.className = 'issue-card';
      a.href = iss.url;
      a.target = '_blank';
      a.innerHTML = dot + '<span class="ident">' + esc(iss.identifier) + '</span>' +
        '<span class="title">' + esc(iss.title) + '</span>' + projTag +
        '<span class="state">' + esc(iss.state) + '</span>';
      body.appendChild(a);
    });
    (projByDate[ds]||[]).forEach(p => {
      projCount++;
      const a = document.createElement('a');
      a.className = 'proj-card';
      a.href = p.url;
      a.target = '_blank';
      a.innerHTML = '<span class="proj-label">Target</span><span class="proj-name">' + esc(p.name) + '</span>';
      body.appendChild(a);
    });

    col.appendChild(body);
    grid.appendChild(col);
  }
  document.getElementById('subtitle').textContent = issueCount + ' issues \u00b7 ' + projCount + ' project targets';
  renderFooter();
}

function renderFooter() {
  const weekEndDate = toDateStr(addDays(weekStart, 6));
  const weekStartStr = toDateStr(weekStart);
  const tmEl = document.getElementById('this-month');
  const year = today.getFullYear(), month = today.getMonth();
  const monthStart = toDateStr(new Date(year, month, 1));
  const monthEnd = toDateStr(new Date(year, month + 1, 0));
  const monthLabel = monthNames[month] + ' ' + year;
  document.getElementById('this-month-title').textContent = monthLabel;

  let upcoming = [];
  function inWeek(d) { return d >= weekStartStr && d <= weekEndDate; }

  issues.forEach(i => {
    if (i.dueDate) {
      const d = i.dueDate.slice(0,10);
      if (d >= monthStart && d <= monthEnd && !inWeek(d)) {
        upcoming.push({date:d, label:i.identifier+': '+i.title, project:i.project||'', type:'issue', url:i.url});
      }
    }
  });
  projectDates.forEach(p => {
    if (p.date >= monthStart && p.date <= monthEnd && !inWeek(p.date)) {
      upcoming.push({date:p.date, label:p.label, project:'', type:'project', url:p.url});
    }
  });
  milestones.forEach(m => {
    if (m.targetDate >= monthStart && m.targetDate <= monthEnd && !inWeek(m.targetDate)) {
      upcoming.push({date:m.targetDate, label:m.name+' (milestone)', project:m.project, type:'milestone', url:''});
    }
  });

  upcoming.sort((a,b) => a.date.localeCompare(b.date));

  if (upcoming.length === 0) {
    tmEl.innerHTML = '<div class="empty-msg">Nothing else due this month</div>';
  } else {
    tmEl.innerHTML = upcoming.map(u => {
      const cls = dateCls(u.date, todayStr);
      const projHtml = u.project ? '<span class="footer-project">' + esc(u.project) + '</span>' : '';
      const nameHtml = u.url
        ? '<a href="'+esc(u.url)+'" target="_blank" style="color:inherit;text-decoration:none"><span class="footer-name">'+esc(u.label)+'</span></a>'
        : '<span class="footer-name">'+esc(u.label)+'</span>';
      return '<div class="footer-item"><span class="footer-date '+cls+'">'+fmtDate(u.date)+'</span>'+nameHtml+projHtml+'</div>';
    }).join('');
  }

  const msEl = document.getElementById('milestones');
  if (milestones.length === 0) {
    msEl.innerHTML = '<div class="empty-msg">No upcoming milestones</div>';
  } else {
    msEl.innerHTML = milestones.map(m => {
      const cls = dateCls(m.targetDate, todayStr);
      const pct = Math.round(m.progress);
      return '<div class="footer-item">' +
        '<span class="footer-date '+cls+'">'+fmtDate(m.targetDate)+'</span>' +
        '<span class="footer-name">'+esc(m.name)+'</span>' +
        '<span class="footer-project">'+esc(m.project)+'</span>' +
        '<span class="footer-progress"><span class="progress-bar"><span class="progress-fill" style="width:'+pct+'%"></span></span>'+pct+'%</span>' +
        '</div>';
    }).join('');
  }
}

function nav(dir) { weekStart = addDays(weekStart, dir * 7); render(); }
function goToday() { weekStart = getMonday(today); render(); }

render();
</script>
</body></html>
```

Replace `__ISSUES_JSON__`, `__PROJECTS_JSON__`, `__PROJECT_DATES_JSON__`, and `__MILESTONES_JSON__` with the actual JSON arrays when writing the file.
