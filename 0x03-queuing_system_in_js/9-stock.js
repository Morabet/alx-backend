import expect from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const client = createClient();

client.on('error', (err) => {
  console.error('Redis client not connected to the server:', err);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const listProducts = [
  {
    Id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    Id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    Id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    Id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

const getItemById = (id) => listProducts.find((product) => product.Id === id);

const reserveStockById = (itemId, stock) => {
  // return client.set(`item.${itemId}`, stock)
  promisify(client.set).bind(client)(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  // client.get(itemId)
  const value = await promisify(client.get).bind(client)(itemId);
  return parseInt(value, 10);
};

// Initialize the stock in Redis for all products
listProducts.forEach((product) => {
  reserveStockById(product.itemId, product.stock);
});

const app = expect();
const PORT = 1245;

app.get('/list_products', (req, res) => {
  const products = listProducts.map((product) => ({
    itemId: product.Id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  }));
  res.json(products);
});

app.get('/list_products/:itemId(\\d+)', async (req, res) => {
  const itemId = parseInt(req.params.Id, 10);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  try {
    const currentStock = await getCurrentReservedStockById(itemId);
    res.send({
      itemId: product.Id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity: parseInt(currentStock, 10) || product.stock,
    });
  } catch (err) {
    res.json({ status: 'Error retrieving stock', err });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.Id, 10);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  try {
    const currentStock = await getCurrentReservedStockById(itemId);
    if (currentStock <= 0) {
      res.json({ status: 'Not enough stock available', itemId });
      return;
    }
    reserveStockById(itemId, currentStock - 1);
    res.json({ status: 'Reservation confirmed', itemId });
  } catch (err) {
    res.json({ status: 'Error reserving stock', err });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

export default app;

