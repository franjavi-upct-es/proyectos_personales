const cron = require('node-cron');
const { runFolder } = require('./tasks.service');
let scheduledTask = null;

function scheduleJob({ hour = 0, minute = 0, second = 0 }) {
    if (scheduledTask) scheduledTask.destroy();
    const expr = `${second} ${minute} ${hour} * * *`;
    scheduledTask = cron.schedule(expr, runFolder);
}

function getStatus() {
    return scheduledTask
        ? { scheduled: true, nextRun: scheduledTask.nextDates().toDate().toISOString() }
        : {scheduled: false, nextRun: null };
}

module.exports = { scheduleJob, getStatus };