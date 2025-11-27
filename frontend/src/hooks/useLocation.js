// frontend/src/hooks/useLocation.js

import { useState, useEffect } from "preact/hooks";
import { Router } from "preact-router";

export function useLocation() {
  const [url, setUrl] = useState(window.location.pathname);

  useEffect(() => {
    const handler = (e) => setUrl(window.location.pathname);
    window.addEventListener("popstate", handler);
    return () => window.removeEventListener("popstate", handler);
  }, []);

  return { pathname: url };
}
