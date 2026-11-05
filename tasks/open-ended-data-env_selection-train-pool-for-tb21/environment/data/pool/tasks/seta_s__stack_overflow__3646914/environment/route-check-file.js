const express = require('express');
const router = express.Router();
const { checkFileExists } = require('../lib/file-checker');

router.get('/check-file', async (req, res) => {
    const filePath = req.query.path;

    if (!filePath) {
        return res.status(400).json({ error: 'Missing path parameter' });
    }

    try {
        const exists = await checkFileExists(filePath);
        res.json({ exists });
    } catch (err) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
