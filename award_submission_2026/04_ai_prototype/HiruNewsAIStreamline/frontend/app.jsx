/**
 * HiruNews AI Streamline — Main React Application
 * Single-file React app with 6 screens, animations, and WebChannel bridge.
 *
 * Lotus Technologies (Pvt) Ltd
 * Developer: Mr. Vidath Dulanjith — DevOps Engineer
 * SLASSCOM SNIA 2026 — Best Tech for Good Software Innovation
 */

const { useState, useEffect, useRef, useCallback, useReducer } = React;

// ─────────────────────────────────────────────────────────────
// SVG ICONS (Lucide-style inline SVGs)
// ─────────────────────────────────────────────────────────────

const Icons = {
  Upload: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" /></svg>,
  Waveform: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 13a2 2 0 0 0 2-2V7a2 2 0 0 1 4 0v13a2 2 0 0 0 4 0V4a2 2 0 0 1 4 0v13a2 2 0 0 0 4 0v-4a2 2 0 0 1 2-2" /></svg>,
  Sparkles: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" /><path d="M5 3v4" /><path d="M19 17v4" /><path d="M3 5h4" /><path d="M17 19h4" /></svg>,
  CheckCircle: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>,
  ArrowRight: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>,
  ArrowLeft: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" /></svg>,
  LayoutDashboard: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="7" height="9" x="3" y="3" rx="1" /><rect width="7" height="5" x="14" y="3" rx="1" /><rect width="7" height="9" x="14" y="12" rx="1" /><rect width="7" height="5" x="3" y="16" rx="1" /></svg>,
  Bell: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" /></svg>,
  Settings: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" /><circle cx="12" cy="12" r="3" /></svg>,
  Sun: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="4" /><path d="M12 2v2" /><path d="M12 20v2" /><path d="m4.93 4.93 1.41 1.41" /><path d="m17.66 17.66 1.41 1.41" /><path d="M2 12h2" /><path d="M20 12h2" /><path d="m6.34 17.66-1.41 1.41" /><path d="m19.07 4.93-1.41 1.41" /></svg>,
  Moon: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" /></svg>,
  Check: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg>,
  X: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>,
  CloudUpload: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242" /><path d="M12 12v9" /><path d="m16 16-4-4-4 4" /></svg>,
  File: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" /><polyline points="14 2 14 8 20 8" /></svg>,
  Trash: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18" /><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" /><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" /></svg>,
  RefreshCw: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" /><path d="M8 16H3v5" /></svg>,
  Clock: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></svg>,
  Timer: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="10" y1="2" x2="14" y2="2" /><line x1="12" y1="14" x2="12" y2="8" /><circle cx="12" cy="14" r="8" /></svg>,
  Shield: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>,
  Pencil: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" /></svg>,
  Play: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3" /></svg>,
  FolderOpen: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2" /></svg>,
  Info: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="12" y1="16" x2="12" y2="12" /><line x1="12" y1="8" x2="12.01" y2="8" /></svg>,
  ChevronLeft: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6" /></svg>,
  ChevronRight: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6" /></svg>,
  Menu: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" y1="12" x2="20" y2="12" /><line x1="4" y1="6" x2="20" y2="6" /><line x1="4" y1="18" x2="20" y2="18" /></svg>,
  TrendingUp: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17" /><polyline points="16 7 22 7 22 13" /></svg>,
  TrendingDown: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7" /><polyline points="16 17 22 17 22 11" /></svg>,
  AlertTriangle: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" /></svg>,
  Loader: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56" /></svg>,
  Plus: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>,
  ExternalLink: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" /><polyline points="15 3 21 3 21 9" /><line x1="10" y1="14" x2="21" y2="3" /></svg>,
  ChevronDown: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6" /></svg>,
  ChevronUp: (p) => <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m18 15-6-6-6 6" /></svg>,
};

const iconSize = { width: 20, height: 20 };
const iconSm = { width: 16, height: 16 };
const iconLg = { width: 24, height: 24 };
const iconXl = { width: 48, height: 48 };


// ─────────────────────────────────────────────────────────────
// MOCK DATA (inline for browser-only mode)
// ─────────────────────────────────────────────────────────────

const MOCK_TRANSCRIPTS = [
  { speaker: "Speaker 1", timestamp: "00:00:02", text: "මෙය සිදුව තිබෙන්නේ අනවබෝධය නිසා බව අපි පැහැදිලිව කිව යුතුය." },
  { speaker: "Speaker 2", timestamp: "00:00:18", text: "වෘත්තිය සමිති ක්\u200Dරියාමාර්ගයකදී හමුදාව යොදවන්න නම් 20ක් අරගන්නේ නැහැ. එහෙනම් 200කට 300කට පුහුණුව ලබා දෙන්න තිබුණා." },
  { speaker: "Speaker 1", timestamp: "00:00:45", text: "දුම්රිය රියැදුරු පුහුණුවට හමුදාව බඳවා ගැනීම තාවකාලිකව අත්හිටුවූවා. මේ පිළිබඳ සම්පූර්ණ විමර්ශනයක් සිදු කරනවා." },
  { speaker: "Speaker 3", timestamp: "00:01:12", text: "කෝච්චි පාරවල්, මහාමාර්ග හදනවා නම් ඒකට අදාළ සැලැස්මක් ඉදිරිපත් කළ යුතුයි." },
  { speaker: "Speaker 2", timestamp: "00:01:38", text: "දුම්රිය ධාවනය කිරීම කිසිම ගැටලුවක් නැහැ. අපි ඒ සඳහා සුදානම්." },
  { speaker: "Speaker 1", timestamp: "00:02:05", text: "මෙම තත්ත්වය පිළිබඳව ජනාධිපතිතුමාට වාර්තා කළා. ඉදිරි දින කිහිපය තුළ නිල නිවේදනයක් නිකුත් කරනවා." },
];

