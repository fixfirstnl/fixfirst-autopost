module.exports = {
  apps: [{
    name: 'claw-bridge',
    script: 'server.js',
    cwd: '/opt/fixfirst-autopost/claw-autonomy-bridge',
    env: { NODE_ENV: 'production', PORT: 3006 },
    max_restarts: 10,
    restart_delay: 5000
  }]
};
