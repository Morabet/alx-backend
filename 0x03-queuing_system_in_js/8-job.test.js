import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const kue = require('kue');

describe('createPushNotificationsJobs', () => {
  let queue;
  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter(); // Enter test mode
  });
  afterEach(() => {
    queue.testMode.clear(); // Clear the queue after each test
    queue.testMode.exit(); // Exit test mode after each test
  });

  it('testing jobs not array', () => {
    expect(() => createPushNotificationsJobs('invalid', queue)).to.throw(Error, 'Jobs is not an array');
  });
  it('should create jobs in the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account',
      },
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(1);
  	expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
  	expect(queue.testMode.jobs[0].data).to.eql(
    	{
  		phoneNumber: '4153518781',
    	message: 'This is the code 4562 to verify your account',
    	},
    );
  });
});

