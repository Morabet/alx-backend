const kue = require('kue');

const queue = kue.createQueue();

const job = queue.create('push_notification_code', {
  phoneNumber: '',
  message: '',
}).save((err) => {
  if (!err) console.log(`Notification job created: ${job.id}`);
});

job
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    console.log('Notification job failed');
  });

