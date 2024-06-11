import { createClient, print } from 'redis';

const client = createClient();

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Function to set hash values
const updateHash = (hashName, field, value) => {
  client.HSET(hashName, field, value, print);
};
// Function to display hash values
const printHashObj = async (hashName) => {
  try {
    const value = await client.HGETALL(hashName);
    console.log(value);
  } catch (error) {
    console.error('Error getting value:', error);
  }
};

const hashObj = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const [field, value] of Object.entries(hashObj)) {
  updateHash('HolbertonSchools', field, value);
}

printHashObj('HolbertonSchools');

