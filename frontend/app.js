/* ═══════════════════════════════════════════════════════════════
   Fraud Shield — Frontend Application Logic
   SPA routing · API integration · Particle system · Dynamic rendering
   ═══════════════════════════════════════════════════════════════ */

const API_BASE = window.location.origin;

// ── Particle Background System ────────────────────────────────

(function initParticles() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let particles = [];
    const PARTICLE_COUNT = 60;
    const CONNECT_DIST = 120;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function createParticles() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                size: Math.random() * 1.5 + 0.5,
                opacity: Math.random() * 0.4 + 0.1,
            });
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(99, 102, 241, ${p.opacity})`;
            ctx.fill();
        });

        // Draw connections
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < CONNECT_DIST) {
                    const opacity = (1 - dist / CONNECT_DIST) * 0.08;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(99, 102, 241, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    resize();
    createParticles();
    animate();

    window.addEventListener('resize', () => {
        resize();
        createParticles();
    });
})();

// ── SPA Navigation ────────────────────────────────────────────

const navLinks = document.querySelectorAll('.nav-link');
const views = document.querySelectorAll('.view');

function navigateTo(viewName) {
    views.forEach(v => v.classList.remove('active'));
    navLinks.forEach(l => l.classList.remove('active'));

    const target = document.getElementById(`view-${viewName}`);
    const link = document.querySelector(`[data-view="${viewName}"]`);

    if (target) target.classList.add('active');
    if (link) link.classList.add('active');

    // Close mobile sidebar
    document.getElementById('sidebar').classList.remove('open');

    // Load data for specific views
    if (viewName === 'dashboard') loadDashboard();
}

// Hash-based routing
function handleRoute() {
    const hash = window.location.hash.replace('#', '') || 'dashboard';
    navigateTo(hash);
}

window.addEventListener('hashchange', handleRoute);
window.addEventListener('DOMContentLoaded', () => {
    handleRoute();
    checkApiStatus();
});

// Nav clicks
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        const view = link.dataset.view;
        window.location.hash = view;
    });
});

// Mobile hamburger
document.getElementById('hamburger').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

// Close sidebar on outside click (mobile)
document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('hamburger');
    if (window.innerWidth <= 768 &&
        !sidebar.contains(e.target) &&
        !hamburger.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});

// ── Toast Notifications ───────────────────────────────────────

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ── API Helpers ───────────────────────────────────────────────

async function apiGet(path) {
    const res = await fetch(`${API_BASE}${path}`);
    if (!res.ok) throw new Error(`API Error: ${res.status}`);
    return res.json();
}

async function apiPost(path, data) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `API Error: ${res.status}`);
    }
    return res.json();
}

// ── API Status Check ──────────────────────────────────────────

async function checkApiStatus() {
    const statusEl = document.getElementById('api-status');
    try {
        await apiGet('/api/dashboard/stats');
        statusEl.innerHTML = '<span class="status-dot online"></span><span class="status-text">System Online</span>';
    } catch {
        statusEl.innerHTML = '<span class="status-dot offline"></span><span class="status-text">System Offline</span>';
    }
}

// ── Button Loading State ──────────────────────────────────────

function setLoading(btnId, loading) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    const text = btn.querySelector('.btn-text');
    const loader = btn.querySelector('.btn-loader');
    if (loading) {
        btn.disabled = true;
        if (text) text.style.display = 'none';
        if (loader) loader.style.display = 'inline-flex';
    } else {
        btn.disabled = false;
        if (text) text.style.display = 'inline-flex';
        if (loader) loader.style.display = 'none';
    }
}

// ── Utility: Risk Level Helpers ───────────────────────────────

function riskClass(level) {
    return (level || 'low').toLowerCase();
}

function riskEmoji(level) {
    const map = { low: '✅', medium: '⚠️', high: '🔶', critical: '🔴' };
    return map[(level || 'low').toLowerCase()] || '❓';
}

function formatDate(iso) {
    if (!iso) return '—';
    const d = new Date(iso);
    return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function typeEmoji(type) {
    const map = { phone: '📱', upi: '💳', website: '🌐', email: '📧', other: '📝' };
    return map[type] || '📝';
}

// ── Dashboard ─────────────────────────────────────────────────

async function loadDashboard() {
    try {
        const stats = await apiGet('/api/dashboard/stats');

        // Animate stat values
        animateValue('stat-total', stats.total_reports);
        animateValue('stat-unique', stats.unique_identifiers);
        animateValue('stat-highrisk', stats.high_risk_count);
        document.getElementById('stat-categories').textContent = stats.by_category.length;

        // Risk distribution chart
        renderRiskChart(stats.risk_distribution);

        // Category chart
        renderCategoryChart(stats.by_category);

        // Recent reports table
        renderRecentTable(stats.recent_reports);

    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

// Animated counter
function animateValue(id, endValue) {
    const el = document.getElementById(id);
    if (!el) return;
    if (endValue === 0) { el.textContent = '0'; return; }

    const duration = 800;
    const start = performance.now();
    const startVal = 0;

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = Math.round(startVal + (endValue - startVal) * eased);
        el.textContent = current.toLocaleString();
        if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
}

function renderRiskChart(data) {
    const container = document.getElementById('risk-chart');
    if (!data || data.length === 0) {
        container.innerHTML = `<div class="chart-placeholder">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
            <p>No risk data yet — submit a report to see stats!</p>
        </div>`;
        return;
    }

    const total = data.reduce((sum, d) => sum + d.count, 0);
    const order = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
    const sorted = order.map(level => data.find(d => d.risk_level === level) || { risk_level: level, count: 0 }).filter(d => d.count > 0);

    let html = '<div class="bar-chart">';
    sorted.forEach(d => {
        const pct = total > 0 ? Math.max((d.count / total) * 100, 8) : 0;
        const cls = riskClass(d.risk_level);
        html += `
            <div class="bar-row">
                <span class="bar-label">${d.risk_level}</span>
                <div class="bar-track">
                    <div class="bar-fill ${cls}" style="width:${pct}%">${d.count}</div>
                </div>
            </div>`;
    });
    html += '</div>';
    container.innerHTML = html;
}

function renderCategoryChart(data) {
    const container = document.getElementById('category-chart');
    if (!data || data.length === 0) {
        container.innerHTML = `<div class="chart-placeholder">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3"><path d="M21 12a9 9 0 1 1-9-9"/><path d="M21 3v9h-9"/></svg>
            <p>No scam categories recorded yet</p>
        </div>`;
        return;
    }

    const total = data.reduce((sum, d) => sum + d.count, 0);
    let html = '<div class="bar-chart">';
    data.slice(0, 6).forEach(d => {
        const pct = total > 0 ? Math.max((d.count / total) * 100, 8) : 0;
        const label = d.category.replace(/_/g, ' ');
        html += `
            <div class="bar-row">
                <span class="bar-label">${label}</span>
                <div class="bar-track">
                    <div class="bar-fill default" style="width:${pct}%">${d.count}</div>
                </div>
            </div>`;
    });
    html += '</div>';
    container.innerHTML = html;
}

function renderRecentTable(reports) {
    const tbody = document.getElementById('recent-tbody');
    if (!reports || reports.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="table-empty">No reports yet. Be the first to report a scam!</td></tr>';
        return;
    }

    tbody.innerHTML = reports.map(r => `
        <tr>
            <td><span class="type-badge">${typeEmoji(r.identifier_type)} ${r.identifier_type}</span></td>
            <td style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;">${escapeHtml(r.identifier_value)}</td>
            <td>${(r.category || 'unknown').replace(/_/g, ' ')}</td>
            <td><span class="risk-badge ${riskClass(r.risk_level)}">${riskEmoji(r.risk_level)} ${r.risk_level} (${r.risk_score})</span></td>
            <td style="white-space:nowrap;">${formatDate(r.reported_at)}</td>
        </tr>
    `).join('');
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

// ── Submit Report ─────────────────────────────────────────────

async function submitReport(e) {
    e.preventDefault();
    setLoading('report-submit-btn', true);

    const form = document.getElementById('report-form');
    const data = {
        identifier_type: form.identifier_type.value,
        identifier_value: form.identifier_value.value.trim(),
        description: form.description.value.trim(),
        reporter_name: form.reporter_name.value.trim() || 'Anonymous',
    };

    try {
        const result = await apiPost('/api/reports/', data);
        showToast('Report submitted successfully!', 'success');
        renderReportResult(result);
        form.reset();
    } catch (err) {
        showToast(err.message || 'Failed to submit report', 'error');
    } finally {
        setLoading('report-submit-btn', false);
    }
}

function renderReportResult(result) {
    const card = document.getElementById('report-result');
    const content = document.getElementById('report-result-content');

    const risk = result.risk || {};
    const ai = result.ai_analysis || {};
    const level = riskClass(risk.level);

    let iconClass = 'safe';
    let iconEmoji = '✅';
    if (risk.score >= 75) { iconClass = 'danger'; iconEmoji = '🚨'; }
    else if (risk.score >= 50) { iconClass = 'danger'; iconEmoji = '⚠️'; }
    else if (risk.score >= 25) { iconClass = 'warning'; iconEmoji = '⚠️'; }

    let html = `
        <div class="result-header">
            <div class="result-icon ${iconClass}">${iconEmoji}</div>
            <div>
                <div class="result-title">Report #${result.report_id} Submitted</div>
                <div class="result-subtitle">${result.message}</div>
            </div>
        </div>

        <div class="risk-meter">
            <div class="risk-meter-header">
                <span class="risk-meter-label">Risk Score</span>
                <span class="risk-meter-score ${level}">${risk.score}/100 — ${risk.level}</span>
            </div>
            <div class="risk-bar-outer">
                <div class="risk-bar-inner ${level}" style="width:${risk.score}%"></div>
            </div>
            ${risk.factors && risk.factors.length > 0 ? `
                <ul class="factors-list">
                    ${risk.factors.map(f => `
                        <li class="factor-item">
                            <span class="factor-dot ${level}"></span>
                            <span>${escapeHtml(f)}</span>
                        </li>`).join('')}
                </ul>` : ''}
        </div>`;

    if (ai && !ai.error) {
        html += `
            <div class="ai-section">
                <div class="ai-section-title">🤖 AI Analysis</div>
                <p class="ai-text">${escapeHtml(ai.explanation)}</p>
                ${ai.scam_type && ai.scam_type !== 'unknown' ? `<p class="ai-text" style="margin-top:8px;"><strong>Scam Type:</strong> ${escapeHtml(ai.scam_type)}</p>` : ''}
                ${ai.confidence ? `<p class="ai-text"><strong>AI Confidence:</strong> ${(ai.confidence * 100).toFixed(0)}%</p>` : ''}
                ${ai.advice ? `<div class="ai-advice">💡 <strong>Advice:</strong> ${escapeHtml(ai.advice)}</div>` : ''}
            </div>`;
    }

    content.innerHTML = html;
    card.style.display = 'block';
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ── Lookup Identifier ─────────────────────────────────────────

async function lookupIdentifier(e) {
    e.preventDefault();
    setLoading('lookup-submit-btn', true);

    const identifier = document.getElementById('lookup-input').value.trim();

    try {
        const result = await apiGet(`/api/reports/lookup/${encodeURIComponent(identifier)}`);
        renderLookupResult(result);
    } catch (err) {
        showToast(err.message || 'Lookup failed', 'error');
    } finally {
        setLoading('lookup-submit-btn', false);
    }
}

function renderLookupResult(result) {
    const card = document.getElementById('lookup-result');
    const content = document.getElementById('lookup-result-content');

    const count = result.report_count || 0;
    const risk = result.risk;

    let iconClass = 'safe';
    let iconEmoji = '✅';
    let title = 'No Reports Found';
    let subtitle = `"${escapeHtml(result.identifier)}" has not been reported yet.`;

    if (count > 0 && risk) {
        const level = riskClass(risk.level);
        if (risk.score >= 75) { iconClass = 'danger'; iconEmoji = '🚨'; }
        else if (risk.score >= 50) { iconClass = 'danger'; iconEmoji = '⚠️'; }
        else if (risk.score >= 25) { iconClass = 'warning'; iconEmoji = '⚠️'; }

        title = `Found ${count} Report${count > 1 ? 's' : ''}`;
        subtitle = `"${escapeHtml(result.identifier)}" has been reported ${count} time${count > 1 ? 's' : ''}.`;
    }

    let html = `
        <div class="result-header">
            <div class="result-icon ${iconClass}">${iconEmoji}</div>
            <div>
                <div class="result-title">${title}</div>
                <div class="result-subtitle">${subtitle}</div>
            </div>
        </div>`;

    if (risk) {
        const level = riskClass(risk.level);
        html += `
            <div class="risk-meter">
                <div class="risk-meter-header">
                    <span class="risk-meter-label">Aggregate Risk Score</span>
                    <span class="risk-meter-score ${level}">${risk.score}/100 — ${risk.level}</span>
                </div>
                <div class="risk-bar-outer">
                    <div class="risk-bar-inner ${level}" style="width:${risk.score}%"></div>
                </div>
                ${risk.factors && risk.factors.length > 0 ? `
                    <ul class="factors-list">
                        ${risk.factors.map(f => `
                            <li class="factor-item">
                                <span class="factor-dot ${level}"></span>
                                <span>${escapeHtml(f)}</span>
                            </li>`).join('')}
                    </ul>` : ''}
            </div>`;
    }

    if (result.reports && result.reports.length > 0) {
        html += `<div class="lookup-reports"><h3 class="chart-title" style="margin-bottom:12px;">Report History</h3>`;
        result.reports.forEach(r => {
            html += `
                <div class="lookup-report-item">
                    <div class="lookup-report-meta">
                        <span class="type-badge">${typeEmoji(r.identifier_type)} ${r.identifier_type}</span>
                        <span class="risk-badge ${riskClass(r.risk_level)}">${riskEmoji(r.risk_level)} ${r.risk_level} (${r.risk_score})</span>
                        <span style="color:var(--text-muted); font-size:0.8rem;">${formatDate(r.reported_at)}</span>
                    </div>
                    <div class="lookup-report-desc">${escapeHtml(r.description)}</div>
                </div>`;
        });
        html += '</div>';
    }

    content.innerHTML = html;
    card.style.display = 'block';
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ── AI Analyzer ───────────────────────────────────────────────

async function analyzeMessage(e) {
    e.preventDefault();
    setLoading('analyzer-submit-btn', true);

    const message = document.getElementById('analyzer-input').value.trim();

    try {
        const result = await apiPost('/api/analysis/', { message });
        renderAnalysisResult(result);
    } catch (err) {
        showToast(err.message || 'Analysis failed', 'error');
    } finally {
        setLoading('analyzer-submit-btn', false);
    }
}

function renderAnalysisResult(result) {
    const card = document.getElementById('analyzer-result');
    const content = document.getElementById('analyzer-result-content');

    let iconClass = 'safe';
    let iconEmoji = '✅';
    let title = 'Looks Safe';
    let subtitle = 'No strong indicators of fraud detected.';

    if (result.is_scam) {
        if (result.confidence >= 0.75) {
            iconClass = 'danger'; iconEmoji = '🚨';
            title = 'High Scam Probability';
            subtitle = `${(result.confidence * 100).toFixed(0)}% confidence this is a scam`;
        } else if (result.confidence >= 0.5) {
            iconClass = 'warning'; iconEmoji = '⚠️';
            title = 'Suspicious Content';
            subtitle = `${(result.confidence * 100).toFixed(0)}% confidence this may be a scam`;
        } else {
            iconClass = 'warning'; iconEmoji = '⚠️';
            title = 'Minor Red Flags';
            subtitle = 'Some suspicious patterns detected';
        }
    }

    let html = `
        <div class="result-header">
            <div class="result-icon ${iconClass}">${iconEmoji}</div>
            <div>
                <div class="result-title">${title}</div>
                <div class="result-subtitle">${subtitle}</div>
            </div>
        </div>`;

    if (result.scam_type && result.scam_type !== 'unknown') {
        html += `<p class="ai-text" style="margin-bottom:12px;"><strong>Identified Scam Type:</strong> <span class="risk-badge ${result.is_scam ? 'critical' : 'low'}">${escapeHtml(result.scam_type)}</span></p>`;
    }

    html += `
        <div class="ai-section">
            <div class="ai-section-title">🤖 AI Explanation</div>
            <p class="ai-text">${escapeHtml(result.explanation)}</p>
            ${result.advice ? `<div class="ai-advice">💡 <strong>Recommended Action:</strong> ${escapeHtml(result.advice)}</div>` : ''}
        </div>`;

    if (result.error) {
        html += `<div class="ai-advice" style="border-left-color:var(--danger); background:rgba(239,68,68,0.06); margin-top:12px;">⚠️ <strong>Note:</strong> ${escapeHtml(result.error)}</div>`;
    }

    content.innerHTML = html;
    card.style.display = 'block';
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
