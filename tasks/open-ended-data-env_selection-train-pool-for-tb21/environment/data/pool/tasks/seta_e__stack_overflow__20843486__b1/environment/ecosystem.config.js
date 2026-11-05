module.exports = {
  apps: [{
    name: 'tasktracker',
    script: 'app.js',
    instances: 1,
    exec_mode: 'fork'
  }]
};
