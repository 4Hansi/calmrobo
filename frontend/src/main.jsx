// frontend/src/main.jsx

import { render } from "preact";
import AppRouter from "./router.jsx";
import "./index.css";

render(<AppRouter />, document.getElementById("root"));
