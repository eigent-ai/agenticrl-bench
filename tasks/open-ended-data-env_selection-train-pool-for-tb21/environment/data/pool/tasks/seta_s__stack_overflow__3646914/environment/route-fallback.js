const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const config = require('../config.json');

router.use('/static/themes', (req, res, next) => {
    if (res.headersSent) {
        return next();
    }

    const urlPath = req.path;
    if (urlPath.endsWith('/logo.png')) {
        const fallbackPath = config.fallbackImage;

        if (fs.existsSync(fallbackPath)) {
            return res.sendFile(fallbackPath);
        }
    }

    next();
});

module.exports = router;