const MOCK_SUGGESTIONS = [
  {
    id: 1, topic_bed: "දුම්රිය රියැදුරු පුහුණුවට හමුදාව බඳවා ගැනීම අත්හිටුවයි",
    tag_lines: ["වෘත්තිය සමිති ක්\u200Dරියාමාර්ගයකදී හමුදාව යොදවන්න 20ක් ගන්නේ නැහැ", "200කට 300කට පුහුණුව ලබා දෙන්න තිබුණා", "දුම්රිය ධාවනය කිරීම කිසිම ගැටලුවක් නැහැ"],
    white_bed: "කෝච්චි පාරවල් මහාමාර්ග හදනවා නම් සැලැස්මක් ඉදිරිපත් කළ යුතුයි",
    source_excerpt: "වෘත්තිය සමිති ක්\u200Dරියාමාර්ගයකදී හමුදාව යොදවන්න නම් 20ක් අරගන්නේ..."
  },
  {
    id: 2, topic_bed: "දිට්වා සුළිකුණාටුවේදී ත්\u200Dරිවිධ හමුදාව කටයුතු කළ විදිය",
    tag_lines: ["මාතර දිස්ත්\u200Dරික්කයේ පවුල් 850ක් අවතැන්", "ආපදා සහන මධ්\u200Dයස්ථාන 12ක් විවෘත කෙරේ", "ගංවතුර තත්ත්වය තවදුරටත් බරපතළ"],
    white_bed: "ත්\u200Dරිවිධ හමුදාව මුළු රට පුරා ආපදා සහන මෙහෙයුම් ක්\u200Dරියාත්මක කරමින් සිටී",
    source_excerpt: "දිට්වා සුළිකුණාටුවේදී ත්\u200Dරිවිධ හමුදාව කටයුතු කළ විදිය අපි දැන් බලමු..."
  },
  {
    id: 3, topic_bed: "අකුරේගොඩ වෙඩි තැබීමේ සිද්ධිය පිළිබඳ නව අනාවරණ",
    tag_lines: ["ත්\u200Dරිරෝද රථයෙන් පැමිණි අයගේ අනන්\u200Dයතාව හඳුනාගෙන නැහැ", "ගිනි අවි සහිත බෑගය අකුරේගොඩදී ලබා දෙන අයුරු CCTV වල", "සහෝදරයින් මෝටර් රථයෙන් හෝකන්දර දෙසට ගිය අයුරු"],
    white_bed: "නීතිඥවරයා සහ බිරිඳ සාමාන්\u200Dය පරිදි සුපිරි වෙළඳසැලට පැමිණ සිටියදී ප්\u200Dරහාරයට ලක් වී ඇත",
    source_excerpt: "ගිනි අවි සහිත බෑගය අකුරේගොඩදී වෙඩික්කරුවන්ට ලබා දෙන..."
  },
  {
    id: 4, topic_bed: "පොලිස් ඇමතිවරයා ඉල්ලා අස්වීමට ජනතා ඉල්ලීමක්",
    tag_lines: ["එදා එල්ටීටීඊ සහ 88/89 කාලය වගේ තත්ත්වයක් ද", "කොන්ද පණ නැති අයට ඇමතිකම් දුන්නාම රටම විනාශයි", "එක රටක් එක නීතියක් කියපු ආණ්ඩුවට කරන්න දෙයක් නැහැ"],
    white_bed: "නීතියේ ආධිපත්\u200Dයය සුරකින්න බැහැ නම් ආණ්ඩුව ඉල්ලා අස් විය යුතුය",
    source_excerpt: "දැන් ජනතාව පාරේ ගමන් කරන්නේ බියෙන්. මේ තත්ත්වයට ආණ්ඩුව..."
  },
  {
    id: 5, topic_bed: "ආර්ථිකය ස්ථාවර කිරීමේ නව ප්\u200Dරතිපත්ති රාමුව",
    tag_lines: ["දළ දේශීය නිෂ්පාදිතයේ වර්ධනය සියයට 4.2ක්", "ණය ප්\u200Dරතිව්\u200Dයුහගත කිරීමේ සාකච්ඡා අවසන් අදියරේ", "සංචාරක ආදායම ඩොලර් බිලියන 3 ඉක්මවයි"],
    white_bed: "ජාත්\u200Dයන්තර මුල්\u200Dය අරමුදල සමඟ ඊළඟ සමාලෝචන සාර්ථකව නිම කිරීමට අපේක්ෂා කරනවා",
    source_excerpt: "ආර්ථිකය ස්ථාවර කිරීමේ නව ප්\u200Dරතිපත්ති රාමුව ඉදිරිපත් කිරීමට..."
  },
];


// ─────────────────────────────────────────────────────────────
// UTILITY FUNCTIONS
// ─────────────────────────────────────────────────────────────

function wordCount(text) {
  if (!text || !text.trim()) return 0;
  return text.trim().split(/\s+/).length;
}

function formatTimestamp() {
  const now = new Date();
  return now.toISOString().replace('T', ' ').split('.')[0];
}

function generateSessionName() {
  const now = new Date();
  const h = String(now.getHours()).padStart(2, '0');
  const m = String(now.getMinutes()).padStart(2, '0');
  return `SESSION_${h}${m}`;
}


// ─────────────────────────────────────────────────────────────
// ANIMATED WRAPPER COMPONENT
// ─────────────────────────────────────────────────────────────

function AnimatedPage({ children, keyName }) {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 30);
    return () => clearTimeout(t);
  }, []);
  return (
    <div style={{
      opacity: visible ? 1 : 0,
      transform: visible ? 'translateX(0)' : 'translateX(20px)',
      transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
    }}>
      {children}
    </div>
  );
}

function StaggerChild({ children, index }) {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 60 + index * 100);
    return () => clearTimeout(t);
  }, [index]);
  return (
    <div style={{
      opacity: visible ? 1 : 0,
      transform: visible ? 'translateY(0)' : 'translateY(16px)',
      transition: 'all 0.35s cubic-bezier(0.4, 0, 0.2, 1)',
    }}>
      {children}
    </div>
  );
}


// ─────────────────────────────────────────────────────────────
// TOAST SYSTEM
// ─────────────────────────────────────────────────────────────

function ToastContainer({ toasts, onDismiss }) {
  return (
    <div className="toast-container">
      {toasts.map((t, i) => (
        <div key={t.id} className={`toast ${t.type}`} style={{
          animation: 'slideInRight 0.3s ease-out',
        }}>
          <div className="toast-icon">
            {t.type === 'success' && <Icons.CheckCircle {...iconSm} style={{ color: 'var(--success)' }} />}
            {t.type === 'error' && <Icons.X {...iconSm} style={{ color: 'var(--error)' }} />}
            {t.type === 'warning' && <Icons.AlertTriangle {...iconSm} style={{ color: 'var(--warning)' }} />}
            {t.type === 'info' && <Icons.Info {...iconSm} style={{ color: 'var(--info)' }} />}
          </div>
          <span className="toast-message">{t.message}</span>
          <button className="toast-close" onClick={() => onDismiss(t.id)}>
            <Icons.X {...iconSm} />
          </button>
        </div>
      ))}
      <style>{`
        @keyframes slideInRight {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `}</style>
    </div>
  );
}


// ─────────────────────────────────────────────────────────────
// TOP BAR COMPONENT
// ─────────────────────────────────────────────────────────────

function TopBar({ theme, onToggleTheme, sessionName }) {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <img src="assets/logo.svg" alt="Logo" className="topbar-logo" />
        <span className="topbar-brand">
          HiruNews <span className="ai-text">AI</span> Streamline
        </span>
      </div>

      <div className="topbar-center">
        <div className="session-pill">
          📁 {sessionName || 'No Active Session'}
        </div>
      </div>

      <div className="topbar-right">
        <button className="topbar-icon-btn" title="Notifications">
          <Icons.Bell {...iconSize} />
          <span className="notification-dot"></span>
        </button>

        <button className="topbar-icon-btn" title="Settings">
          <Icons.Settings {...iconSize} />
        </button>

        <button className="topbar-icon-btn" onClick={onToggleTheme}
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}>
          {theme === 'dark'
            ? <Icons.Sun {...iconSize} />
            : <Icons.Moon {...iconSize} />
          }
        </button>

      </div>
    </header>
  );
}


// ─────────────────────────────────────────────────────────────
// SIDEBAR COMPONENT
// ─────────────────────────────────────────────────────────────

const NAV_ITEMS = [
  { key: 'upload', label: 'Upload', icon: Icons.Upload, ai: false },
  { key: 'transcription', label: 'Transcription', icon: Icons.Waveform, ai: false },
  { key: 'suggestions', label: 'AI Suggestions', icon: Icons.Sparkles, ai: true },
  { key: 'approval', label: 'Editor Review', icon: Icons.CheckCircle, ai: false },
  { key: 'handoff', label: 'Handoff', icon: Icons.ArrowRight, ai: false },
  { key: 'dashboard', label: 'Dashboard', icon: Icons.LayoutDashboard, ai: false },
];

function Sidebar({ currentScreen, onNavigate, collapsed, onToggleCollapse }) {
  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        {!collapsed && <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-muted)' }}>NAVIGATION</span>}
        <button className="sidebar-toggle" onClick={onToggleCollapse} title="Toggle sidebar">
          {collapsed ? <Icons.ChevronRight {...iconSize} /> : <Icons.ChevronLeft {...iconSize} />}
        </button>
      </div>

      {!collapsed && <div className="sidebar-section-label">Workflow</div>}

      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <button key={item.key}
              className={`nav-item ${currentScreen === item.key ? 'active' : ''} ${item.ai ? 'ai-item' : ''}`}
              onClick={() => onNavigate(item.key)}
              title={item.label}
            >
              <Icon {...iconSize} />
              {!collapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        {!collapsed && (
          <>
            <div className="sidebar-footer-text">Lotus Technologies (Pvt) Ltd</div>
            <div className="sidebar-footer-version">HiruNewsAIStreamline v2.1.0</div>
          </>
        )}
      </div>
    </aside>
  );
}


