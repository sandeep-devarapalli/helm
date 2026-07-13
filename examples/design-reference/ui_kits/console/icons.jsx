/* Lucide-style inline icon set for the helm workbench kit. 2px stroke. */
const svg = (children, size = 16) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">{children}</svg>
);
window.Icons = {
  dollar: (s) => svg(<><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></>, s),
  target: (s) => svg(<><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></>, s),
  zap: (s) => svg(<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>, s),
  landmark: (s) => svg(<path d="M3 21h18M4 18h16M6 18V9M10 18V9M14 18V9M18 18V9M12 3 2 9h20L12 3z"/>, s),
  chevDown: (s) => svg(<polyline points="6 9 12 15 18 9"/>, s),
  chevRight: (s) => svg(<polyline points="9 18 15 12 9 6"/>, s),
  chevUp: (s) => svg(<polyline points="18 15 12 9 6 15"/>, s),
  msg: (s) => svg(<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>, s),
  plus: (s) => svg(<><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></>, s),
  x: (s) => svg(<path d="M18 6 6 18M6 6l12 12"/>, s),
  refresh: (s) => svg(<><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/></>, s),
  file: (s) => svg(<><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M14 2v5h5"/></>, s),
  wrench: (s) => svg(<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>, s),
  arrowUp: (s) => svg(<><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></>, s),
  external: (s) => svg(<><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></>, s),
  shield: (s) => svg(<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>, s),
  coins: (s) => svg(<><circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/></>, s),
};
