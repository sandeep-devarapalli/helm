import React, { Suspense, lazy } from "react";
import ReactDOM from "react-dom/client";
import "@helm/ui/styles.css";
import { LandingPage } from "./LandingPage";

const WorkbenchApp = lazy(async () => {
  const module = await import("./App");
  return { default: module.App };
});

const initialUrl = new URL(window.location.href);
if (initialUrl.pathname === "/" && initialUrl.searchParams.has("workspace")) {
  initialUrl.pathname = "/app";
  window.history.replaceState(null, "", initialUrl);
}

function RootRoute() {
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  if (path !== "/app") return <LandingPage />;
  return (
    <Suspense fallback={<div className="route-loading">Loading Workbench</div>}>
      <WorkbenchApp />
    </Suspense>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RootRoute />
  </React.StrictMode>,
);