// ─────────────────────────────────────────────────────────────
// SCREEN 1: UPLOAD
// ─────────────────────────────────────────────────────────────

function UploadScreen({ state, dispatch, onStartProcessing, addToast }) {
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => { e.preventDefault(); setDragging(true); };
  const handleDragLeave = () => setDragging(false);
  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      dispatch({ type: 'ADD_FILES', payload: files.map(f => ({ name: f.name, size: f.size, type: f.type, path: f.path || f.name, addedAt: formatTimestamp() })) });
      addToast('success', `${files.length} file(s) added`);
    }
  };
  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      dispatch({ type: 'ADD_FILES', payload: files.map(f => ({ name: f.name, size: f.size, type: f.type, path: f.path || f.name, addedAt: formatTimestamp() })) });
      addToast('success', `${files.length} file(s) added`);
    }
  };
  const removeFile = (idx) => dispatch({ type: 'REMOVE_FILE', payload: idx });

  const canStart = state.files.length > 0 && state.metadata.reporter;

  return (
    <AnimatedPage keyName="upload">
      <div className="page-header">
        <h1 className="page-title">
          <Icons.Upload {...iconLg} /> Upload Source Material
        </h1>
        <p className="page-subtitle">Drop raw news content to begin AI-assisted tagline generation</p>
      </div>

      {/* Drop Zone */}
      <div className={`drop-zone ${dragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver} onDragLeave={handleDragLeave} onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}>
        <input type="file" ref={fileInputRef} style={{ display: 'none' }} multiple
          accept=".mp3,.mp4,.wav,.m4a,.txt,.doc,.docx,.pdf" onChange={handleFileSelect} />
        <div className="drop-zone-icon float-animation">
          <Icons.CloudUpload style={{ width: 56, height: 56 }} />
        </div>
        <div className="drop-zone-text">Drop files here or click to browse</div>
        <div className="drop-zone-hint">Supports: Audio (MP3, WAV, M4A), Video (MP4), Documents (TXT, DOC, PDF)</div>
        <div className="file-type-badges">
          <span className="badge badge-info">Audio</span>
          <span className="badge badge-ai">Video</span>
          <span className="badge badge-neutral">Document</span>
        </div>
      </div>

      {/* File List */}
      {state.files.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)', marginTop: 'var(--space-5)' }}>
          {state.files.map((file, i) => (
            <StaggerChild key={i} index={i}>
              <div className="file-row">
                <div className="file-icon"><Icons.File {...iconSize} /></div>
                <div className="file-info">
                  <div className="file-name">{file.name}</div>
                  <div className="file-meta">
                    <span>{(file.size / 1024).toFixed(1)} KB</span>
                    <span>{file.addedAt}</span>
                  </div>
                </div>
                <div className="progress-bar" style={{ width: 80 }}>
                  <div className="progress-fill" style={{ width: '100%' }}></div>
                </div>
                <button className="btn btn-ghost btn-sm" onClick={(e) => { e.stopPropagation(); removeFile(i); }}>
                  <Icons.Trash {...iconSm} />
                </button>
              </div>
            </StaggerChild>
          ))}
        </div>
      )}

      {/* Bulletin Metadata */}
      <div className="card" style={{ marginTop: 'var(--space-6)' }}>
        <div className="card-header">
          <h3 className="card-title">Bulletin Metadata</h3>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-5)' }}>
          <div className="form-group">
            <label className="form-label">Reporter Name</label>
            <input className="input" placeholder="Enter reporter name"
              value={state.metadata.reporter}
              onChange={(e) => dispatch({ type: 'SET_METADATA', payload: { reporter: e.target.value } })} />
          </div>
          <div className="form-group">
            <label className="form-label">Location</label>
            <input className="input" placeholder="Enter location"
              value={state.metadata.location}
              onChange={(e) => dispatch({ type: 'SET_METADATA', payload: { location: e.target.value } })} />
          </div>
          <div className="form-group">
            <label className="form-label">Bulletin Slot</label>
            <select className="select"
              value={state.metadata.bulletinSlot}
              onChange={(e) => dispatch({ type: 'SET_METADATA', payload: { bulletinSlot: e.target.value } })}>
              <option value="11:55 AM">🕐 11:55 AM</option>
              <option value="6:55 PM">🕐 6:55 PM</option>
              <option value="9:55 PM">🕐 9:55 PM</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Priority</label>
            <div className="segmented-control">
              {['Breaking', 'Headline', 'Minor'].map((p) => (
                <button key={p} className={`segment ${state.metadata.priority === p ? 'active' : ''}`}
                  onClick={() => dispatch({ type: 'SET_METADATA', payload: { priority: p } })}>
                  {p}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Action Bar */}
      <div className="action-bar">
        <button className="btn btn-secondary">Save Draft</button>
        <button className="btn btn-primary" disabled={!canStart} onClick={onStartProcessing}>
          Start AI Processing <Icons.ArrowRight {...iconSm} />
        </button>
      </div>
    </AnimatedPage>
  );
}


// ─────────────────────────────────────────────────────────────
// SCREEN 2: TRANSCRIPTION
// ─────────────────────────────────────────────────────────────

function TranscriptionScreen({ state, dispatch, onBack, onContinue }) {
  const { transcriptionStatus, transcriptionProgress, transcript } = state;

  // Generate waveform bars
  const waveformBars = Array.from({ length: 60 }, (_, i) => {
    const h = 10 + Math.random() * 50;
    return <div key={i} className="waveform-bar" style={{ height: h + '%' }} />;
  });

  return (
    <AnimatedPage keyName="transcription">
      <div className="page-header">
        <h1 className="page-title">
          <Icons.Waveform {...iconLg} /> Transcription & Speaker Diarization
        </h1>
      </div>

      {/* Processing Banner */}
      <div className={`processing-banner ${transcriptionStatus === 'processing' ? 'active' : transcriptionStatus === 'complete' ? 'complete' : transcriptionStatus === 'error' ? 'error' : 'active'}`}
        style={{ marginBottom: 'var(--space-6)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
          {transcriptionStatus === 'processing' && (<>
            <Icons.Loader className="spin" {...iconSize} style={{ color: 'var(--ai-accent)' }} />
            <span>🪄 AI is transcribing your content... {transcriptionProgress}%</span>
          </>)}
          {transcriptionStatus === 'complete' && (<>
            <Icons.CheckCircle {...iconSize} style={{ color: 'var(--success)' }} />
            <span style={{ color: 'var(--success)' }}>✓ Transcription complete</span>
          </>)}
          {transcriptionStatus === 'error' && (<>
            <Icons.X {...iconSize} style={{ color: 'var(--error)' }} />
            <span style={{ color: 'var(--error)' }}>✗ Error — retry</span>
          </>)}
          {transcriptionStatus === 'idle' && (<>
            <Icons.Loader className="spin" {...iconSize} style={{ color: 'var(--ai-accent)' }} />
            <span>Preparing transcription...</span>
          </>)}
        </div>
        {(transcriptionStatus === 'processing' || transcriptionStatus === 'idle') && (
          <div className="progress-bar" style={{ marginTop: 'var(--space-3)' }}>
            <div className="progress-fill" style={{ width: `${transcriptionProgress || 5}%` }}></div>
          </div>
        )}
      </div>

      {/* Two Column: Source + Transcript */}
      {transcript.length > 0 && (
        <div className="two-col">
          {/* Left: Source Preview */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title"><Icons.File {...iconSm} /> Source File</h3>
            </div>
            <div className="waveform">{waveformBars}</div>
            <div style={{ marginTop: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span className="form-label">Duration</span>
                <span className="mono" style={{ color: 'var(--text-secondary)' }}>02:35</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span className="form-label">Format</span>
                <span className="mono" style={{ color: 'var(--text-secondary)' }}>audio/wav</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span className="form-label">Segments</span>
                <span className="mono" style={{ color: 'var(--text-secondary)' }}>{transcript.length}</span>
              </div>
            </div>
            <button className="btn btn-ghost btn-sm" style={{ marginTop: 'var(--space-4)', width: '100%' }}>
              <Icons.Play {...iconSm} /> Play Audio
            </button>
          </div>

          {/* Right: Transcript */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Transcript with Speaker Diarization</h3>
            </div>
            <div style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 'var(--space-2)', marginBottom: 'var(--space-4)' }}>
              <Icons.Info {...iconSm} /> Diarization is a GPT-based prototype heuristic
            </div>
            <div style={{ maxHeight: 400, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              {transcript.map((seg, i) => {
                const speakerNum = parseInt(seg.speaker.replace('Speaker ', '')) || 1;
                const avatarClass = `speaker-avatar s${Math.min(speakerNum, 4)}`;
                return (
                  <StaggerChild key={i} index={i}>
                    <div className="speaker-block">
                      <div className={avatarClass}>S{speakerNum}</div>
                      <div style={{ flex: 1 }}>
                        <div className="speaker-meta">
                          <span className="speaker-name">{seg.speaker}</span>
                          <span className="speaker-time">{seg.timestamp}</span>
                        </div>
                        <div className="speaker-text">{seg.text}</div>
                      </div>
                    </div>
                  </StaggerChild>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Action Bar */}
      <div className="action-bar">
        <button className="btn btn-ghost" onClick={onBack}>
          <Icons.ArrowLeft {...iconSm} /> Back
        </button>
        <div className="action-bar-right">
          <button className="btn btn-secondary">
            <Icons.RefreshCw {...iconSm} /> Regenerate
          </button>
          <button className="btn btn-primary" disabled={transcript.length === 0} onClick={onContinue}>
            Continue to AI Suggestions <Icons.ArrowRight {...iconSm} />
          </button>
        </div>
      </div>
    </AnimatedPage>
  );
}


// ─────────────────────────────────────────────────────────────
// SCREEN 3: AI SUGGESTIONS
// ─────────────────────────────────────────────────────────────

function SuggestionsScreen({ state, dispatch, onBack, onContinue, addToast }) {
  const { suggestions, selectedSuggestions } = state;

  const toggleSelect = (id) => dispatch({ type: 'TOGGLE_SUGGESTION', payload: id });

  const updateSuggestion = (id, field, value) => {
    dispatch({ type: 'UPDATE_SUGGESTION', payload: { id, field, value } });
  };

  const selectedCount = selectedSuggestions.length;

  return (
    <AnimatedPage keyName="suggestions">
      <div className="page-header">
        <h1 className="page-title">
          <Icons.Sparkles {...iconLg} style={{ color: 'var(--ai-accent)' }} /> AI Tagline Suggestions
        </h1>
      </div>

      {/* AI Banner */}
      <div className="ai-banner" style={{ marginBottom: 'var(--space-6)' }}>
        <Icons.Shield {...iconSize} style={{ color: 'var(--ai-accent)' }} />
        <span>✨ Generated by AI — Requires Senior Editor Approval Before Broadcast</span>
      </div>

      {/* Suggestion Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-5)' }}>
        {suggestions.map((sug, i) => {
          const isSelected = selectedSuggestions.includes(sug.id);
          const topicWc = wordCount(sug.topic_bed);
          const whiteWc = wordCount(sug.white_bed);

          return (
            <StaggerChild key={sug.id} index={i}>
              <div className={`suggestion-card ${isSelected ? 'selected' : ''}`}>
                {/* Header */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-4)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                    {/* Checkbox */}
                    <div className={`checkbox ${isSelected ? 'checked' : ''}`}
                      onClick={() => toggleSelect(sug.id)} style={{ cursor: 'pointer' }}>
                      <Icons.Check {...{ width: 14, height: 14 }} />
                    </div>
                    <span style={{ fontSize: 15, fontWeight: 600, color: 'var(--text-primary)' }}>Suggestion {sug.id}</span>
                    {isSelected && <span className="badge badge-ai">Selected</span>}
                  </div>
                  <button className="btn btn-ghost btn-sm">
                    <Icons.RefreshCw {...iconSm} /> Regenerate
                  </button>
                </div>

                {/* Topic Bed */}
                <div className="suggestion-section">
                  <div className="suggestion-section-label">
                    <span>Topic Bed</span>
                    <span className="suggestion-section-hint">(Red background, max 12 words)</span>
                  </div>
                  <div className="suggestion-input-row">
                    <div className="color-bar red"></div>
                    <input className="input" value={sug.topic_bed}
                      onChange={(e) => updateSuggestion(sug.id, 'topic_bed', e.target.value)}
                      style={{ fontFamily: "'Noto Sans Sinhala', 'Inter', sans-serif" }} />
                  </div>
                  <div className={`word-count ${topicWc > 12 ? 'over' : topicWc >= 11 ? 'warn' : 'ok'}`}>
                    {topicWc} / 12 words
                  </div>
                </div>

                {/* Tag Lines */}
                <div className="suggestion-section">
                  <div className="suggestion-section-label">
                    <span>TAG Lines</span>
                    <span className="suggestion-section-hint">(One per line, max 9 words each)</span>
                  </div>
                  <div className="suggestion-input-row">
                    <div className="color-bar orange"></div>
                    <textarea className="textarea" rows={3}
                      value={sug.tag_lines.join('\n')}
                      onChange={(e) => updateSuggestion(sug.id, 'tag_lines', e.target.value.split('\n'))}
                      style={{ fontFamily: "'Noto Sans Sinhala', 'Inter', sans-serif", lineHeight: 2 }} />
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--space-3)' }}>
                    {sug.tag_lines.map((line, li) => {
                      const wc = wordCount(line);
                      return <span key={li} className={`word-count ${wc > 9 ? 'over' : wc >= 8 ? 'warn' : 'ok'}`}>
                        L{li + 1}: {wc}/9
                      </span>;
                    })}
                  </div>
                </div>

                {/* White Bed */}
                <div className="suggestion-section">
                  <div className="suggestion-section-label">
                    <span>White Bed</span>
                    <span className="suggestion-section-hint">(White background, max 15 words)</span>
                  </div>
                  <div className="suggestion-input-row">
                    <div className="color-bar white"></div>
                    <input className="input" value={sug.white_bed}
                      onChange={(e) => updateSuggestion(sug.id, 'white_bed', e.target.value)}
                      style={{ fontFamily: "'Noto Sans Sinhala', 'Inter', sans-serif" }} />
                  </div>
                  <div className={`word-count ${whiteWc > 15 ? 'over' : whiteWc >= 14 ? 'warn' : 'ok'}`}>
                    {whiteWc} / 15 words
                  </div>
                </div>

                {/* Source */}
                <div className="suggestion-source">
                  Source: {sug.source_excerpt}
                </div>
              </div>
            </StaggerChild>
          );
        })}

        {/* Add Manual */}
        <button className="btn btn-ghost" style={{
          border: '2px dashed var(--border-strong)',
          borderRadius: 'var(--radius-xl)',
          padding: 'var(--space-5)',
          width: '100%',
          justifyContent: 'center',
        }}>
          <Icons.Plus {...iconSize} /> Add Manual Suggestion
        </button>
      </div>

      {/* Action Bar */}
      <div className="action-bar">
        <button className="btn btn-ghost" onClick={onBack}>
          <Icons.ArrowLeft {...iconSm} /> Back
        </button>
        <div className="action-bar-right">
          <span className="action-bar-info">{selectedCount} of {suggestions.length} suggestions selected</span>
          <button className="btn btn-primary" disabled={selectedCount === 0} onClick={onContinue}>
            Proceed to Approval <Icons.ArrowRight {...iconSm} />
          </button>
        </div>
      </div>
    </AnimatedPage>
  );
}


// ─────────────────────────────────────────────────────────────
// SCREEN 4: EDITOR APPROVAL
// ─────────────────────────────────────────────────────────────

const CHECKLIST_ITEMS = [
  "Facts verified against source material",
  "No defamatory or legally sensitive content",
  "Complies with broadcasting standards",
  "Sinhala grammar and script reviewed",
  "Source confidentiality preserved",
];

function ApprovalScreen({ state, dispatch, onBack, onApprove, addToast }) {
  const { suggestions, selectedSuggestions, approvalChecklist, editorNotes, metadata } = state;
  const selectedSugs = suggestions.filter(s => selectedSuggestions.includes(s.id));
  const [expanded, setExpanded] = useState(true);

  const checkedCount = approvalChecklist.filter(Boolean).length;
  const allChecked = checkedCount === CHECKLIST_ITEMS.length;

  const toggleCheck = (idx) => {
    dispatch({ type: 'TOGGLE_CHECKLIST', payload: idx });
  };

  return (
    <AnimatedPage keyName="approval">
      <div className="page-header">
        <h1 className="page-title">
          <Icons.CheckCircle {...iconLg} /> Editor Review & Approval
        </h1>
      </div>

      {/* Warning Banner */}
      <div className="warning-banner" style={{ marginBottom: 'var(--space-6)' }}>
        <Icons.AlertTriangle {...iconSize} />
        <span>⚠ No AI-generated content may be broadcast without completing all items below.</span>
      </div>

      {/* Review Summary Card */}
      <div className="card" style={{ marginBottom: 'var(--space-5)' }}>
        <div className="card-header">
          <h3 className="card-title">Review Summary</h3>
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-3)' }}>
          <span className="badge badge-neutral">Session: {generateSessionName()}</span>
          <span className="badge badge-info">Bulletin: {metadata.bulletinSlot}</span>
          <span className="badge badge-warning">Priority: {metadata.priority}</span>
          <span className="badge badge-ai">{selectedSugs.length} tagline sets</span>
          <span className="badge badge-neutral">{formatTimestamp()}</span>
        </div>
      </div>

      {/* Content Preview Card */}
      <div className="card" style={{ marginBottom: 'var(--space-5)' }}>
        <div className="card-header">
          <h3 className="card-title">Content Preview</h3>
          <button className="btn btn-ghost btn-sm" onClick={() => setExpanded(!expanded)}>
            {expanded ? <><Icons.ChevronUp {...iconSm} /> Collapse</> : <><Icons.ChevronDown {...iconSm} /> Expand</>}
          </button>
        </div>
        {expanded && selectedSugs.map((sug, i) => (
          <div key={sug.id} className="tagline-preview" style={{ marginBottom: 'var(--space-3)' }}>
            <div className="tagline-preview-strip red-bed">{sug.topic_bed}</div>
            {sug.tag_lines.map((line, li) => (
              <div key={li} className="tagline-preview-strip orange-bed">{line}</div>
            ))}
            <div className="tagline-preview-strip white-bed">{sug.white_bed}</div>
          </div>
        ))}
      </div>

      {/* Approval Checklist */}
      <div className="card" style={{ marginBottom: 'var(--space-5)' }}>
        <div className="card-header">
          <h3 className="card-title"><Icons.Shield {...iconSm} /> Approval Checklist — All items required</h3>
        </div>
        <div style={{ marginBottom: 'var(--space-4)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
            <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{checkedCount} of {CHECKLIST_ITEMS.length} complete</span>
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${(checkedCount / CHECKLIST_ITEMS.length) * 100}%` }}></div>
          </div>
        </div>
        {CHECKLIST_ITEMS.map((item, idx) => (
          <div key={idx} className="checkbox-wrapper" onClick={() => toggleCheck(idx)}>
            <div className={`checkbox ${approvalChecklist[idx] ? 'checked' : ''}`}>
              <Icons.Check {...{ width: 14, height: 14 }} />
            </div>
            <span className="checkbox-label">{item}</span>
          </div>
        ))}
      </div>

      {/* Editor Notes */}
      <div className="card" style={{ marginBottom: 'var(--space-5)' }}>
        <div className="card-header">
          <h3 className="card-title">Editor Notes / Comments (Optional)</h3>
        </div>
        <textarea className="textarea" rows={3}
          placeholder="e.g. NOV 6.55 Bulletin"
          value={editorNotes}
          onChange={(e) => dispatch({ type: 'SET_EDITOR_NOTES', payload: e.target.value })} />
        <div style={{ textAlign: 'right', fontSize: 12, color: 'var(--text-muted)', marginTop: 'var(--space-1)' }}>
          {(editorNotes || '').length} characters
        </div>
      </div>

      {/* Action Bar */}
      <div className="action-bar">
        <button className="btn btn-ghost" onClick={onBack}>
          <Icons.ArrowLeft {...iconSm} /> Back
        </button>
        <div className="action-bar-right">
          <button className="btn btn-danger btn-sm" onClick={() => addToast('error', 'Session rejected.')}>
            Reject
          </button>
          <button className="btn btn-warning btn-sm" onClick={() => addToast('warning', 'Changes requested. Returning to suggestions.')}>
            Request Changes
          </button>
          <button className={`btn btn-success ${allChecked ? 'pulse-animation' : ''}`}
            disabled={!allChecked} onClick={onApprove}>
            Approve ✓
          </button>
        </div>
      </div>
    </AnimatedPage>
  );
}


