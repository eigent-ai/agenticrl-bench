const express = require("express");
const app = express();

app.get("/", (req, res) => {
    res.send("Frontend OK");
});

app.get("/status", (req, res) => {
    res.send("Node.js running");
});

app.listen(3000, "127.0.0.1", () => {
    console.log("Node.js frontend running on port 3000");
});
