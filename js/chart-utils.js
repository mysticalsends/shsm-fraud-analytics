/**
 * chart-utils.js — SHSM Analytics Hub
 * Shared Chart.js dark-theme configuration and formatting helpers.
 * Load this AFTER chart.js and BEFORE any page-specific chart scripts.
 */

/* ── Base chart config factory ──────────────────────────────────────────── */
// Note: DARK_OPTS is intentionally NOT defined here — each dashboard page
// defines its own version since the grid color varies between pages.
function baseChartConfig(scaleOverrides = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 300 },
    plugins: {
      legend: {
        labels: {
          color: '#5a6a82',
          font: { family: 'Space Mono', size: 10 },
          boxWidth: 10,
          padding: 8
        }
      }
    },
    scales: {
      x: {
        ticks: { color: '#5a6a82', font: { family: 'Space Mono', size: 9 }, maxRotation: 45 },
        grid:  { color: '#1a2540' }
      },
      y: {
        ticks: { color: '#5a6a82', font: { family: 'Space Mono', size: 9 } },
        grid:  { color: '#1a2540' }
      },
      ...scaleOverrides
    }
  };
}

/* ── Number formatters ──────────────────────────────────────────────────── */
const fmt = {
  /** $1.23B */
  billions: n => n == null ? '—' : '$' + (n / 1e9).toFixed(2) + 'B',
  /** $123M */
  millions: n => n == null ? '—' : '$' + (n / 1e6).toFixed(0) + 'M',
  /** $1.5M with one decimal */
  millionsD: n => n == null ? '—' : '$' + (n / 1e6).toFixed(1) + 'M',
  /** Compact: auto-selects B / M / K */
  compact: function(n) {
    if (n == null) return '—';
    if (Math.abs(n) >= 1e9) return '$' + (n / 1e9).toFixed(1) + 'B';
    if (Math.abs(n) >= 1e6) return '$' + (n / 1e6).toFixed(1) + 'M';
    if (Math.abs(n) >= 1e3) return '$' + (n / 1e3).toFixed(0) + 'K';
    return '$' + n.toLocaleString();
  },
  /** Plain integer with comma separator */
  int: n => n == null ? '—' : n.toLocaleString(),
  /** Percentage with one decimal */
  pct: n => n == null ? '—' : n.toFixed(1) + '%'
};