// ─────────────────────────────────────────────────────────────
// SCREEN 5: HANDOFF
// ─────────────────────────────────────────────────────────────

function HandoffScreen({ state, dispatch, onBack, addToast }) {
  const { suggestions, selectedSuggestions, metadata, exportStatus, editorNotes } = state;
  const selectedSugs = suggestions.filter(s => selectedSuggestions.includes(s.id));
  const [sessionName, setSessionName] = useState(generateSessionName());
  const [outputFolder, setOutputFolder] = useState('');
  const [exported, setExported] = useState(false);
  const [exportPath, setExportPath] = useState('');

  const browseFolderHandler = () => {
    if (window.bridge && window.bridge.browse_folder) {
      const resultStr = window.bridge.browse_folder();
      try {
        const result = JSON.parse(resultStr);
        if (result.folder) setOutputFolder(result.folder);
      } catch (e) {
        // Async callback style
        window.bridge.browse_folder(function (r) {
          try {
            const res = JSON.parse(r);
            if (res.folder) setOutputFolder(res.folder);
          } catch (ex) { }
        });
      }
    }
  };

  const doExport = () => {
    const approvedContent = {
      bulletin_slot: metadata.bulletinSlot,
      priority: metadata.priority,
      editor_notes: editorNotes || '',
      suggestions: selectedSugs,
    };

    if (window.bridge && window.bridge.export_handoff) {
      try {
        const resultStr = window.bridge.export_handoff(sessionName, outputFolder, JSON.stringify(approvedContent));
        const result = JSON.parse(resultStr);
        if (result.success) {
          setExported(true);
          setExportPath(result.file_path);
          addToast('success', result.message);
        } else {
          addToast('error', result.error || 'Export failed');
        }
      } catch (e) {
        // Try callback style
        window.bridge.export_handoff(sessionName, outputFolder, JSON.stringify(approvedContent), function (r) {
          try {
            const res = JSON.parse(r);
            if (res.success) {
              setExported(true);
              setExportPath(res.file_path);
              addToast('success', res.message);
            } else {
              addToast('error', res.error || 'Export failed');
            }
          } catch (ex) {
            // Browser mock fallback
            setExported(true);
            setExportPath(`data/sessions/${sessionName}/ai_handoff.json`);
            addToast('success', 'Exported successfully (demo mode)');
          }
        });
      }
    } else {
      // Pure browser fallback
      setExported(true);
      setExportPath(`data/sessions/${sessionName}/ai_handoff.json`);
      addToast('success', 'Exported successfully (demo mode)');
    }
  };

  return (
    <AnimatedPage keyName="handoff">
      <div className="page-header">
        <h1 className="page-title">
          <Icons.ArrowRight {...iconLg} /> Handoff to Broadcast Graphics Engine
        </h1>
        <p className="page-subtitle">Export approved content to HiruTaglineCreator v2.1</p>
      </div>

      {/* Status Card */}
      <div className="card" style={{ marginBottom: 'var(--space-5)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
          <span className="badge badge-success" style={{ fontSize: 14, padding: '6px 16px' }}>
            <Icons.CheckCircle {...iconSm} /> Approved
          </span>
          <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
            Bulletin: {metadata.bulletinSlot} · Priority: {metadata.priority} · {selectedSugs.length} tagline sets · Approved: {formatTimestamp()}
          </span>
        </div>
      </div>

      {exported ? (
        /* Export Success State */
        <div className="card">
          <div className="export-success">
            <div className="export-success-icon" style={{ animation: 'bounceIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)' }}>
              <Icons.CheckCircle style={{ width: 40, height: 40 }} />
            </div>
            <div className="export-success-text">Export Successful!</div>
            <div className="export-success-path">{exportPath}</div>
            <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
              <button className="btn btn-ghost btn-sm">
                <Icons.FolderOpen {...iconSm} /> View Exported File
              </button>
              <button className="btn btn-secondary btn-sm">
                <Icons.ExternalLink {...iconSm} /> Launch HiruTaglineCreator
              </button>
            </div>
          </div>
          <style>{`
            @keyframes bounceIn {
              0% { transform: scale(0); opacity: 0; }
              60% { transform: scale(1.15); }
              100% { transform: scale(1); opacity: 1; }
            }
          `}</style>
        </div>
      ) : (
        <>
          {/* Approved Content Preview */}
          <div className="card" style={{ marginBottom: 'var(--space-5)' }}>
            <div className="card-header">
              <h3 className="card-title">Approved Content Preview</h3>
            </div>
            <div style={{ maxHeight: 300, overflowY: 'auto' }}>
              {selectedSugs.map((sug) => (
                <div key={sug.id} className="tagline-preview" style={{ marginBottom: 'var(--space-3)' }}>
                  <div className="tagline-preview-strip red-bed">{sug.topic_bed}</div>
                  {sug.tag_lines.map((line, li) => (
                    <div key={li} className="tagline-preview-strip orange-bed">{line}</div>
                  ))}
                  <div className="tagline-preview-strip white-bed">{sug.white_bed}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Export Configuration */}
          <div className="card" style={{ marginBottom: 'var(--space-5)' }}>
            <div className="card-header">
              <h3 className="card-title">Export Configuration</h3>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-5)' }}>
              <div className="form-group">
                <label className="form-label">Session Name</label>
                <input className="input mono" value={sessionName}
                  onChange={(e) => setSessionName(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Output Folder</label>
                <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                  <input className="input mono" value={outputFolder}
                    placeholder="Default: data/sessions/"
                    onChange={(e) => setOutputFolder(e.target.value)} />
                  <button className="btn btn-secondary" onClick={browseFolderHandler}>Browse...</button>
                </div>
              </div>
            </div>
            <div style={{ marginTop: 'var(--space-3)', fontSize: 13, color: 'var(--text-muted)' }}>
              Will export to: <span className="mono">{outputFolder || 'data/sessions'}/{sessionName}/ai_handoff.json</span>
            </div>
          </div>
        </>
      )}

      {/* Action Bar */}
      <div className="action-bar">
        <button className="btn btn-ghost" onClick={onBack}>
          <Icons.ArrowLeft {...iconSm} /> Back to Approval
        </button>
        <div className="action-bar-right">
          <button className="btn btn-secondary">
            <Icons.ExternalLink {...iconSm} /> Launch HiruTaglineCreator
          </button>
          {!exported && (
            <button className="btn btn-primary" onClick={doExport}>
              Export to HiruTaglineCreator <Icons.ArrowRight {...iconSm} />
            </button>
          )}
        </div>
      </div>
    </AnimatedPage>
  );
}


// ─────────────────────────────────────────────────────────────
// SCREEN 6: DASHBOARD
// ─────────────────────────────────────────────────────────────

function DashboardScreen() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Load dashboard data
    if (window.bridge && window.bridge.load_dashboard_data) {
      try {
        const r = window.bridge.load_dashboard_data();
        setData(JSON.parse(r));
      } catch (e) {
        window.bridge.load_dashboard_data(function (r) {
          try { setData(JSON.parse(r)); } catch (ex) { }
        });
      }
    }
    // Fallback if no bridge or timeout
    setTimeout(() => {
      if (!data) {
        setData({
          stats: { taglines_today: 42, taglines_approved: 38, pending_review: 4, avg_time_per_tagline: 142, trends: { taglines_today_pct: 12, approved_pct: 8, pending_pct: -3, avg_time_pct: -5 } },
          chart: [{ day: 'Dec 4', taglines: 28 }, { day: 'Dec 5', taglines: 35 }, { day: 'Dec 6', taglines: 22 }, { day: 'Dec 7', taglines: 40 }, { day: 'Dec 8', taglines: 31 }, { day: 'Dec 9', taglines: 45 }, { day: 'Dec 10', taglines: 42 }],
          sessions: [
            { id: 1, session: 'AKUREGODA', bulletin_slot: '6:55 PM', taglines: 18, status: 'Approved', timestamp: '2025-12-10 17:22' },
            { id: 2, session: 'DITWA_CYCLONE', bulletin_slot: '9:55 PM', taglines: 24, status: 'Approved', timestamp: '2025-12-10 21:10' },
            { id: 3, session: 'MATARA_FLOOD', bulletin_slot: '11:55 AM', taglines: 15, status: 'Pending Review', timestamp: '2025-12-10 10:44' },
            { id: 4, session: 'PARLIAMENT', bulletin_slot: '6:55 PM', taglines: 21, status: 'Approved', timestamp: '2025-12-09 17:31' },
            { id: 5, session: 'ECONOMY_Q3', bulletin_slot: '9:55 PM', taglines: 19, status: 'Approved', timestamp: '2025-12-09 20:58' },
            { id: 6, session: 'GALLE_ROAD', bulletin_slot: '11:55 AM', taglines: 12, status: 'Rejected', timestamp: '2025-12-08 11:12' },
            { id: 7, session: 'CABINET_MTG', bulletin_slot: '6:55 PM', taglines: 17, status: 'Approved', timestamp: '2025-12-08 16:45' },
            { id: 8, session: 'HEALTH_MIN', bulletin_slot: '9:55 PM', taglines: 20, status: 'Changes Requested', timestamp: '2025-12-07 21:03' },
          ],
          health: [{ name: 'OpenAI API', status: 'Connected', color: 'green' }, { name: 'Local Storage', status: 'OK', color: 'green' }, { name: 'HiruTaglineCreator Bridge', status: 'Ready', color: 'green' }],
          performance: { transcription_avg_time: '18.4s', generation_avg_time: '12.1s', success_rate: '96.8%', transcription_pct: 92, generation_pct: 88, success_pct: 97 },
        });
      }
    }, 500);
  }, []);

  if (!data) {
    return (
      <AnimatedPage keyName="dashboard">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '50vh' }}>
          <Icons.Loader className="spin" style={{ width: 32, height: 32, color: 'var(--ai-accent)' }} />
        </div>
      </AnimatedPage>
    );
  }

  const statusBadgeClass = (status) => {
    switch (status) {
      case 'Approved': return 'badge-success';
      case 'Pending Review': return 'badge-warning';
      case 'Rejected': return 'badge-error';
      case 'Changes Requested': return 'badge-warning';
      default: return 'badge-neutral';
    }
  };

  // Use Recharts if available
  const hasRecharts = typeof Recharts !== 'undefined';

  return (
    <AnimatedPage keyName="dashboard">
      <div className="page-header">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h1 className="page-title"><Icons.LayoutDashboard {...iconLg} /> Dashboard</h1>
            <p className="page-subtitle">Production activity and system health</p>
          </div>
          <button className="btn btn-ghost btn-sm"><Icons.RefreshCw {...iconSm} /> Refresh</button>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="stats-grid" style={{ marginBottom: 'var(--space-6)' }}>
        <StaggerChild index={0}>
          <div className="stat-card red">
            <div className="stat-icon-wrapper red"><Icons.Sparkles {...iconSize} /></div>
            <div className="stat-value">{data.stats.taglines_today}</div>
            <div className="stat-label">Taglines Generated Today</div>
            <div className={`stat-trend ${data.stats.trends.taglines_today_pct >= 0 ? 'up' : 'down'}`}>
              {data.stats.trends.taglines_today_pct >= 0 ? <Icons.TrendingUp {...iconSm} /> : <Icons.TrendingDown {...iconSm} />}
              {Math.abs(data.stats.trends.taglines_today_pct)}% from yesterday
            </div>
          </div>
        </StaggerChild>
        <StaggerChild index={1}>
          <div className="stat-card green">
            <div className="stat-icon-wrapper green"><Icons.CheckCircle {...iconSize} /></div>
            <div className="stat-value">{data.stats.taglines_approved}</div>
            <div className="stat-label">Taglines Approved</div>
            <div className="stat-trend up">
              <Icons.TrendingUp {...iconSm} /> {data.stats.trends.approved_pct}% from yesterday
            </div>
          </div>
        </StaggerChild>
        <StaggerChild index={2}>
          <div className="stat-card amber">
            <div className="stat-icon-wrapper amber"><Icons.Clock {...iconSize} /></div>
            <div className="stat-value">{data.stats.pending_review}</div>
            <div className="stat-label">Pending Review</div>
            <div className="stat-trend down">
              <Icons.TrendingDown {...iconSm} /> {Math.abs(data.stats.trends.pending_pct)}% from yesterday
            </div>
          </div>
        </StaggerChild>
        <StaggerChild index={3}>
          <div className="stat-card blue">
            <div className="stat-icon-wrapper blue"><Icons.Timer {...iconSize} /></div>
            <div className="stat-value">{data.stats.avg_time_per_tagline}s</div>
            <div className="stat-label">Avg Time per Tagline</div>
            <div className="stat-trend down">
              <Icons.TrendingDown {...iconSm} /> {Math.abs(data.stats.trends.avg_time_pct)}% faster
            </div>
          </div>
        </StaggerChild>
      </div>

      {/* Chart Card */}
      <div className="card" style={{ marginBottom: 'var(--space-6)' }}>
        <div className="card-header">
          <h3 className="card-title">Taglines Created — Last 7 Days</h3>
        </div>
        <div className="chart-container">
          {hasRecharts ? (
            <Recharts.ResponsiveContainer width="100%" height={280}>
              <Recharts.BarChart data={data.chart} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <Recharts.CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <Recharts.XAxis dataKey="day" tick={{ fill: 'var(--text-muted)', fontSize: 12 }} axisLine={{ stroke: 'var(--border)' }} />
                <Recharts.YAxis tick={{ fill: 'var(--text-muted)', fontSize: 12 }} axisLine={{ stroke: 'var(--border)' }} />
                <Recharts.Tooltip
                  contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--text-primary)' }}
                  labelStyle={{ color: 'var(--text-secondary)' }}
                />
                <Recharts.Bar dataKey="taglines" fill="#E63946" radius={[6, 6, 0, 0]} />
              </Recharts.BarChart>
            </Recharts.ResponsiveContainer>
          ) : (
            /* Fallback: CSS-only bar chart */
            <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-around', height: '100%', padding: '20px 0' }}>
              {data.chart.map((d, i) => (
                <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, flex: 1 }}>
                  <div style={{
                    width: 40,
                    height: `${(d.taglines / 50) * 220}px`,
                    background: 'linear-gradient(180deg, #E6394680, #E63946)',
                    borderRadius: '6px 6px 0 0',
                    transition: 'height 0.5s ease',
                  }}></div>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{d.day}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Secondary Row: Performance + Health */}
      <div className="two-col-even" style={{ marginBottom: 'var(--space-6)' }}>
        <StaggerChild index={0}>
          <div className="card">
            <div className="card-header">
              <h3 className="card-title"><Icons.Sparkles {...iconSm} style={{ color: 'var(--ai-accent)' }} /> AI Processing Performance</h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
              {[
                { label: 'Transcription Avg', value: data.performance.transcription_avg_time, pct: data.performance.transcription_pct, color: 'var(--info)' },
                { label: 'Generation Avg', value: data.performance.generation_avg_time, pct: data.performance.generation_pct, color: 'var(--ai-accent)' },
                { label: 'Success Rate', value: data.performance.success_rate, pct: data.performance.success_pct, color: 'var(--success)' },
              ].map((m, i) => (
                <div key={i}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{m.label}</span>
                    <span style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)' }}>{m.value}</span>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${m.pct}%`, background: m.color }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </StaggerChild>
        <StaggerChild index={1}>
          <div className="card">
            <div className="card-header">
              <h3 className="card-title"><Icons.Shield {...iconSm} /> System Health</h3>
            </div>
            {data.health.map((h, i) => (
              <div key={i} className="health-row">
                <span className="health-name">{h.name}</span>
                <div className="health-status">
                  <div className={`health-dot ${h.color}`}></div>
                  <span style={{ color: h.color === 'green' ? 'var(--success)' : h.color === 'amber' ? 'var(--warning)' : 'var(--error)' }}>{h.status}</span>
                </div>
              </div>
            ))}
          </div>
        </StaggerChild>
      </div>

      {/* Recent Sessions Table */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Recent Sessions</h3>
          <button className="btn btn-ghost btn-sm">View All</button>
        </div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Session</th>
                <th>Bulletin Slot</th>
                <th>Taglines</th>
                <th>Status</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {data.sessions.map((s) => (
                <tr key={s.id}>
                  <td style={{ color: 'var(--text-muted)' }}>{s.id}</td>
                  <td><span className="mono" style={{ fontWeight: 600 }}>{s.session}</span></td>
                  <td>{s.bulletin_slot}</td>
                  <td>{s.taglines}</td>
                  <td><span className={`badge ${statusBadgeClass(s.status)}`}>{s.status}</span></td>
                  <td className="mono" style={{ color: 'var(--text-secondary)' }}>{s.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AnimatedPage>
  );
}


// ─────────────────────────────────────────────────────────────
// APP STATE REDUCER
// ─────────────────────────────────────────────────────────────

const initialState = {
  files: [],
  metadata: {
    reporter: '',
    location: '',
    bulletinSlot: '6:55 PM',
    priority: 'Headline',
  },
  transcriptionStatus: 'idle', // idle | processing | complete | error
  transcriptionProgress: 0,
  transcript: [],
  suggestions: [],
  selectedSuggestions: [],
  approvalChecklist: [false, false, false, false, false],
  editorNotes: '',
  exportStatus: null,
};

function appReducer(state, action) {
  switch (action.type) {
    case 'ADD_FILES':
      return { ...state, files: [...state.files, ...action.payload] };
    case 'REMOVE_FILE':
      return { ...state, files: state.files.filter((_, i) => i !== action.payload) };
    case 'SET_METADATA':
      return { ...state, metadata: { ...state.metadata, ...action.payload } };
    case 'SET_TRANSCRIPTION_STATUS':
      return { ...state, transcriptionStatus: action.payload };
    case 'SET_TRANSCRIPTION_PROGRESS':
      return { ...state, transcriptionProgress: action.payload };
    case 'SET_TRANSCRIPT':
      return { ...state, transcript: action.payload, transcriptionStatus: 'complete' };
    case 'SET_SUGGESTIONS':
      return {
        ...state,
        suggestions: action.payload,
        selectedSuggestions: action.payload.map(s => s.id), // Select all by default
      };
    case 'TOGGLE_SUGGESTION': {
      const id = action.payload;
      const sel = state.selectedSuggestions.includes(id)
        ? state.selectedSuggestions.filter(x => x !== id)
        : [...state.selectedSuggestions, id];
      return { ...state, selectedSuggestions: sel };
    }
    case 'UPDATE_SUGGESTION': {
      const { id, field, value } = action.payload;
      return {
        ...state,
        suggestions: state.suggestions.map(s =>
          s.id === id ? { ...s, [field]: value } : s
        ),
      };
    }
    case 'TOGGLE_CHECKLIST': {
      const newChecklist = [...state.approvalChecklist];
      newChecklist[action.payload] = !newChecklist[action.payload];
      return { ...state, approvalChecklist: newChecklist };
    }
    case 'SET_EDITOR_NOTES':
      return { ...state, editorNotes: action.payload };
    case 'SET_EXPORT_STATUS':
      return { ...state, exportStatus: action.payload };
    default:
      return state;
  }
}


// ─────────────────────────────────────────────────────────────
// MAIN APP COMPONENT
// ─────────────────────────────────────────────────────────────

function App() {
  const [currentScreen, setCurrentScreen] = useState('upload');
  const [theme, setTheme] = useState('dark');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [toasts, setToasts] = useState([]);
  const [state, dispatch] = useReducer(appReducer, initialState);
  const toastIdRef = useRef(0);

  // Apply theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Setup WebChannel bridge
  useEffect(() => {
    if (typeof QWebChannel !== 'undefined' && window.qt && window.qt.webChannelTransport) {
      new QWebChannel(window.qt.webChannelTransport, function (channel) {
        window.bridge = channel.objects.bridge;

        // Connect signals
        if (window.bridge.transcriptionProgress) {
          window.bridge.transcriptionProgress.connect(function (data) {
            try {
              const p = JSON.parse(data);
              dispatch({ type: 'SET_TRANSCRIPTION_PROGRESS', payload: p.percent });
            } catch (e) { }
          });
        }
        if (window.bridge.transcriptionComplete) {
          window.bridge.transcriptionComplete.connect(function (data) {
            try {
              const result = JSON.parse(data);
              if (result.status === 'complete') {
                dispatch({ type: 'SET_TRANSCRIPT', payload: result.segments });
              }
            } catch (e) { }
          });
        }
        if (window.bridge.taglineComplete) {
          window.bridge.taglineComplete.connect(function (data) {
            try {
              const result = JSON.parse(data);
              if (result.status === 'complete') {
                dispatch({ type: 'SET_SUGGESTIONS', payload: result.suggestions });
              }
            } catch (e) { }
          });
        }
      });
    } else {
      // Browser fallback — setup mock bridge
      new QWebChannel(null, function (channel) {
        window.bridge = channel.objects.bridge;
      });
    }
  }, []);

  // Toggle theme
  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

  // Toast management
  const addToast = useCallback((type, message) => {
    const id = ++toastIdRef.current;
    setToasts(prev => [...prev, { id, type, message }]);
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
  }, []);

  const dismissToast = useCallback((id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  // Navigation
  const navigate = (screen) => setCurrentScreen(screen);

  // Start AI Processing (Upload -> Transcription)
  const startProcessing = () => {
    setCurrentScreen('transcription');
    dispatch({ type: 'SET_TRANSCRIPTION_STATUS', payload: 'processing' });
    dispatch({ type: 'SET_TRANSCRIPTION_PROGRESS', payload: 0 });

    // Call bridge
    const filePath = state.files.length > 0 ? state.files[0].path : 'sample.wav';

    if (window.bridge && window.bridge.start_transcription) {
      try {
        window.bridge.start_transcription(filePath);
      } catch (e) {
        window.bridge.start_transcription(filePath, function () { });
      }
    }

    // Mock progress simulation for browser mode
    if (!window.qt || !window.qt.webChannelTransport) {
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.random() * 15 + 5;
        if (progress >= 100) {
          progress = 100;
          clearInterval(interval);
          // Load mock transcript
          setTimeout(() => {
            dispatch({ type: 'SET_TRANSCRIPT', payload: MOCK_TRANSCRIPTS });
            // Also pre-generate suggestions
            dispatch({ type: 'SET_SUGGESTIONS', payload: MOCK_SUGGESTIONS });
            addToast('success', 'Transcription completed successfully');
          }, 500);
        }
        dispatch({ type: 'SET_TRANSCRIPTION_PROGRESS', payload: Math.min(Math.round(progress), 100) });
      }, 350);
    }
  };

  // Continue to suggestions
  const continueToSuggestions = () => {
    setCurrentScreen('suggestions');
    // If suggestions not yet loaded, generate them
    if (state.suggestions.length === 0) {
      if (window.bridge && window.bridge.generate_taglines) {
        const transcriptJson = JSON.stringify(state.transcript);
        try {
          window.bridge.generate_taglines(transcriptJson, state.metadata.bulletinSlot);
        } catch (e) {
          window.bridge.generate_taglines(transcriptJson, state.metadata.bulletinSlot, function () { });
        }
      }
      // Browser fallback
      if (!window.qt || !window.qt.webChannelTransport) {
        setTimeout(() => {
          dispatch({ type: 'SET_SUGGESTIONS', payload: MOCK_SUGGESTIONS });
        }, 800);
      }
    }
  };

  // Approve
  const handleApprove = () => {
    addToast('success', 'Content approved! Proceeding to handoff...');
    setCurrentScreen('handoff');
  };

  // Session name
  const sessionName = state.files.length > 0
    ? state.files[0].name.replace(/\.[^.]+$/, '').toUpperCase()
    : generateSessionName();

  // Render current screen
  const renderScreen = () => {
    switch (currentScreen) {
      case 'upload':
        return <UploadScreen state={state} dispatch={dispatch} onStartProcessing={startProcessing} addToast={addToast} />;
      case 'transcription':
        return <TranscriptionScreen state={state} dispatch={dispatch}
          onBack={() => navigate('upload')} onContinue={continueToSuggestions} />;
      case 'suggestions':
        return <SuggestionsScreen state={state} dispatch={dispatch}
          onBack={() => navigate('transcription')} onContinue={() => navigate('approval')} addToast={addToast} />;
      case 'approval':
        return <ApprovalScreen state={state} dispatch={dispatch}
          onBack={() => navigate('suggestions')} onApprove={handleApprove} addToast={addToast} />;
      case 'handoff':
        return <HandoffScreen state={state} dispatch={dispatch}
          onBack={() => navigate('approval')} addToast={addToast} />;
      case 'dashboard':
        return <DashboardScreen />;
      default:
        return <UploadScreen state={state} dispatch={dispatch} onStartProcessing={startProcessing} addToast={addToast} />;
    }
  };

  return (
    <div className="app-shell">
      <TopBar theme={theme} onToggleTheme={toggleTheme} sessionName={sessionName} />
      <div className="app-body">
        <Sidebar currentScreen={currentScreen} onNavigate={navigate}
          collapsed={sidebarCollapsed} onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)} />
        <main className="main-content">
          {renderScreen()}
        </main>
      </div>
      <ToastContainer toasts={toasts} onDismiss={dismissToast} />
    </div>
  );
}


// ─────────────────────────────────────────────────────────────
// RENDER
// ─────────────────────────────────────────────────────────────

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
