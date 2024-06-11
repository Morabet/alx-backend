import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
import express from 'express';

const client = createClient();
client.on('error', (err) => {
  console.error('Redis client not connected to the server:', err);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const reserveSeat = async (number) => promisify(client.set).bind(client)('available_seats', number);

const getCurrentAvailableSeats = async () => promisify(client.get).bind(client)('available_seats');

const initialSeats = 50;
let reservationEnabled = true;

reserveSeat(initialSeats).then(() => console.log(`Initialized available seats to ${initialSeats}`));

const queue = createQueue();
const app = express();
const PORT = 1245;

app.get('/available_seats', async (req, res) => {
  try {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats });
  } catch (error) {
    res.json({ status: 'Error retrieving available seats', error });
  }
});

app.get('/reserve_seat', async (req, res) => {
  if (reservationEnabled === false) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    return res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentSeats = await getCurrentAvailableSeats();

      if (currentSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }

      const newSeats = currentSeats - 1;
      await reserveSeat(newSeats);

      if (newSeats === 0) {
        reservationEnabled = false;
      }

      done();
    } catch (error) {
      done(error);
    }
  });

  return res.json({ status: 'Queue processing' });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

