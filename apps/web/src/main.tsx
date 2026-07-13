import React from "react";
import ReactDOM from "react-dom/client";
import "@helm/ui/styles.css";
import "./workbench.css";
import { App } from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
